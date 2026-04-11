from mazegen.draw_maze import *
from mazegen.generate_maze import *
from mazegen.config_parser import *
from mazegen.headers import *
from typing import Dict, Any
from os import system
import time


def get_dict_config(path: str) -> Dict[str, Any]:
    try:
        parser = ConfigParser(path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Config file not found at '{path}'. "
            f"Please ensure the file exists and the path is correct."
        )
    except PermissionError:
        raise PermissionError(
            f"Permission denied when accessing '{path}'. "
            f"Please check that you have read access to the file."
        )
    except Exception as err:
        raise RuntimeError(
            f"Unexpected error while loading config from '{path}': {err}"
        ) from err

    return parser.get_dict_config()


def amazing() -> None:
    maze_info = get_dict_config("config.txt")
    height = maze_info["height"]
    width = maze_info["width"]
    grid = create_grid(height, width)
    generate_maze(grid)
    DrawMaze(
        grid,
        maze_info["entry"],
        maze_info["exit_"],
        is_reset_cell=True,
        colored_maze=False
    )
    

def main() -> None:
    try:
        amazing()
    except (Exception, BaseException) as e:
        print(e)



if __name__ == "__main__":
    main()
