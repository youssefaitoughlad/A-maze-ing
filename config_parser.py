from pydantic import BaseModel, Field, ValidationError
from pydantic import model_validator, field_validator
from typing import List, Tuple
import os


class ConfigValidate(BaseModel):
    model_config = {"extra": "forbid"}

    width: int = Field(default=10)
    height: int = Field(default=10)
    entry: tuple[int, int] = Field(default=(0, 0))
    exit_: tuple[int, int] = Field(default=(9, 9))
    perfect: bool = False
    output_file: str = Field(..., min_length=1, max_length=50)
    seed: int = Field(default=8, ge=0)

    @field_validator('width', 'height')
    @classmethod
    def grid_validate(cls, v: int) -> int:
        if v < 3:
            raise ValueError(
                f"Maze sizes must be > 3, i got {v}"
            )
        if v > 30:
            raise ValueError(
                f"Maze sizes must be <= 30, i got {v}"
            )
        return v

    @field_validator('entry', 'exit_', mode='before')
    @classmethod
    def coordinates_valbefore(cls, v: List[str]) -> List[int]:
        converted = []
        try:
            for item in v:
                converted.append(int(item))
        except ValueError:
            raise ValueError(
                f"coordinates must be a valid integer (got: {v})"
            )
        return converted

    @field_validator('entry', 'exit_')
    @classmethod
    def coordinates_validation(cls, v: tuple[int, int]) -> tuple[int, int]:
        for item in v:
            if item < 0:
                raise ValueError(f"coordinates must be positive, i got {v}")
        return v

    @model_validator(mode='after')
    def entry_exit_validation(self) -> 'ConfigValidate':
        errors = []

        if self.entry == self.exit_:
            errors.append(
                "entry and exit coordinates must "
                f"be different, i got {self.entry}"
            )
        if self.entry[0] >= self.width:
            errors.append("entry coordinates exceeded the width")
        if self.entry[1] >= self.height:
            errors.append("entry coordinates exceeded the height")

        if self.exit_[0] >= self.width:
            errors.append("exit coordinates exceeded the width")
        if self.exit_[1] >= self.height:
            errors.append("exit coordinates exceeded the height")

        if not self.output_file.endswith(".txt"):
            errors.append("output_file must be a .txt file")
        directory = os.path.dirname(os.path.abspath(self.output_file)) or '.'
        if not os.path.exists(directory):
            errors.append(f"Directory does not exist: {directory}")
        elif not os.access(directory, os.W_OK):
            errors.append(f"Cannot write to directory: {directory}")
        if errors:
            raise ValueError("\n".join(errors))
        return self


class ConfigParser:
    def __init__(self, path: str) -> None:
        self.config: ConfigValidate = self.get_config(path)

    def get_config(self, path: str) -> ConfigValidate:
        try:
            with open(path, 'r') as f:
                lines = f.readlines()
        except PermissionError:
            raise PermissionError(
                f"Permission denied to read '{path}'"
            )
        except FileNotFoundError:
            raise FileNotFoundError(
                f"The file '{path}' does not exist."
            )

        clean_config = []
        for line in lines:
            line = line.strip()

            if not line or line.startswith('#'):
                continue
            clean_config.append(line)

        config = {}
        for line in clean_config:
            if "=" not in line:
                raise ValueError(
                    "some line not contain '='"
                )
            splited = line.split('=')
            if len(splited) == 2:
                key, value = splited
                config[key.strip()] = value.strip()
            else:
                raise ValueError("configs must be with one '='")
        return self.config_key_lower(config)

    def config_key_lower(self, config: dict) -> ConfigValidate:
        mandadory_keys = [
            'width', 'height', 'entry', 'exit_', 'output_file', 'perfect'
        ]
        config_l = {}

        for key in config:
            l_key = key.lower()
            if l_key == 'exit':
                l_key += '_'
            config_l[l_key] = config[key]

        for man in mandadory_keys:
            if man not in config_l.keys():
                raise ValueError(f"Missing mandatory config keys: {man}")
        return self.convert_values(config_l)

    def convert_values(self, config: dict) -> ConfigValidate:
        lst = ['entry', 'exit_']
        for key in config:
            if key in lst:
                if ',' not in config[key]:
                    raise ValueError(f"',' missed in {key}")
                items = config[key].split(',')
                if len(items) != 2:
                    raise ValueError(
                        f"coordinates use 2 values(x-y), i got {tuple(items)}"
                    )
                config[key] = [item.strip() for item in items]
            if key == 'perfect':
                config[key] = config[key].lower() == "true"

        int_keys = ['width', 'height', 'seed']
        for key in int_keys:
            if key in config:
                try:
                    config[key] = int(config[key])
                except (ValueError):
                    raise ValueError(
                        f"'{key}' must be an integer, got '{config[key]}'"
                    )

        try:
            py_config = ConfigValidate(**config)
        except ValidationError as err:
            messages = [e['msg'] for e in err.errors()]
            raise ValueError("\n".join(messages))
        return py_config


def main() -> None:
    try:
        _ = ConfigParser("config.txt")
    except Exception as err:
        print(f"{err}")


main()
