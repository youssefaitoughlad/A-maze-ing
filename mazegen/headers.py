from pathlib import Path
from os import system
import time


def type_writer(text: str, delay: float = 0.002) -> None:
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
    system("clear")
    for line in amazing_banner.split("\n"):
        type_writer(line)
    for line in intro_lines:
        type_writer(line, 0.03)
    time.sleep(2)


def show_goodby_banner() -> None:
    system('clear')
    for line in goodby_banner.split("\n"):
        type_writer(line)


def show_menu() -> str:
    for item in amazing_menu[:-1]:
        print(item)
    return input(amazing_menu[-1])


def get_valid_choice() -> str:
    while True:
        choice = show_menu().strip()
        if choice in ("1", "2", "3", "4"):
            return choice
        print("Invalid choice. Please enter a number between 1 and 4.")
