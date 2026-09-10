import os
import sys
from colorama import Fore, Style, init

init(autoreset=True)

CYAN = Fore.CYAN
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
WHITE = Fore.WHITE
DIM = Style.DIM
BOLD = Style.BRIGHT
RESET = Style.RESET_ALL

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print()
    print(CYAN + BOLD + "╔══════════════════════════════════════════════════════════╗")
    print(CYAN + BOLD + "║" + WHITE + BOLD + "                         NEXUM                            " + CYAN + BOLD + "║")
    print(CYAN + BOLD + "║" + DIM + WHITE + "                  Local AI Assistant                     " + CYAN + BOLD + "║")
    print(CYAN + BOLD + "╚══════════════════════════════════════════════════════════╝")
    print()

def prompt():
    return input(CYAN + BOLD + "nexum" + MAGENTA + " > " + RESET)

def info(text):
    print(BLUE + "◆ " + WHITE + text)

def success(text):
    print(GREEN + "✓ " + WHITE + text)

def warn(text):
    print(YELLOW + "! " + WHITE + text)

def error(text):
    print(RED + "✗ " + WHITE + text)

def section(text):
    print()
    print(MAGENTA + BOLD + "── " + text + " " + "─" * max(1, 50 - len(text)))
