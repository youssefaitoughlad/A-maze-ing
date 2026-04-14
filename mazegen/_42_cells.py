from typing import List, Tuple
from mazegen._cell import Cell


def _42cells(
        maze_width: int,
        maze_height: int
) -> List[Tuple[int, int]]:
    """
    Returns the coordinates of cells that form
the visible "42" pattern in the maze.

    This function calculates and returns a list of
cell coordinates that together
    create a visually recognizable "42" pattern when rendered with special
    highlighting. The pattern is placed approximately at the center of the maze
    and consists of fully closed cells (all four walls present) that stand out
    visually from the surrounding paths.

    The pattern coordinates are calculated relative to the maze's center point
    (half_maze_width). The function pre-defines specific offset positions that
    form the shapes of digits '4' and '2' using 2x2 or 3x2 block formations.
    These cells must have all walls closed (N, E, S, W all True) to create the
    visual effect required by the project specification.

    Args:
        maze_width: Total number of columns in
the maze grid (WIDTH from config)
        maze_height: Total number of rows in
the maze grid (HEIGHT from config)

    Returns:
        List of (x, y) coordinate tuples representing cells
that belong to the "42" pattern.
        Each coordinate is valid within
the maze bounds (assumes caller validates size).
    """
    maze_height = maze_height * 1
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
    """
    Resets the visited status of all cells and marks
"42" pattern cells as visited.

    This function performs two critical operations for maze generation and
    visualization:

    1. Resets the `visited` flag to False for every cell in the grid, clearing
       any state from previous generation attempts or algorithms.

    2. Sets `visited = True` specifically for cells belonging to
the "42" pattern.
       This ensures pattern cells are treated as already-visited
       during generation,
       preventing the algorithm from opening walls within the pattern and
       maintaining their fully-closed state.

    The "42" pattern must consist of completely closed cells to be visible in
    the final output. By marking these cells as visited
before generation begins,
    the maze generation algorithm (e.g., recursive backtracker)
will not attempt
    to carve passages through them, preserving all four walls.

    Args:
        current_grid: 2D list of Cell objects representing
the current maze state.
        Modified in-place; visited flags are updated for all cells.
    """
    height = len(current_grid)
    width = len(current_grid[0])

    cells_42 = _42cells(width, height)
    for cells_in_grid in current_grid:
        for cell in cells_in_grid:
            x, y = cell.x, cell.y
            cell.visited = False
            if (x, y) in cells_42:
                cell.visited = True
