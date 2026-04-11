from typing import Dict


class Cell:
    """
    Represents a single cell in the maze grid.

    Each cell maintains its coordinates, visitation state for generation
    algorithms, and the status of its four cardinal walls (North, East,
    South, West). A wall value of True means the wall is closed/present,
    while False means the wall is open/removed. External border walls
    must remain closed to ensure maze boundaries are respected.

    Attributes:
        x: Column index of the cell in the maze grid (0 to width-1)
        y: Row index of the cell in the maze grid (0 to height-1)
        visited: Flag used during maze generation (e.g., recursive backtracker)
        walls: Dictionary mapping direction letters to boolean wall states
    """

    def __init__(
            self,
            x: int,
            y: int
            ) -> None:
        self.x: int = x
        self.y: int = y
        self.visited: bool = False
        self.walls: Dict[str, bool] = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }
