from mazegen.draw_maze import *
from mazegen.generate_maze import *
from mazegen.config_parser import *
from mazegen.headers import *
from enum import Enum
from typing import Dict, Any
from os import system
import time


class Amazing():
    pass


class MenuChoice(Enum):
    GENERATE = "1"
    COLORS = "2"
    ANIMATE = "3"
    QUIT = "5"


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


def show_maze(maze, entry, exit_, is_reset_call ,path=None, animate=False):
    cord = maze.path_to_coordinate(path) if path else []
    DrawMaze(maze.grid, entry, exit_, is_reset_call, cord, animate)


def build_maze(height, width, entry, exit_, seed, perfect):
    maze = MazeGenerator(height, width, entry, exit_, "maze.txt", seed, perfect)
    maze.generate_maze()
    path = maze.shortest_path()
    return maze, path


def amazing() -> None:
    maze_config = get_dict_config("config.txt")
    height  = maze_config.get("height")
    width   = maze_config.get("width")
    entry   = maze_config.get("entry")
    exit_   = maze_config.get("exit_")
    perfect = maze_config.get("perfect")
    seed    = maze_config.get("seed")

    
    # show_amazing_banner()
    system('clear')
    maze, path = build_maze(height, width, entry, exit_, seed, perfect)
    show_maze(maze, entry, exit_, True, [])
    choice = show_menu()
    path_visible = True
    animate = False
    while True:
        system('clear')
        match choice:
            case MenuChoice.GENERATE.value:
                maze, path = build_maze(height, width, entry, exit_, seed, perfect)
                show_maze(maze, entry, exit_, True, [])
            case MenuChoice.COLORS.value:
                system('clear')
                animate = True
                show_maze(maze, entry, exit_, True, [], animate)
            case MenuChoice.ANIMATE.value:
                system('clear')
                if path_visible:
                    show_maze(maze, entry, exit_, True, path, animate)
                else:
                    show_maze(maze, entry, exit_, True, [], animate)
                path_visible = not path_visible
            case MenuChoice.QUIT.value:
                system('clear')
                show_goodby_banner()
                break
            case _:
                system('clear')
                raise ValueError(
                    "Invalid choice "
                )
        choice = show_menu()

def main() -> None:
    try:
        amazing()
    except (Exception, BaseException) as e:
        print(e)



if __name__ == "__main__":
    main()

