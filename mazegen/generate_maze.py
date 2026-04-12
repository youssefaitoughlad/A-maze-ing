from typing import List, Dict, Tuple, Any, Optional, Set, Deque
from mazegen._42_cells import reset_cells
from mazegen._cell import Cell
from collections import deque
import random


class MazeGenerator():
    DIRECTIONS = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0)
    }

    def __init__(
        self,
        height: int,
        width: int,
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        output_file: str,
        seed: Any,
        perfect: bool = True,
    ) -> None:
        self.height: int = height
        self.width: int = width
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit_
        self.perfect: bool = perfect
        self.output_file: str = output_file
        self.grid = self.create_grid()

        if seed:
            random.seed(seed)

    def create_grid(self) -> List[List[Cell]]:
        return [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
            ]

    def get_neighbors(self, current_cell: Cell) -> Dict[str, Cell]:
        neighbors: Dict[str, Cell] = {}
        height: int = len(self.grid) - 1
        width: int = len(self.grid[0]) - 1

        cell_x, cell_y = current_cell.x, current_cell.y
        if cell_y > 0:
            neighbors["N"] = self.grid[cell_y - 1][cell_x]
        if cell_x < width:
            neighbors["E"] = self.grid[cell_y][cell_x + 1]
        if cell_y < height:
            neighbors["S"] = self.grid[cell_y + 1][cell_x]
        if cell_x > 0:
            neighbors["W"] = self.grid[cell_y][cell_x - 1]

        return neighbors

    def remove_wall(self, cell: Cell, neighbor: Cell) -> None:
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

    def get_unvisited_neighbors(
        self, current_cell: Cell
    ) -> Dict[str, Cell]:
        neighbors = self.get_neighbors(current_cell)

        unvisited_neighbors: Dict[str, Cell] = {}

        for direction, neighbor in neighbors.items():
            if not neighbor.visited:
                unvisited_neighbors[direction] = neighbor

        return unvisited_neighbors

    def path_to_coordinate(self, path: List[str]) -> List[Tuple[int, int]]:
        coordinates: List[Tuple[int, int]] = []
        cell_x, cell_y = self.entry

        for direction in path:
            dx, dy = self.DIRECTIONS[direction]
            cell_x += dx
            cell_y += dy
            coordinates.append((cell_x, cell_y))

        return coordinates

    def reconstruct_path(
        self, parent: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]]
    ) -> List[str]:
        path: List[str] = []
        current: Tuple[int, int] = self.exit

        while current != self.entry:
            prev, direction = parent[current]
            path.append(direction)
            current = prev

        path.reverse()
        return path

    def shortest_path(self) -> List[str]:
        parent: Optional[Dict[Tuple[int, int], Tuple[Tuple[int, int], str]]]
        parent = self.bfs()

        if parent is None:
            return []

        return self.reconstruct_path(parent)

    def can_move(self, x: int, y: int, direction: str) -> bool:
        cell: Cell = self.grid[y][x]
        return not cell.walls[direction]

    def bfs(
        self
    ) -> Optional[Dict[Tuple[int, int], Tuple[Tuple[int, int], str]]]:
        queue: Deque[Tuple[int, int]] = deque()
        visited: Set[Tuple[int, int]] = set()
        parent: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}

        queue.append(self.entry)
        visited.add(self.entry)

        while queue:
            cell_x, cell_y = queue.popleft()

            if (cell_x, cell_y) == self.exit:
                return parent

            for direction in self.DIRECTIONS:
                if self.can_move(cell_x, cell_y, direction):
                    dx, dy = self.DIRECTIONS[direction]
                    nx, ny = dx + cell_x, dy + cell_y

                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = ((cell_x, cell_y), direction)
                        queue.append((nx, ny))

        return None

    def dfs(self, current_cell: Cell) -> Optional[Cell]:
        current_cell.visited = True
        unvisited_neighbors: Dict[str, Cell]
        unvisited_neighbors = self.get_unvisited_neighbors(current_cell)

        if not unvisited_neighbors:
            return None

        neighbor: Cell = random.choice(list(unvisited_neighbors.values()))
        self.remove_wall(current_cell, neighbor)
        neighbor.visited = True

        return neighbor

    def generate_maze(self) -> None:
        reset_cells(self.grid)
        start: Cell = self.grid[0][0]
        stack: List[Cell] = [start]
        while stack:
            current_cell: Cell = stack[-1]
            next_cell: Optional[Cell] = self.dfs(current_cell)

            if next_cell:
                stack.append(next_cell)
            else:
                stack.pop()

        if not self.perfect:
            self.break_random_walls()

    def is_open_square(self, x: int, y: int) -> bool:
        for dy in range(3):
            for dx in range(3):
                current_cell: Cell = self.grid[dy + y][dx + x]

                if (
                    dx < 2 and current_cell.walls["E"]
                    or dy < 2 and current_cell.walls["S"]
                ):
                    return False
        return True

    def has_open_square(self) -> bool:
        height: int = len(self.grid)
        width: int = len(self.grid[0])

        for y in range(height - 2):
            for x in range(width - 2):
                if self.is_open_square(x, y):
                    return True

        return False

    def is_fully_closed(self, cell: Cell) -> bool:
        return all(cell.walls.values())

    def break_random_walls(self) -> None:
        for row in self.grid:
            for cell in row:
                if self.is_fully_closed(cell):
                    continue
                for direction, (dx, dy) in self.DIRECTIONS.items():
                    nx, ny = cell.x + dx, cell.y + dy

                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        neighbor: Cell = self.grid[ny][nx]

                        if self.is_fully_closed(neighbor):
                            continue

                        if cell.walls[direction] and random.random() < 0.1:
                            self.remove_wall(cell, neighbor)
