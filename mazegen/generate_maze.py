from typing import List, Dict, Tuple, Union
from mazegen.draw_maze import DrawMaze
from mazegen._42_cells import reset_cells
from mazegen._cell import Cell
from collections import deque
import random


class MazeGenerator:
    pass


DIRECTIONS = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0)
}

def create_grid(
        height: int,
        width: int
        ) -> List[List[Cell]]:
    return [[Cell(x, y) for x in range(width)] for y in range(height)]


def get_neighbors(
        current_cell: Cell,
        current_grid: List[List[Cell]]
        ) -> Dict[str, Cell]:
    neighbors: Dict[str, Cell] = {}
    height: int = len(current_grid) - 1
    width: int = len(current_grid[0]) - 1

    cell_x, cell_y = current_cell.x, current_cell.y
    if cell_y > 0:
        neighbors["N"] = current_grid[cell_y - 1][cell_x]
    if cell_x < width:
        neighbors["E"] = current_grid[cell_y][cell_x + 1]
    if cell_y < height:
        neighbors["S"] = current_grid[cell_y + 1][cell_x]
    if cell_x > 0:
        neighbors["W"] = current_grid[cell_y][cell_x - 1]

    return neighbors


def remove_wall(cell: Cell, neighbor: Cell) -> None:
    dx = neighbor.x - cell.x
    dy = neighbor.y - cell.y

    if dx == 1:
        cell.walls["E"] = False
        neighbor.walls["W"] = False
    elif dx == -1:
        cell.walls["W"] = False
        neighbor.walls["E"] = False
    elif dy == 1:
        cell.walls["S"] = False
        neighbor.walls["N"] = False
    elif dy == -1:
        cell.walls["N"] = False
        neighbor.walls["S"] = False


def get_unvisited_neighbor(
        current_cell: Cell,
        current_grid: List[List[Cell]]
        )-> Dict[str, Cell]:
    neighbors = get_neighbors(current_cell, current_grid)

    unvisited_neighbors = {}

    for direction, neighbor in neighbors.items():
        if not neighbor.visited:
            unvisited_neighbors[direction] = neighbor

    return unvisited_neighbors

def path_to_coordinate(path, entry):
    coordinates = []
    cell_x, cell_y = entry
    
    for direction in path:
        dx, dy= DIRECTIONS[direction]
        cell_x += dx
        cell_y += dy

        coordinates.append((cell_x, cell_y))
    return coordinates


def reconstruct_path(parent, entry, exit_):
    path = []
    current = exit_

    while current != entry:
        prev, direction = parent[current]
        path.append(direction)
        current = prev

    path.reverse()
    return path


def shortest_path(current_grid, entry, exit_):
    parent = bfs(current_grid, entry, exit_)

    if parent is None:
        return []

    return reconstruct_path(parent, entry, exit_)


def can_move(grid, x, y, direction):
    cell: Cell = grid[y][x]

    if cell.walls[direction]:
        return False
    return True


def bfs(
        current_grid: list[list[Cell]],
        entry,
        exit
        ) -> None:

    queue = deque()
    visited = set()
    parent = {}

    queue.append(entry)
    visited.add(entry)

    while queue:
        cell_x, cell_y = queue.popleft()

        if (cell_x, cell_y) == exit:
            return parent

        for direction in DIRECTIONS:
            if can_move(current_grid, cell_x, cell_y, direction):
                dx, dy = DIRECTIONS[direction]
                nx, ny = dx + cell_x, dy + cell_y

                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = ((cell_x, cell_y), direction)
                    queue.append((nx, ny))

    return None       


def dfs(
        current_cell: Cell, current_grid: list[list[Cell]]
        ) -> Union[Cell, None]:
    current_cell.visited = True
    unvisited_neighbor = get_unvisited_neighbor(current_cell, current_grid)

    if not unvisited_neighbor:
        return None

    neighbor: Cell = random.choice(list(unvisited_neighbor.values()))
    remove_wall(current_cell, neighbor)
    neighbor.visited = True
    
    return neighbor


def generate_maze(current_grid: List[List[Cell]]) -> None:
    start: Cell = current_grid[0][0]
    stack: List[Cell] = [start]

    while stack:
        current_cell = stack[-1]
        next_cell = dfs(current_cell, current_grid)

        if next_cell:
            stack.append(next_cell)
        else:
            stack.pop()


def is_open_square(
        current_grid: List[List[Cell]],
        x: int,
        y: int
        ) -> bool:
    for dy in range(3):
        for dx in range(3):
            current_cell = current_grid[dy + y][dx + x]

            if (
                dx < 2 and current_cell.walls["E"]
                or  dy < 2 and current_cell.walls["N"]
            ):
                return False
    return True


def has_open_square(current_grid: List[List[Cell]]) -> bool:
    heigth: int = len(current_grid)
    width: int = len(current_grid[0])

    for y in range(heigth - 2):
        for x in range(width - 2):
            if is_open_square(current_grid, x, y):
                return True

    return False

def is_fully_closed(cell):
    return all(cell.walls.values())


def break_random_walls(grid):
    for row in grid:
        for cell in row:
            if is_fully_closed(cell):
                continue
            for direction, (dx, dy) in DIRECTIONS.items():
                nx, ny = cell.x + dx, cell.y + dy

                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                    neighbor = grid[ny][nx]

                    if is_fully_closed(neighbor):
                        continue

                    if cell.walls[direction] and random.random() < 0.1:
                        remove_wall(cell, neighbor)

