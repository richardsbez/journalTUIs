"""
Goal management: weekly, monthly, yearly and calendar.
"""

import calendar
from datetime import datetime

from core.colors import Color
from core.constants import MONTHS_LIST
from core.storage import save_data
from ui.utils import clear_screen, create_progress_bar, show_feedback


def manage_goals(data: dict) -> None:
    if "goals" not in data:
        data["goals"] = {"weekly": [], "monthly": [], "yearly": []}

    current_type = "weekly"
    selected_month = datetime.now().month

    while True:
        clear_screen()
        _goals_header()
        _render_tabs(current_type)

        if current_type == "calendar":
            _render_calendar(data)
        elif current_type == "monthly":
            selected_month = _render_monthly(data, selected_month)
        else:
            _render_goals_list(data["goals"].get(current_type, []), current_type)

        _goals_menu(current_type)
        cmd = input(f"{Color.CYAN}❯{Color.RESET} ").lower().strip()

        # Month navigation
        if current_type == "monthly":
            if cmd in ["<", "←"]:
                selected_month = selected_month - 1 if selected_month > 1 else 12
                continue
            elif cmd in [">", "→"]:
                selected_month = selected_month + 1 if selected_month < 12 else 1
                continue

        # Switch tab
        if cmd == "1":
            current_type = "weekly"
        elif cmd == "2":
            current_type = "monthly"
        elif cmd == "3":
            current_type = "yearly"
        elif cmd == "4":
            current_type = "calendar"
        elif cmd == "v":
            break
        elif current_type == "calendar":
            _handle_calendar(data, cmd)
        elif cmd == "+":
            _add_goal(data, current_type, selected_month)
        elif cmd == "e":
            _edit_goal(data, current_type, selected_month)
        elif cmd == "u":
            _update_progress(data, current_type, selected_month)
        elif cmd == "d":
            _delete_goal(data, current_type, selected_month)


# ─── Rendering ───────────────────────────────────────────────────────────────


def _goals_header() -> None:
    print(f"\n{Color.MAGENTA_B}{'━' * 100}{Color.RESET}")
    print(f"{Color.BOLD}{Color.MAGENTA_B}{'🎯 GOALS MANAGER'.center(100)}{Color.RESET}")
    print(f"{Color.MAGENTA_B}{'━' * 100}{Color.RESET}\n")


def _render_tabs(current_type: str) -> None:
    tabs = []
    for t in ["weekly", "monthly", "yearly", "calendar"]:
        name = "CALENDAR" if t == "calendar" else t.upper()
        if t == current_type:
            tabs.append(f"{Color.BG_BLUE}{Color.WHITE} {name} {Color.RESET}")
        else:
            name_inactive = "Calendar" if t == "calendar" else t.capitalize()
            tabs.append(f"{Color.DIM}[{name_inactive}]{Color.RESET}")
    print("  " + "   ".join(tabs))
    print(f"\n{Color.DIM}{'─' * 100}{Color.RESET}\n")


def _render_goals_list(goals: list, goal_type: str) -> None:
    if not goals:
        print(f"{Color.DIM}  No {goal_type[:-2]} goals registered.{Color.RESET}\n")
        return

    for idx, goal in enumerate(goals, 1):
        _print_goal(idx, goal)


def _render_monthly(data: dict, selected_month: int) -> int:
    print(
        f"{Color.BOLD}{Color.MAGENTA_B}📅 {MONTHS_LIST[selected_month - 1].upper()}{Color.RESET}"
    )
    print(f"{Color.DIM}{'─' * 100}{Color.RESET}\n")

    current_month = datetime.now().month
    nav = []
    for i, name in enumerate(MONTHS_LIST, 1):
        if i == selected_month:
            nav.append(f"{Color.BG_BLUE}{Color.WHITE} {name[:3]} {Color.RESET}")
        elif i == current_month:
            nav.append(f"{Color.CYAN_B}{name[:3]}{Color.RESET}")
        else:
            nav.append(f"{Color.DIM}{name[:3]}{Color.RESET}")

    print("  " + "  ".join(nav[:6]))
    print("  " + "  ".join(nav[6:]))
    print(f"\n{Color.DIM}Use < and > to navigate between months{Color.RESET}")
    print(f"{Color.DIM}{'─' * 100}{Color.RESET}\n")

    month_name = MONTHS_LIST[selected_month - 1]
    month_goals = [
        (i, g)
        for i, g in enumerate(data["goals"].get("monthly", []))
        if month_name in g.get("text", "")
    ]

    if not month_goals:
        print(f"{Color.DIM}  No goals for {month_name}.{Color.RESET}\n")
    else:
        for display_idx, (_, goal) in enumerate(month_goals, 1):
            highlight = (
                f" {Color.CYAN_B}⭐ CURRENT MONTH{Color.RESET}"
                if selected_month == datetime.now().month
                else ""
            )
            _print_goal(display_idx, goal, highlight)

    return selected_month


