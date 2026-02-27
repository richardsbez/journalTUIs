"""
Daily activity logging for the weekly heatmap.
"""

from datetime import datetime

from core.colors import Color
from core.constants import SUGGESTED_ACTIVITIES
from core.storage import save_data
from ui.utils import clear_screen, show_feedback


def log_daily_activity(data: dict) -> None:
    clear_screen()
    print(f"\n{Color.CYAN_B}{'━' * 80}{Color.RESET}")
    print(
        f"{Color.BOLD}{Color.CYAN_B}{"🔥 LOG TODAY'S ACTIVITIES".center(80)}{Color.RESET}"
    )
    print(f"{Color.CYAN_B}{'━' * 80}{Color.RESET}\n")

    today = datetime.now()
    key = today.strftime("%Y-%m-%d")
    data["daily_activities"].setdefault(key, {"activities": {}, "level": 0})
    record = data["daily_activities"][key]

    _list_activities(record)

    choice = input(f"\n{Color.CYAN}❯{Color.RESET} ").strip()
    if not choice:
        return

    activity = _resolve_activity(choice)
    if not activity:
        return

    record["activities"][activity] = record["activities"].get(activity, 0) + 1
    record["level"] = _calculate_level(sum(record["activities"].values()))

    if save_data(data):
        total = sum(record["activities"].values())
        show_feedback(f"✓ {activity} logged! Today's total: {total}", "success")


def _list_activities(record: dict) -> None:
    print(f"{Color.BOLD}SUGGESTED ACTIVITIES:{Color.RESET}")
    print(f"{Color.DIM}{'─' * 80}{Color.RESET}\n")

    for i, name in enumerate(SUGGESTED_ACTIVITIES, 1):
        count = record["activities"].get(name, 0)
        status = (
            f"{Color.GREEN_B}✓ {count}x{Color.RESET}"
            if count > 0
            else f"{Color.DIM}○{Color.RESET}"
        )
        print(f"  {i}. {status} {name}")

    print(f"\n  {Color.BOLD}0.{Color.RESET} Custom activity")
    print(f"\n{Color.DIM}{'─' * 80}{Color.RESET}")
    print(f"{Color.BOLD}Enter the activity number (or Enter to go back):{Color.RESET}")


def _resolve_activity(choice: str) -> str | None:
    try:
        idx = int(choice)
        if idx == 0:
            custom = input(f"\n{Color.CYAN}Activity name:{Color.RESET} ").strip()
            return custom if custom else None
        elif 1 <= idx <= len(SUGGESTED_ACTIVITIES):
            return SUGGESTED_ACTIVITIES[idx - 1]
        else:
            show_feedback("Invalid number!", "error")
            return None
    except ValueError:
        show_feedback("Invalid input!", "error")
        return None


def _calculate_level(total: int) -> int:
    if total == 0:
        return 0
    if total <= 2:
        return 1
    if total <= 4:
        return 2
    if total <= 6:
        return 3
    return 4
