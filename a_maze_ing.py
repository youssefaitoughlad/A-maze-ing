from mazegen.draw_maze import DrawMaze
from mazegen.generate_maze import MazeGenerator
from mazegen.config_parser import ConfigParser
from mazegen.headers import show_menu, show_goodby_banner, show_amazing_banner
from mazegen.maze2hex import save_output
from mazegen.colors import Colors, BackGroundColor
from mazegen.colors import get_front_color, get_back_color
from typing import Dict, Any, List, Tuple
from enum import Enum
from os import system


class MenuChoice(Enum):
    """Enumeration of available interactive menu options."""
    GENERATE = "1"
    ANIMATE = "2"
    COLORS = "3"
    QUIT = "4"


class Amazing:
    """
    Main application controller for the A-Maze-ing project.

    This class orchestrates the complete maze generation and visualization
    system, handling configuration loading, maze generation, output file
    writing, and interactive user interface management. It serves as the
    central coordinator between the generator, renderer, and UI components.

    The class implements the required interactive features including maze
    regeneration, color customization, path visibility toggling, and proper
    cleanup on exit. It maintains application state across user interactions
    such as current maze instance, path visibility status, and color schemes.

    Error handling is comprehensive as required by the subject: configuration
    file errors, permission issues, and unexpected exceptions are caught and
    presented as clear user-friendly messages without crashing the program.

    Attributes:
        height: Number of rows in the maze grid (Y dimension)
        width: Number of columns in the maze grid (X dimension)
        entry: Tuple of (x, y) coordinates for maze entrance
        exit_: Tuple of (x, y) coordinates for maze exit
(underscore avoids built-in)
        perfect: Boolean flag for perfect maze generation (True = unique path)
        seed: Random seed string for reproducible generation
        output_file: Destination file path for maze output
        config_path: Path to the configuration file
        maze: Current MazeGenerator instance or None if not yet generated
        path: List of direction strings representing shortest path
from entry to exit
        animate: Flag enabling animated path finding visualization
        path_visible: Flag indicating whether solution path is currently
displayed
        front_color: Current foreground color for maze rendering
        back_color: Current background color for maze rendering
    """

    def __init__(self, config_path: str = "config.txt") -> None:
        """
        Initialize the Amazing application with configuration.

        Loads maze parameters from the specified configuration file and
        initializes application state with default values. All configuration
        values are validated during parsing; missing or invalid values trigger
        appropriate error messages.

        Args:
            config_path: Path to the configuration file (default: "config.txt")

        Raises:
            FileNotFoundError: If config file doesn't exist
            PermissionError: If config file can't be read due to permissions
            RuntimeError: For other configuration parsing errors
        """
        config: Dict[str, Any] = self._load_config(config_path)
        self.height: int = int(config.get("height", 0))
        self.width: int = int(config.get("width", 0))
        self.entry: Tuple[int, int] = tuple(config.get("entry", (0, 0)))
        self.exit_: Tuple[int, int] = tuple(config.get("exit_", (0, 0)))
        self.perfect: bool = bool(config.get("perfect", True))
        self.seed: str = config.get("seed", "")
        self.output_file: str = str(config.get("output_file", ""))
        self.config_path: str = config_path
        self.maze: MazeGenerator | None = None
        self.path: List[str] = []
        self.animate: bool = False
        self.path_visible: bool = False
        self.front_color: Colors = get_front_color(False)
        self.back_color: BackGroundColor = get_back_color()

    def _load_config(self, path: str) -> Dict[str, Any]:
        """
        Load and parse the configuration file
with comprehensive error handling.

        Attempts to read the configuration file using ConfigParser and returns
        the parsed dictionary. Different exception types are caught and
        re-raised with user-friendly messages that clearly explain the issue
        without exposing internal implementation details.

        Args:
            path: Path to the configuration file to load

        Returns:
            Dictionary containing configuration key-value pairs

        Raises:
            FileNotFoundError: If the specified file does not exist
            PermissionError: If read permissions are insufficient
            RuntimeError: For any other unexpected error during parsing
        """
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
                f"Unexpected error while loading config from '{path}':"
                f"{err}"
            ) from err

    def _build_maze(self) -> None:
        """
        Generate a new maze using current configuration parameters.

        Creates a MazeGenerator instance with the current maze dimensions,
        entry/exit points, and perfection setting. Executes the generation
        algorithm, computes the shortest path, and saves the output to the
        specified file format. Updates the internal maze reference and path
        cache for subsequent display operations.
        """
        self.maze = MazeGenerator(
            self.height, self.width, self.entry,
            self.exit_, self.config_path, self.seed, self.perfect
        )
        self.maze.generate_maze()
        self.path = self.maze.shortest_path()
        save_output(
            self.maze.grid,
            self.entry,
            self.exit_,
            self.path,
            self.output_file
        )

    def _show_maze(self, is_reset: bool, show_path: bool = False) -> None:
        """
        Render the current maze with optional path highlighting.

        Converts the path direction list to absolute coordinates if path
        display is requested, then delegates to DrawMaze for terminal
        rendering. The is_reset parameter controls whether the display
        should clear previous content before drawing.

        Args:
            is_reset: If True, clears terminal before drawing the maze
            show_path: If True, highlights the solution path in the display
        """
        if self.maze is None:
            return

        cord: List[Tuple[int, int]]
        cord = self.maze.path_to_coordinate(self.path) if show_path else []
        DrawMaze(
            self.maze.grid,
            self.entry,
            self.exit_,
            is_reset,
            cord,
            self.front_color,
            self.back_color,
            self.animate
        )

    def _handle_generate(self) -> None:
        """Handle 'Generate New Maze' menu option."""
        self.back_color = get_back_color()
        self._build_maze()
        self._show_maze(is_reset=True, show_path=self.path_visible)

    def _handle_colors(self) -> None:
        """
        Handle 'Change Colors' menu option with
        animation state preservation.
        """
        self.back_color = get_back_color()
        if self.animate:
            self.front_color = get_front_color()
        else:
            self.front_color = get_front_color(False)
        self.animate = True
        self._show_maze(is_reset=True, show_path=self.path_visible)

    def _handle_animate(self) -> None:
        """Toggle solution path visibility on/off."""
        self.path_visible = not self.path_visible
        self._show_maze(is_reset=True, show_path=self.path_visible)

    def run(self) -> None:
        """
        Main application loop handling user interaction.

        Displays the welcome banner, generates the initial maze, then enters
        the interactive menu loop. Processes user choices by delegating to
        appropriate handlers, updates the display accordingly, and continues
        until the user selects quit, at which point the goodbye banner is
        shown and the application exits cleanly.

        The menu loop uses structural pattern matching (Python 3.10+) to
        handle different menu choices elegantly. All exceptions during
        execution are caught at the top level to prevent crashes.
        """
        system('clear')
        show_amazing_banner()
        system('clear')
        self._build_maze()
        self._show_maze(is_reset=True)
        choice = show_menu().strip()

        while True:
            system('clear')
            match choice:
                case MenuChoice.GENERATE.value:
                    self._handle_generate()
                case MenuChoice.ANIMATE.value:
                    self._handle_animate()
                case MenuChoice.COLORS.value:
                    self._handle_colors()
                case MenuChoice.QUIT.value:
                    show_goodby_banner()
                    break
                case _:
                    raise ValueError(
                        "Invalid menu choice, "
                        "Please select a valid option from the menu."
                        )
            choice = show_menu().strip()


def main() -> None:
    """
    Entry point for the A-Maze-ing application.

    Initializes and runs the Amazing application, catching any exceptions
    that bubble up from the main loop to prevent raw traceback dumps.
    Prints user-friendly error messages instead of crashing unexpectedly,
    as required by the project specifications for robust error handling.
    """
    try:
        Amazing().run()
    except (Exception, KeyboardInterrupt, BaseException) as e:
        if isinstance(e, KeyboardInterrupt):
            print("\033[91mError: ctrl+c is invalid choice!!!\033[0m")
        else:
            print(f"\033[91mError: {e}\033[0m")
        # import sys
        # sys.exit(1)


if __name__ == "__main__":
    main()