def _print_goal(idx: int, goal: dict, highlight: str = "") -> None:
    text = goal.get("text", "")
    prog = goal.get("progress", 0)
    bar = create_progress_bar(prog, 40)
    if goal.get("type") == "current_week" and not highlight:
        highlight = f" {Color.CYAN_B}⭐ CURRENT WEEK{Color.RESET}"
    print(f"  {Color.BOLD}{idx}.{Color.RESET} {text}{highlight}")
    print(f"     {bar}  {Color.BOLD}{prog}%{Color.RESET}\n")


def _goals_menu(current_type: str) -> None:
    print(f"{Color.DIM}{'─' * 100}{Color.RESET}")
    print(f"{Color.BOLD}COMMANDS:{Color.RESET}")
    print(
        f"  {Color.BOLD}[1]{Color.RESET} Weekly  {Color.BOLD}[2]{Color.RESET} Monthly  {Color.BOLD}[3]{Color.RESET} Yearly  {Color.BOLD}[4]{Color.RESET} Calendar"
    )
    if current_type != "calendar":
        print(
            f"  {Color.BOLD}[+]{Color.RESET} New  {Color.BOLD}[E]{Color.RESET} Edit  {Color.BOLD}[U]{Color.RESET} Progress  {Color.BOLD}[D]{Color.RESET} Delete"
        )
    print(f"  {Color.BOLD}[V]{Color.RESET} Back")
    print(f"{Color.DIM}{'─' * 100}{Color.RESET}\n")


# ─── Calendar ────────────────────────────────────────────────────────────────


def _render_calendar(data: dict) -> None:
    now = datetime.now()
    month_key = f"{now.year}-{now.month:02d}"
    marked_days = {
        int(k): v for k, v in data.get("calendar", {}).get(month_key, {}).items()
    }

    for line in _create_visual_calendar(now.year, now.month, marked_days).split("\n"):
        print(f"  {line}")

    print(f"\n{Color.DIM}{'─' * 100}{Color.RESET}")
    print(f"\n{Color.BOLD}MARK TODAY:{Color.RESET}")
    print(
        f"  {Color.GREEN_B}[C]{Color.RESET} Complete  {Color.YELLOW_B}[P]{Color.RESET} Partial  {Color.RED_B}[F]{Color.RESET} Failed  {Color.DIM}[L]{Color.RESET} Clear"
    )


def _create_visual_calendar(year: int, month: int, marked_days: dict) -> str:
    cal = calendar.monthcalendar(year, month)
    today = (
        datetime.now().day
        if (datetime.now().year == year and datetime.now().month == month)
        else -1
    )
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    lines = [
        f"{Color.BOLD}{Color.CYAN_B}{MONTHS_LIST[month - 1]} {year}{Color.RESET}",
        f"{Color.DIM}{'─' * 42}{Color.RESET}",
        "  ".join(f"{Color.BOLD}{d:^3}{Color.RESET}" for d in weekdays),
        f"{Color.DIM}{'─' * 42}{Color.RESET}",
    ]

    STATUS_COLOR = {
        "complete": Color.GREEN_B,
        "partial": Color.YELLOW_B,
        "failed": Color.RED_B,
    }

    for week in cal:
        line = []
        for day in week:
            if day == 0:
                line.append(f"{Color.DIM}   {Color.RESET}")
            elif day == today:
                line.append(f"{Color.BG_BLUE}{Color.WHITE}{day:2d}{Color.RESET} ")
            else:
                status = marked_days.get(day)
                color = STATUS_COLOR.get(status, Color.DIM)
                line.append(f"{color}{day:2d}{Color.RESET} ")
        lines.append("  ".join(line))

    lines += [
        f"\n{Color.DIM}{'─' * 42}{Color.RESET}",
        f"{Color.GREEN_B}██{Color.RESET} Complete  {Color.YELLOW_B}██{Color.RESET} Partial  "
        f"{Color.RED_B}██{Color.RESET} Failed  {Color.BG_BLUE}{Color.WHITE}██{Color.RESET} Today",
    ]
    return "\n".join(lines)


