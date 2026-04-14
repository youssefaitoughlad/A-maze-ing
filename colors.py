from enum import Enum
from typing import List
import random


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


def get_front_color(colored_maze: bool = True) -> Colors:
    """
    Returns a random foreground color or white
    if colored mode is disabled.
    """
    if not colored_maze:
        return Colors.WHITE
    colors: List[Colors] = [c for c in Colors if c != Colors.RESET]
    return random.choice(colors)


def get_back_color() -> BackGroundColor:
    """
    Returns a random background color
    for highlighting the '42' pattern.
    """
    colors: List[BackGroundColor] = [c for c in BackGroundColor]
    return random.choice(colors)
