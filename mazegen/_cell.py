from typing import Dict, List, Tuple


class Cell:
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
