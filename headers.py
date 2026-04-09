import time
from pathlib import Path
from os import system


def type_writer(text: str, delay: float = 0.002) -> None:
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


amazing_banner: str = Path("amazing_banner.txt").read_text()

intro_lines: list[str] = [
    "Welcome to the AMAZING PROJECT!",
    "Prepare to witness something extraordinary...",
    "Ideas come alive here, and innovation has no limits.",
    "Let's embark on this incredible journey together!\n",
    "Loading features...",
    "READY 🚀",
]

goodby_banner: str = Path("goodby_banner.txt").read_text()


def show_amazing_banner() -> None:
    system("clear")
    for line in amazing_banner.split("\n"):
        type_writer(line)
    for line in intro_lines:
        type_writer(line, 0.03)


def show_goodby_banner() -> None:
    system('clear')
    for line in goodby_banner.split("\n"):
        type_writer(line)

