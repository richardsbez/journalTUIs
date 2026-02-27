"""
Entry point for the todoTerminal application.
Coordinates the main flow: notebook selection → dashboard → commands.
"""

import sys
import os

# Add root directory to path so relative imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.colors import Color
from core.storage import load_data
from ui.utils import clear_screen
from ui.notebooks import show_notebook_selection
from ui.dashboard import show_interface
from features.tasks import (
    add_task,
    complete_task,
    edit_task,
    delete_task,
    change_priority,
    add_notebook,
    remove_notebook,
    select_notebook,
)
from features.goals import manage_goals
from features.notes import manage_notes
from features.heatmap import log_daily_activity
from features.stats import show_general_stats


def notebook_selection_loop(data: dict) -> bool:
    """
    Runs the notebook selection menu.
    Returns True when a notebook is selected, False to quit.
    """
    while True:
        show_notebook_selection(data)
        cmd = input(f"{Color.CYAN}❯{Color.RESET} ").lower().strip()

        if cmd.isdigit() and select_notebook(data, int(cmd) - 1):
            return True
        elif cmd == "n":
            add_notebook(data)
        elif cmd == "r":
            remove_notebook(data)
        elif cmd == "q":
            _exit_screen()
            return False


def main_loop(data: dict) -> None:
    """Main loop: displays the dashboard and processes commands."""
    COMMANDS = {
        "+": add_task,
        "x": complete_task,
        "e": edit_task,
        "d": delete_task,
        "p": change_priority,
        "n": add_notebook,
        "r": remove_notebook,
        "m": manage_goals,
        "a": manage_notes,
        "h": log_daily_activity,
        "s": show_general_stats,
    }

    while True:
        show_interface(data)
        cmd = input(f"{Color.CYAN}❯{Color.RESET} ").lower().strip()

        if cmd.isdigit():
            select_notebook(data, int(cmd) - 1)

        elif cmd == "c":
            if not notebook_selection_loop(data):
                break

        elif cmd == "q":
            _exit_screen()
            break

        elif cmd in COMMANDS:
            COMMANDS[cmd](data)


def _exit_screen() -> None:
    clear_screen()
    print(f"\n{Color.CYAN_B}{'━' * 60}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN_B}{'👋 See you later!'.center(60)}{Color.RESET}")
    print(
        f"{Color.DIM}{'Your data has been saved successfully.'.center(60)}{Color.RESET}"
    )
    print(f"{Color.CYAN_B}{'━' * 60}{Color.RESET}\n")


def main() -> None:
    data = load_data()
    if notebook_selection_loop(data):
        main_loop(data)


if __name__ == "__main__":
    main()
