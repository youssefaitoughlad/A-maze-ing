import time
from os import system


def type_writer(text, delay=0.002):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


amazing_banner = r"""
                         █████╗ ███╗   ███╗ █████╗ ███████╗██╗███╗   ██╗ ██████╗ 
                        ██╔══██╗████╗ ████║██╔══██╗╚══███╔╝██║████╗  ██║██╔════╝ 
                        ███████║██╔████╔██║███████║  ███╔╝ ██║██╔██╗ ██║██║  ███╗
                        ██╔══██║██║╚██╔╝██║██╔══██║ ███╔╝  ██║██║╚██╗██║██║   ██║
                        ██║  ██║██║ ╚═╝ ██║██║  ██║███████╗██║██║ ╚████║╚██████╔╝
                        ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝               


                                    CREATED BY YAIT-OUG & ILHAKAM

"""

intro_lines = [
    "Welcome to the AMAZING PROJECT!",
    "Prepare to witness something extraordinary...",
    "Ideas come alive here, and innovation has no limits.",
    "Let’s embark on this incredible journey together!\n",
    "Loading features...",
    "READY 🚀"
]

goodby_banner = r"""
                     ██████╗ ██╗  ██╗ █████╗ ██╗   ██╗ █████╗ ██████╗ ███████╗██╗  ██╗ █████╗ 
                    ██╔════╝ ██║  ██║██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗
                    ██║  ███╗███████║███████║ ╚████╔╝ ███████║██████╔╝█████╗  ███████║███████║
                    ██║   ██║██╔══██║██╔══██║  ╚██╔╝  ██╔══██║██╔══██╗██╔══╝  ██╔══██║██╔══██║
                    ╚██████╔╝██║  ██║██║  ██║   ██║   ██║  ██║██║  ██║███████╗██║  ██║██║  ██║
                     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
 """

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


show_amazing_banner()
show_goodby_banner()
