from pathlib import Path
from os import system
import time


def type_writer(text: str, delay: float = 0.002) -> None:
    """
    Display text with a typewriter animation effect.

    This function prints each character sequentially with a small delay
    between characters, creating a smooth typing animation effect. It's
    used throughout the visual interface to enhance user experience with
    cinematic text rendering. The flush=True ensures each character appears
    immediately without buffering, while the optional delay parameter allows
    adjusting the typing speed for different contexts (e.g., faster for
    menus, slower for dramatic introductions).

    Args:
        text: The string to be displayed with typewriter effect
        delay: Time in seconds between each character (default 0.002 for
               fast typing, use 0.03 for slower dramatic effect)
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


amazing_banner: str = Path(
    "/home/yait-oug/Desktop/A-maze-inesh/amazing_banner.txt"
    ).read_text()

intro_lines: list[str] = [
    "Welcome to the AMAZING PROJECT!",
    "Prepare to witness something extraordinary...",
    "Ideas come alive here, and innovation has no limits.",
    "Let's embark on this incredible journey together!\n",
    "Loading features...",
    "READY 🚀",
]

goodby_banner: str = Path(
    "/home/yait-oug/Desktop/A-maze-inesh/goodby_banner.txt"
    ).read_text()

amazing_menu: list[str] = [
    "\n\033[95m === A-Maze-ing Menu ===\033[0m",
    "1- Regenerate New Maze",
    "2- Change Colors",
    "3- Animate path Finding",
    "4- Quit",
    "\033[95mEnter your choice (1-4) : \033[0m"
]


def show_amazing_banner() -> None:
    """
    Display the animated welcome banner and introduction sequence.

    Clears the terminal screen, then renders the ASCII art banner followed
    by introductory text lines with dramatic typewriter animation. Includes
    a brief pause after the sequence to let the user absorb the welcome
    message before proceeding to the main menu.
    """
    system("clear")
    for line in amazing_banner.split("\n"):
        type_writer(line)
    for line in intro_lines:
        type_writer(line, 0.03)
    time.sleep(2)


def show_goodby_banner() -> None:
    """
    Display the animated farewell banner when exiting the program.

    Clears the terminal and renders the goodbye ASCII art banner with
    typewriter effect, providing a polished exit experience that matches
    the professional presentation of the welcome sequence.
    """
    system('clear')
    for line in goodby_banner.split("\n"):
        type_writer(line)


def show_menu() -> str:
    """
    Render the interactive menu and capture user input.

    Prints each menu item on its own line (excluding the prompt line),
    then displays the colored prompt and returns the user's raw input.
    The separation allows for cleaner formatting and easier modification
    of menu options without changing the input logic.

    Returns:
        Raw user input string from the terminal
    """
    for item in amazing_menu[:-1]:
        print(item)
    return input(amazing_menu[-1])


def get_valid_choice() -> str:
    """
    Get and validate user menu selection with input loop.

    Continuously displays the menu and prompts the user until a valid
    choice (1, 2, 3, or 4) is provided. Invalid inputs trigger an error
    message and re-prompt without crashing, maintaining robustness as
    required by the subject. This function ensures the main program
    only receives valid menu commands.

    Returns:
        Validated choice string: one of '1', '2', '3', or '4'
    """
    while True:
        choice = show_menu().strip()
        if choice in ("1", "2", "3", "4"):
            return choice
        print("Invalid choice. Please enter a number between 1 and 4.")
