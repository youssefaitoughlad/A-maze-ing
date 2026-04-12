from mazegen.draw_maze import *
from mazegen.generate_maze import *
from mazegen.config_parser import *
from mazegen.headers import *
from mazegen.maze2hex import *
from mazegen.colors import *
from enum import Enum
from typing import Dict, Any
from os import system


class MenuChoice(Enum):
    GENERATE   = "1"
    COLORS     = "2"
    ANIMATE    = "3"
    QUIT       = "4"


class Amazing:
    def __init__(self, config_path: str = "config.txt"):
        config         = self._load_config(config_path)
        self.height    = config.get("height")
        self.width     = config.get("width")
        self.entry     = config.get("entry")
        self.exit_     = config.get("exit_")
        self.perfect   = config.get("perfect")
        self.seed      = config.get("seed")
        self.output_file = config.get("output_file")
        self.config_path: str = config_path
        self.maze      = None
        self.path      = None
        self.animate   = False
        self.path_visible = False
        self.front_color: Colors = get_front_color(False)
        self.back_color: BackGroundColor = get_back_color()

    def _load_config(self, path: str) -> Dict[str, Any]:
        try:
            return ConfigParser(path).get_dict_config()
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
                f"Unexpected error while loading config from '{path}': {str(err).strip('Value error, ')}"
            ) from err

    def _build_maze(self):
        self.maze = MazeGenerator(
            self.height, self.width, self.entry,
            self.exit_, self.config_path, self.seed, self.perfect
        )
        self.maze.generate_maze()
        self.path = self.maze.shortest_path()
        save_output(self.maze.grid, self.entry, self.exit_, self.path, self.output_file)

    def _show_maze(self, is_reset: bool, show_path: bool = False):
        cord = self.maze.path_to_coordinate(self.path) if show_path else []
        DrawMaze(self.maze.grid, self.entry, self.exit_, is_reset, cord, self.front_color, self.back_color, self.animate)

    def _handle_generate(self):
        self.back_color = get_back_color()
        self._build_maze()
        self._show_maze(is_reset=True, show_path=self.path_visible)

    def _handle_colors(self):
        self.back_color = get_back_color()
        self.front_color = get_front_color() if self.animate else get_front_color(False)
        self.animate = True
        self._show_maze(is_reset=True, show_path=self.path_visible)

    def _handle_animate(self):
        self.path_visible = not self.path_visible
        self._show_maze(is_reset=True, show_path=self.path_visible)


    def run(self) -> None:
        system('clear')
        self._build_maze()
        self._show_maze(is_reset=True)
        choice = show_menu()

        while True:
            system('clear')
            match choice:
                case MenuChoice.GENERATE.value:
                    self._handle_generate()
                case MenuChoice.COLORS.value:
                    self._handle_colors()
                case MenuChoice.ANIMATE.value:
                    self._handle_animate()
                case MenuChoice.QUIT.value:
                    show_goodby_banner()
                    break
                case _:
                    raise ValueError(
                        "Invalid menu choice. Please select a valid option from the menu."
                        )


def main() -> None:
    try:
        Amazing().run()
    except (Exception, BaseException) as e:
        print(e)


if __name__ == "__main__":
    main()
