from typing import List, Dict
from mazegen._cell import Cell


def trs2bits(walls: Dict[str, bool]) -> int:
    """
    Convert a cell's wall dictionary to a hexadecimal-compatible integer.

    This function transforms the boolean wall states (True = closed/present,
    False = open/removed) into a 4-bit integer following the project's
    output specification. The bit order is: South (LSB), West, East, North
    (MSB) - though the function processes in W→S→E→N order to build bits
    correctly from least to most significant.

    The resulting integer (0-15) can be directly formatted as a single
    hexadecimal digit (0-F) in the output file, where each bit position
    corresponds to a specific wall direction as defined in the subject.

    Args:
        walls: Dictionary with keys 'N', 'E', 'S', 'W' mapping to bool
               where True means the wall is closed (bit = 1)

    Returns:
        Integer from 0 to 15 representing the 4-bit wall configuration
    """
    keys = "WSEN"
    bits = 0

    for key in keys:
        bits |= walls[key]
        if key != 'N':
            bits <<= 1
    return bits


def transformer2hex(grid: List[List[Cell]]) -> List[str]:
    """
    Convert a complete maze grid to hexadecimal string representation.

    This function processes each cell in the grid row by row, converting
    each cell's wall configuration to a single hexadecimal digit using
    trs2bits(). The result is a list where each element is a continuous
    hex string for one entire row of the maze.

    The output format matches the project's specification: one hexadecimal
    digit per cell, rows separated by newlines, with no additional spacing
    or delimiters between digits in the same row.

    Args:
        grid: 2D list of Cell objects representing the complete maze

    Returns:
        List of strings, each string containing the hex digits for one row
    """
    output = []

    for row in grid:
        text = ""
        for cell in row:
            text += format(trs2bits(cell.walls), 'X')
        output.append(text)
    return output


def save_output(
        grid: List[List[Cell]],
        entry: tuple[int, int],
        exit_: tuple[int, int],
        path: list[str],
        file_path: str
        ) -> None:
    """
    Write the complete maze output to a file following project specifications.

    This function generates the final output file containing three sections
    as required by the subject: the hexadecimal wall representation of the
    maze grid, followed by an empty line, then the entry and exit coordinates,
    and finally the shortest path from entry to exit using N/E/S/W letters.

    The output format is critical for automated testing (Moulinette) and
    must match exactly: rows of hex digits, blank line, coordinates line,
    path string. All lines end with newline characters as specified.

    Args:
        grid: 2D list of Cell objects representing the maze
        entry: Tuple of (x, y) coordinates for maze entrance
        exit_: Tuple of (x, y) coordinates for maze exit (note underscore
               to avoid conflict with built-in 'exit')
        path: List of direction strings ('N', 'E', 'S', 'W') forming the
              shortest valid path from entry to exit
        file_path: Destination file path where output will be written

    Note:
        The function assumes grid has already been validated and path
        has been computed. It does not perform additional validation
        to keep file I/O operations focused on writing only.
    """

    output = transformer2hex(grid)
    with open(file_path, 'w') as f:
        f.write("\n".join(output))
        f.write("\n\n")
        f.write(",".join([str(c) for c in entry]) + "\n")
        f.write(",".join([str(c) for c in exit_]) + "\n")
        f.write("".join(path) + "\n")
