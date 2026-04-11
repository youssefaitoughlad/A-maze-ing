from mazegen._42_cells import _42cells
from mazegen._cell import Cell
from enum import Enum
import random
from typing import List, Tuple


class BackGroundColor(Enum):
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


class Colors(Enum):
    WHITE = "\033[89m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


class DrawMaze():
    def __init__(
            self,
            grid: List[List[Cell]],
            entry: Tuple[int, int],
            exit: Tuple[int, int],
            is_reset_cell: bool,
            colored_maze: bool = True
    ) -> None:
        self.grid: List[List[Cell]] = grid
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.is_reset_cell: bool = is_reset_cell
        self.colored_maze: bool = colored_maze
        self.width: int = len(grid[0])
        self.heigth: int = len(grid)
        self.front_color: Colors = self.get_front_color()
        self.back_color: BackGroundColor = self.get_back_color()
        self.draw_maze()

    def get_front_color(self) -> Colors:
        if not self.colored_maze:
            return Colors.WHITE
        colors: List[Colors] = [c for c in Colors if c != Colors.RESET]
        return random.choice(colors)

    def get_back_color(self) -> BackGroundColor:
        colors: List[BackGroundColor] = [c for c in BackGroundColor]
        return random.choice(colors)

    def show_maze_with_colors(self, text: str) -> None:
        print(f"{self.front_color.value}{text}{Colors.RESET.value}")

    def draw_top_line(self, colums: int) -> None:
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
        from time import sleep
        for colums in range(self.heigth):
            sleep(0.02)
            self.draw_top_line(colums)
            sleep(0.02)
            self.draw_midlle_line(colums)
            sleep(0.02)
        self.draw_bottom_line()
