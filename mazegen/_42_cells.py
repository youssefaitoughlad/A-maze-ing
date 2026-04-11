from typing import List, Tuple
from mazegen._cell import Cell


def _42cells(
        maze_width: int,
        maze_height: int
    ) -> List[Tuple[int, int]]:

    half_maze_width = (maze_width // 2)
    cells = [
        (half_maze_width + 2, half_maze_width - 2),
        (half_maze_width + 1, half_maze_width - 2),
        (half_maze_width + 3, half_maze_width - 2),
        (half_maze_width + 3, half_maze_width - 1),
        (half_maze_width + 3, half_maze_width),
        (half_maze_width + 2, half_maze_width),
        (half_maze_width + 1, half_maze_width),
        (half_maze_width + 1, half_maze_width + 1),
        (half_maze_width + 1, half_maze_width + 2),
        (half_maze_width + 2, half_maze_width + 2),
        (half_maze_width + 3, half_maze_width + 2),
        \
        (half_maze_width - 3, half_maze_width - 2),
        (half_maze_width - 3, half_maze_width - 1),
        (half_maze_width - 3, half_maze_width),
        (half_maze_width - 2, half_maze_width),
        (half_maze_width - 1, half_maze_width),
        (half_maze_width - 1, half_maze_width + 1),
        (half_maze_width - 1, half_maze_width + 2)
    ]
    return cells


def reset_cells(current_grid: List[List[Cell]]) -> None:
    height = len(current_grid)
    width = len(current_grid[0])

    cells_42 = _42cells(width, height)
    for cells_in_grid in current_grid:
        for cell in cells_in_grid:
            x, y = cell.x, cell.y
            cell.visited = False
            if (x, y) in cells_42:
                cell.visited = True
