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
    maze_config = get_dict_config("config.txt")
    height = maze_config.get("height")
    width = maze_config.get("width")
    entry = maze_config.get("entry")
    exit_ = maze_config.get("exit_")
    perfect = maze_config["perfect"]
    seed = maze_config.get("seed", None)


    grid = create_grid(height, width)
    reset_cells(grid)
    generate_maze(grid)
    sp = shortest_path(grid, entry, exit_)
    cord = path_to_coordinate(sp, entry)
    p = input("with path :")
    if p == "1":
        DrawMaze(grid,entry, exit_,True,cord, False)
    else:
        DrawMaze(grid,entry, exit_,True,[], False)
        
def main() -> None:
    try:
        amazing()
    except (Exception, BaseException) as e:
        print(e)



if __name__ == "__main__":
    main()
