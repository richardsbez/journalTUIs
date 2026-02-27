"""
General statistics screen for the application.
"""

from core.colors import Color
from core.constants import TERMINAL_WIDTH
from ui.utils import clear_screen, create_progress_bar, calculate_stats


def show_general_stats(data: dict) -> None:
    clear_screen()
    WIDTH = TERMINAL_WIDTH

    print(f"\n{Color.MAGENTA_B}{'━' * WIDTH}{Color.RESET}")
    print(
        f"{Color.BOLD}{Color.MAGENTA_B}{'📊 GENERAL STATISTICS'.center(WIDTH)}{Color.RESET}"
    )
    print(f"{Color.MAGENTA_B}{'━' * WIDTH}{Color.RESET}\n")

    _notebook_stats(data)
    _general_summary(data)
    _goals_summary(data)

    print(f"\n{Color.DIM}{'─' * WIDTH}{Color.RESET}")
    input(f"\n{Color.DIM}Press ENTER to go back...{Color.RESET}")


def _notebook_stats(data: dict) -> None:
    print(f"{Color.BOLD}PROGRESS BY NOTEBOOK{Color.RESET}")
    print(f"{Color.DIM}{'─' * TERMINAL_WIDTH}{Color.RESET}\n")

    for notebook in data["notebooks"]:
        total, completed, progress = calculate_stats(data["tasks"], notebook)
        bar = create_progress_bar(progress, 40)
        print(
            f"  {notebook:.<25} {bar}  {progress:>3}%  {Color.DIM}({completed}/{total}){Color.RESET}"
        )
    print()


def _general_summary(data: dict) -> None:
    print(f"{Color.BOLD}GENERAL SUMMARY{Color.RESET}")
    print(f"{Color.DIM}{'─' * TERMINAL_WIDTH}{Color.RESET}\n")

    unique_ids = {t["id"] for t in data["tasks"]}
    total = len(unique_ids)
    completed = sum(
        1 for t in data["tasks"] if t["status"] == "X" and t["id"] in unique_ids
    )

    print(f"  Total tasks: {Color.BOLD}{total}{Color.RESET}")
    print(f"  {Color.GREEN_B}✓{Color.RESET} Completed: {completed}")
    print(f"  {Color.YELLOW_B}○{Color.RESET} Pending: {total - completed}\n")


def _goals_summary(data: dict) -> None:
    print(f"{Color.BOLD}GOALS SUMMARY{Color.RESET}")
    print(f"{Color.DIM}{'─' * TERMINAL_WIDTH}{Color.RESET}\n")

    goals = data.get("goals", {})
    has_goals = False

    for goal_type, label in [
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]:
        lst = goals.get(goal_type, [])
        if lst:
            has_goals = True
            avg = int(sum(g.get("progress", 0) for g in lst) / len(lst))
            bar = create_progress_bar(avg, 30)
            print(f"  {label:.<15} {bar}  {avg:>3}%")

    if not has_goals:
        print(f"  {Color.DIM}No goals registered. Use [M] to create some!{Color.RESET}")
