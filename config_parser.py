from pydantic import BaseModel, Field, ValidationError
from pydantic import model_validator, field_validator
from typing import List, Tuple, Optional, Any
import os
import ast


class ConfigValidate(BaseModel):
    """
    Validated maze configuration model using Pydantic.

    This class defines the structure and validation
    rules for maze configuration
    settings read from a configuration file.

    Attributes:
        width: Number of cells in the maze horizontally (3-30)
        height: Number of cells in the maze vertically (3-30)
        entry: Starting coordinates (x, y) as a tuple
        exit_: Ending coordinates (x, y) as a tuple (underscore to
avoid keyword conflict)
        perfect: If True, maze has exactly one path between
entry and exit
        output_file: File path where maze will be saved
(.txt extension required)
        seed: Random seed for reproducible maze generation (default: 8)

    Raises:
        ValueError: When validation fails for any field or
cross-field constraints
    """
    model_config = {"extra": "forbid"}

    width: int = Field(...)
    height: int = Field(...)
    entry: Tuple[int, int] = Field(...)
    exit_: Tuple[int, int] = Field(...)
    perfect: bool = False
    output_file: str = Field(..., min_length=1, max_length=50)
    seed: Optional[Any] = Field(default=8)

    @field_validator('width', 'height')
    @classmethod
    def grid_validate(cls, v: int) -> int:
        """
        Validate maze dimensions are within acceptable bounds.

        Args:
            v: The dimension value (width or height) to validate

        Returns:
            The validated dimension value

        Raises:
            ValueError:If dimension is less than 3 or greater than 30
        """
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
        """
        Parse and convert coordinate strings to integers before validation.

        This validator runs before the main coordinate validation to ensure
        raw string input is converted to proper integer format.

        Args:
            v: List of coordinate strings (e.g., ['0', '0'])

        Returns:
            List of converted integer coordinates

        Raises:
            ValueError: If coordinates contain non-integer values
        """
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
        """
        Validate that coordinates are non-negative.

        Args:
            v: Tuple of (x, y) coordinates

        Returns:
            The validated coordinate tuple

        Raises:
            ValueError: If any coordinate is negative
        """
        for item in v:
            if item < 0:
                raise ValueError(f"coordinates must be positive, i got {v}")
        return v

    @model_validator(mode='after')
    def entry_exit_validation(self) -> 'ConfigValidate':
        """
        Perform cross-field validation after all individual field validations.

        This validator checks relationships between multiple fields including:
        - Entry and exit coordinates are different
        - Coordinates are within maze bounds
        - Output file has correct extension
        - Output directory exists and is writable
        - Output file is writable if it already exists

        Returns:
            The validated ConfigValidate instance

        Raises:
            ValueError: With all collected error messages
if any validation fails
        """
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
        if directory and not os.path.exists(directory):
            errors.append(f"Directory does not exist: {directory}")

        elif directory and not os.access(directory, os.W_OK):
            errors.append(f"Cannot write to directory: {directory}")

        current_path = "./" + self.output_file
        if os.path.exists(current_path):
            if not os.access(current_path, os.W_OK):
                errors.append(f"Cannot write to file: {self.output_file}")

        if errors:
            raise ValueError("\n".join(errors))
        return self


class ConfigParser:
    """
    Parse and validate maze configuration from a text file.

    This class handles reading a configuration file, parsing KEY=VALUE pairs,
    and validating the configuration using the ConfigValidate model.

    Attributes:
        config: Validated configuration object (ConfigValidate instance)

    Example:
        >>> parser = ConfigParser("config.txt")
        >>> config = parser.get_config()
        >>> print(config.width, config.height)
    """

    def __init__(self, path: str) -> None:
        """
        Initialize ConfigParser and load configuration from file.

        Args:
            path: Path to the configuration file

        Raises:
            FileNotFoundError: If configuration file does not exist
            PermissionError: If file cannot be read due to permissions
            ValueError: If configuration contains invalid values
        """
        self.config: ConfigValidate = self.set_config(path)

    def set_config(self, path: str) -> ConfigValidate:
        """
        Read and parse configuration file into validated model.

        This method orchestrates the entire configuration loading process:
        1. Reads the file
        2. Filters comments and empty lines
        3. Parses KEY=VALUE pairs
        4. Validates and converts values

        Args:
            path: Path to the configuration file

        Returns:
            Validated ConfigValidate object

        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read
            ValueError: For parsing or validation errors
        """
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
                    "line not contain '='"
                )
            splited = line.split('=')
            if len(splited) == 2:
                key, value = splited
                key = key.strip()
                if key in config:
                    raise ValueError(
                        f"Duplicate config key: {key}"
                    )
                config[key] = value.strip()
            else:
                raise ValueError("configs must be with one '='")
        return self.config_key_lower(config)

    def config_key_lower(self, config: dict[str, str]) -> ConfigValidate:
        """
        Convert configuration keys to lowercase and map 'exit' to 'exit_'.

        Args:
            config: Dictionary with original case-sensitive keys

        Returns:
            Validated ConfigValidate object

        Raises:
            ValueError: If any mandatory key is missing
        """
        mandatory_keys = [
            'width', 'height', 'entry', 'exit_', 'output_file', 'perfect'
        ]
        config_l = {}

        for key in config:
            l_key = key.lower()
            if l_key == 'exit':
                l_key += '_'
            config_l[l_key] = config[key]

        for man in mandatory_keys:
            if man not in config_l.keys():
                raise ValueError(f"Missing mandatory config key: {man}")
        return self.convert_values(config_l)

    def convert_values(self, config: dict[str, Any]) -> ConfigValidate:
        """
        Convert string values to appropriate Python types.

        Handles conversions for:
        - Coordinates: "x,y" strings to tuple of ints
        - Perfect flag: "true"/"false" strings to boolean
        - Dimensions: String numbers to integers

        Args:
            config: Dictionary with string values

        Returns:
            Validated ConfigValidate object

        Raises:
            ValueError: For invalid coordinate format,
boolean values, or integers
        """
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
                config[key] = config[key].lower()
                if config[key] in ('true', '1', 'yes'):
                    config[key] = True
                elif config[key] in ('false', '0', 'no'):
                    config[key] = False
                else:
                    raise ValueError(
                        f"perfect must be 'true' or 'false'"
                        f", i got {config[key]}"
                    )
            if key == 'seed':
                try:
                    value = ast.literal_eval(config[key])
                    if isinstance(
                        value, (int, float, bool, str, bytes, bytearray)
                    ):
                        config[key] = value
                except (ValueError, SyntaxError):
                    pass

        int_keys = ['width', 'height']
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

    def get_config(self) -> ConfigValidate:
        """
        Return the validated configuration object.

        Returns:
            ConfigValidate instance containing all configuration values
        """
        return self.config

    def get_dict_config(self) -> dict[str, Any]:
        """
        Return configuration as a dictionary.

        Returns:
            Dictionary representation of the validated configuration
        """
        return self.config.model_dump()


def main() -> None:
    """
    Main entry point for testing the configuration parser.

    Reads 'config.txt' from current directory and prints the parsed
    configuration dictionary to stdout.

    Example:
        $ python config_parser.py
        {'width': 20, 'height': 15, 'entry': (0, 0), ...}
    """
    try:
        _ = ConfigParser("config.txt")
        print(_.get_dict_config())
    except Exception as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    main()