def _handle_calendar(data: dict, cmd: str) -> None:
    mapping = {"c": "complete", "p": "partial", "f": "failed"}
    if cmd in mapping:
        _mark_day(data, mapping[cmd])
    elif cmd == "l":
        _clear_day(data)


def _mark_day(data: dict, status: str) -> None:
    now = datetime.now()
    month_key = f"{now.year}-{now.month:02d}"
    data.setdefault("calendar", {}).setdefault(month_key, {})[str(now.day)] = status
    if save_data(data):
        msgs = {
            "complete": ("Day marked as complete! ✓", "success"),
            "partial": ("Day marked as partial!", "warning"),
            "failed": ("Day marked as failed.", "error"),
        }
        show_feedback(*msgs[status])


def _clear_day(data: dict) -> None:
    now = datetime.now()
    month_key = f"{now.year}-{now.month:02d}"
    cal = data.get("calendar", {}).get(month_key, {})
    if str(now.day) in cal:
        del cal[str(now.day)]
        if save_data(data):
            show_feedback("Day mark removed!", "info")


# ─── Goal CRUD ───────────────────────────────────────────────────────────────


def _get_filtered_goals(
    data: dict, goal_type: str, month: int
) -> list[tuple[int, dict]]:
    """Returns list of (real_index, goal) filtered by month (for monthly goals)."""
    if goal_type == "monthly":
        month_name = MONTHS_LIST[month - 1]
        return [
            (i, g)
            for i, g in enumerate(data["goals"]["monthly"])
            if month_name in g.get("text", "")
        ]
    return list(enumerate(data["goals"].get(goal_type, [])))


def _add_goal(data: dict, goal_type: str, month: int) -> None:
    print(f"\n{Color.GREEN_B}➕ NEW {goal_type.upper()} GOAL{Color.RESET}")
    text = input("Description: ").strip()
    if not text:
        return
    try:
        prog = int(input("Initial progress (0-100) [0]: ").strip() or "0")
        prog = max(0, min(100, prog))
    except ValueError:
        prog = 0

    data["goals"][goal_type].append({"text": text, "progress": prog})
    if save_data(data):
        show_feedback("Goal added!", "success")


def _edit_goal(data: dict, goal_type: str, month: int) -> None:
    goals = _get_filtered_goals(data, goal_type, month)
    if not goals:
        show_feedback("No goals to edit!", "warning")
        return
    try:
        idx_display = int(input(f"\n{Color.BLUE}Goal number:{Color.RESET} ")) - 1
        real_idx, goal = goals[idx_display]
        print(f"{Color.DIM}Current text: {goal['text']}{Color.RESET}")
        new_text = input("New text (Enter to keep): ").strip()
        if new_text:
            data["goals"][goal_type][real_idx]["text"] = new_text
            if save_data(data):
                show_feedback("Goal edited!", "success")
    except (ValueError, IndexError):
        show_feedback("Invalid input!", "error")


def _update_progress(data: dict, goal_type: str, month: int) -> None:
    goals = _get_filtered_goals(data, goal_type, month)
    if not goals:
        show_feedback("No goals to update!", "warning")
        return
    try:
        idx_display = int(input(f"\n{Color.BLUE}Goal number:{Color.RESET} ")) - 1
        real_idx, goal = goals[idx_display]
        print(f"{Color.DIM}Current progress: {goal['progress']}%{Color.RESET}")
        new_prog = int(input("New progress (0-100): ").strip())
        data["goals"][goal_type][real_idx]["progress"] = max(0, min(100, new_prog))
        if save_data(data):
            show_feedback(f"Progress updated to {new_prog}%!", "success")
    except (ValueError, IndexError):
        show_feedback("Invalid input!", "error")


def _delete_goal(data: dict, goal_type: str, month: int) -> None:
    goals = _get_filtered_goals(data, goal_type, month)
    if not goals:
        show_feedback("No goals to delete!", "warning")
        return
    try:
        idx_display = int(input(f"\n{Color.RED}Number to delete:{Color.RESET} ")) - 1
        real_idx, goal = goals[idx_display]
        confirm = input(f"Confirm delete '{goal['text']}'? (y/n): ").lower()
        if confirm == "y":
            data["goals"][goal_type].pop(real_idx)
            if save_data(data):
                show_feedback("Goal deleted!", "success")
    except (ValueError, IndexError):
        show_feedback("Invalid input!", "error")
