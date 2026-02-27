"""
ANSI color module for the terminal.
Centralizes all formatting constants used in the application.
"""


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Text colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors
    RED_B = "\033[91m"
    GREEN_B = "\033[92m"
    YELLOW_B = "\033[93m"
    BLUE_B = "\033[94m"
    MAGENTA_B = "\033[95m"
    CYAN_B = "\033[96m"

    # Backgrounds
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_GRAY = "\033[100m"
