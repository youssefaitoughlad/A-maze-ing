from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional

class ConfigValidate(BaseModel):
    width: int = Field(...)
    height: int = Field(...)
    entry: tuple[int, int] = (0, 0)
    exit_ : tuple[int, int] = Field(...)
    perfect: bool = False
    output_file: str = Field(..., min_length=0, max_length=20)


class ConfigParsar:
    def __init__(self, path: str) -> None:
        self.config: ConfigValidate = self.get_config(path)


    def get_config(self, path: str) -> ConfigValidate:
        try:
            with open(path, 'r') as f:
                lines = f.readlines()
        except PermissionError:
            raise PermissionError(
                f"Error: Permission denied to read '{path}'"
            )

        clean_config = []
        for line in lines:
            line = line.strip()

            if not line or line.startswith('#'):
                continue
            clean_config.append(line)

        config = dict()
        for line in clean_config:
            splited = line.split('=')
            if len(splited) == 2:
                key, value = splited
                config[key.strip()] = value.strip()
        return self.config_key_lower(config)

    def config_key_lower(self, config: dict) -> ConfigValidate:
        config_l = dict()

        for key in config:
            l_key = key.lower()
            if key == 'EXIT':
                l_key += '_'
            config_l[l_key] = config[key]
        return self.convert_values(config_l)

    def convert_values(self, config: dict) -> ConfigValidate:
        lst = ['entry', 'exit_']
        for key in config:
            if key in lst:
                items = config[key].split(',')
                config[key] = [item.strip() for item in items]
            if key == 'perfect':
                

        try:
            



def main() -> None:
    parser = ConfigParsar()
    parser.get_config("config.txt")
    parser.config_key_lower()
    print(parser.config_str)


main()