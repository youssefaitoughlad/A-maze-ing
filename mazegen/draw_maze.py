from mazegen._42_cells import _42cells
from mazegen._cell import Cell
from enum import Enum
import random
from typing import List, Tuple


class BackGroundColor(Enum):
    """
    ANSI color codes for terminal background colors
    used in maze visualization.
    """
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


class Colors(Enum):
    """
    ANSI color codes for terminal foreground colors
    used in maze visualization.
    """
    WHITE = "\033[89m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


class DrawMaze():
    """
    Renders a visual ASCII representation of the generated maze
    in the terminal.

    This class provides a complete visualization system that displays walls,
    entry/exit points, and the required "42" pattern. It supports both colored
    and monochrome rendering modes, with random color selection for walls
    when colored mode is enabled. The rendering follows the project's
    requirement that all external borders must show closed walls, and corridors
    are visually represented with proper wall connections.

    Key Features:
    - Displays maze walls using ASCII characters (●, ║, ===, spaces)
    - Highlights entry point with baby emoji (👶) and exit with bottle emoji (🍼)
    - Visually distinguishes the "42" pattern cells using background colors
    - Optional random color cycling for walls (change during interactive mode)
    - Respects maze boundaries with closed external walls

    The visual output matches the project specification where each cell
    shows its north, east, south, and west walls. The rendering includes
    proper alignment and spacing to ensure the maze structure is clearly
    readable and the "42" pattern is visibly identifiable.

    Attributes:
        grid: 2D list of Cell objects representing the complete maze structure
        entry: (x, y) coordinates of the maze entrance point
        exit: (x, y) coordinates of the maze exit point
        is_reset_cell: Flag indicating whether to highlight
the "42" pattern cells
        colored_maze: Enables/disables colored rendering
(True = colored, False = monochrome)
        width: Number of columns in the maze grid
        height: Number of rows in the maze grid
        front_color: Randomly selected ANSI color code for walls and text
        back_color: Randomly selected ANSI background color for
"42" pattern cells
    """
    def __init__(
            self,
            grid: List[List[Cell]],
            entry: Tuple[int, int],
            exit_: Tuple[int, int],
            is_reset_cell: bool,
            path: List[str],
            colored_maze: bool = True
    ) -> None:
        self.grid: List[List[Cell]] = grid
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit_
        self.is_reset_cell: bool = is_reset_cell
        self.path: List[str] = path
        self.colored_maze: bool = colored_maze
        self.width: int = len(grid[0])
        self.heigth: int = len(grid)
        self.front_color: Colors = self.get_front_color()
        self.back_color: BackGroundColor = self.get_back_color()
        self.draw_maze()

    def get_front_color(self) -> Colors:
        """
        Returns a random foreground color or white
        if colored mode is disabled.
        """
        if not self.colored_maze:
            return Colors.WHITE
        colors: List[Colors] = [c for c in Colors if c != Colors.RESET]
        return random.choice(colors)

    def get_back_color(self) -> BackGroundColor:
        """
        Returns a random background color
        for highlighting the '42' pattern.
        """
        colors: List[BackGroundColor] = [c for c in BackGroundColor]
        return random.choice(colors)

    def show_maze_with_colors(self, text: str) -> None:
        """
        Prints text with the current foreground color
        and resets afterward.
        """
        print(f"{self.front_color.value}{text}{Colors.RESET.value}")

    def draw_top_line(self, colums: int) -> None:
        """
        Draws the top border line for a row of cells
    including north walls.

        Args:
            colums: The row index being rendered (y-coordinate)
        """
        top_line: str = ""
        for y in range(self.width):
            top_line += "●"
            top_line += "====" if self.grid[colums][y].walls["N"] else "    "
        top_line += "●"
        if self.colored_maze:
            self.show_maze_with_colors(top_line)
        else:
            print(top_line)

    def draw_midlle_line(self, colums: int) -> None:
        """
        Draws the middle section of a cell row including
west/east walls and markers.

        Renders two lines per cell row to properly display
vertical walls and
        special markers for entry (👶), exit (🍼), and
the "42" pattern background.

        Args:
            colums: The row index being rendered (y-coordinate)
        """
        for i in range(2):
            middle_line: str = ""
            for y in range(self.width):
                middle_line += "║" if self.grid[colums][y].walls["W"] else " "
                if (
                    self.is_reset_cell
                    and ((y, colums) in _42cells(self.width, self.heigth))
                ):
                    middle_line += self.back_color.value + "    "
                    middle_line += "\033[0m" + self.front_color.value
                elif (y, colums) == self.entry and i == 1:
                    middle_line += "👶" + self.front_color.value
                    middle_line += "  " + self.front_color.value
                elif (y, colums) == self.exit and i == 1:
                    middle_line += " 🍼" + self.front_color.value
                    middle_line += " " + self.front_color.value
                elif (y, colums) in self.path and i == 1 and (y, colums) != self.entry:
                    middle_line += "\033[95m" + " *  " + "\033[0m" + self.front_color.value 
                else:
                    middle_line += "    " + self.front_color.value

            if self.grid[colums][self.width - 1].walls["E"]:
                middle_line += "║"
            else:
                middle_line += " "
            if self.colored_maze:
                self.show_maze_with_colors(middle_line)
            else:
                print(middle_line)

    def draw_bottom_line(self) -> None:
        """
        Draws the bottom border line
        of the entire maze including south walls.
        """
        bottom_line: str = ""
        for rows in range(self.width):
            bottom_line += "●"
            if self.grid[self.heigth - 1][rows].walls["S"]:
                bottom_line += "===="
            else:
                bottom_line += "    "
        bottom_line += "●"

        if self.colored_maze:
            self.show_maze_with_colors(bottom_line)
        else:
            print(bottom_line)

    def draw_maze(self) -> None:
        """
        Renders the complete maze with animated drawing effect.

        Draws row by row with small delays (0.02 seconds) between each line
        to create a progressive building animation effect. The rendering
        includes all walls, entry/exit markers, and the "42" pattern highlight.
        """
        from time import sleep
        for colums in range(self.heigth):
            self.draw_top_line(colums)
            self.draw_midlle_line(colums)
        self.draw_bottom_line()
