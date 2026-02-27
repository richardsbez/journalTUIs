"""
Quick notes per notebook.
"""

from core.colors import Color
from core.storage import save_data
from ui.utils import clear_screen


def manage_notes(data: dict) -> None:
    notebook = data["active_notebook"]

    while True:
        clear_screen()
        WIDTH = 80

        print(f"\n{Color.YELLOW_B}{'━' * WIDTH}{Color.RESET}")
        print(
            f"{Color.BOLD}{Color.YELLOW_B}{'📝 QUICK NOTES'.center(WIDTH)}{Color.RESET}"
        )
        print(f"{Color.YELLOW_B}{notebook.upper().center(WIDTH)}{Color.RESET}")
        print(f"{Color.YELLOW_B}{'━' * WIDTH}{Color.RESET}\n")

        note = data["notes"].get(notebook, "")
        _display_note(note, WIDTH)

        print(f"{Color.DIM}{'─' * WIDTH}{Color.RESET}")
        print(
            f"{Color.BOLD}[E]{Color.RESET} Edit  {Color.BOLD}[L]{Color.RESET} Clear  {Color.BOLD}[V]{Color.RESET} Back"
        )
        print(f"{Color.DIM}{'─' * WIDTH}{Color.RESET}\n")

        cmd = input(f"{Color.CYAN}❯{Color.RESET} ").lower().strip()

        if cmd == "e":
            _edit_note(data, notebook)
        elif cmd == "l":
            _clear_note(data, notebook)
        elif cmd == "v":
            break


def _display_note(note: str, width: int) -> None:
    if note:
        print(f"{Color.DIM}┌{'─' * (width - 2)}┐{Color.RESET}")
        for line in note.split("\n"):
            print(
                f"{Color.DIM}│{Color.RESET} {line:<{width - 4}} {Color.DIM}│{Color.RESET}"
            )
        print(f"{Color.DIM}└{'─' * (width - 2)}┘{Color.RESET}\n")
    else:
        print(f"{Color.DIM}  (No notes in this notebook){Color.RESET}\n")


def _edit_note(data: dict, notebook: str) -> None:
    print(f"\n{Color.DIM}Type your notes (empty line to finish):{Color.RESET}\n")
    lines = []
    while True:
        line = input(f"{Color.YELLOW}│{Color.RESET} ")
        if line == "":
            break
        lines.append(line)
    data["notes"][notebook] = "\n".join(lines)
    if save_data(data):
        print(f"\n{Color.GREEN_B}✓ Notes saved!{Color.RESET}")
        input(f"{Color.DIM}Press ENTER...{Color.RESET}")


def _clear_note(data: dict, notebook: str) -> None:
    confirm = input(
        f"\n{Color.YELLOW}Confirm clear notes? (y/n):{Color.RESET} "
    ).lower()
    if confirm == "y":
        data["notes"][notebook] = ""
        save_data(data)
        print(f"{Color.GREEN_B}✓ Notes cleared!{Color.RESET}")
        input(f"{Color.DIM}Press ENTER...{Color.RESET}")
