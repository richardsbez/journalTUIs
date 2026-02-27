"""
Main screen (dashboard): tasks + goals + heatmap.
"""

from datetime import datetime, timedelta

from core.colors import Color
from core.constants import TERMINAL_WIDTH
from ui.utils import (
    clear_screen,
    date_header,
    create_progress_bar,
    get_priority_emoji,
    calculate_stats,
    visual_len,
    truncate_text,
)


def show_interface(data: dict) -> None:
    clear_screen()
    WIDTH = TERMINAL_WIDTH
    active_notebook = data["active_notebook"]
    tasks = data["tasks"]
    goals = data.get("goals", {"weekly": [], "monthly": [], "yearly": []})

    print(date_header())
    print(f"{Color.CYAN_B}{'━' * WIDTH}{Color.RESET}\n")

    _render_columns(tasks, goals, active_notebook)
    _render_heatmap(data)

    print(f"{Color.CYAN_B}{'━' * WIDTH}{Color.RESET}")
    print(
        f"{Color.BOLD}COMMANDS{Color.RESET} -> {Color.BOLD}C{Color.RESET} Notebooks menu  {Color.BOLD}Q{Color.RESET} Quit"
    )
    print(f"{Color.CYAN_B}{'━' * WIDTH}{Color.RESET}\n")


def _render_columns(tasks: list, goals: dict, active_notebook: str) -> None:
    LEFT_WIDTH = 55
    RIGHT_WIDTH = 43

    total, completed, progress = calculate_stats(tasks, active_notebook)
    filtered_tasks = sorted(
        [t for t in tasks if active_notebook in t.get("notebooks", [t["notebook"]])],
        key=lambda x: (x["status"] == "X", -x.get("priority", 2)),
    )
    pending = [t for t in filtered_tasks if t["status"] != "X"]
    completed_list = [t for t in filtered_tasks if t["status"] == "X"]
    weekly_goals = goals.get("weekly", [])

    # Headers
    print(
        f"{Color.BOLD}✓ TASKS • {active_notebook.upper():<40}{Color.RESET}  {Color.BOLD}🎯 WEEKLY GOALS{Color.RESET}"
    )
    print(f"{Color.DIM}{'─' * LEFT_WIDTH}  {'─' * RIGHT_WIDTH}{Color.RESET}")

    # Progress bars
    tasks_bar = create_progress_bar(progress, 35)
    left_progress = f"  {tasks_bar} {Color.BOLD}{progress}%{Color.RESET} {Color.DIM}({completed}/{total}){Color.RESET}"

    if weekly_goals:
        avg = int(sum(g.get("progress", 0) for g in weekly_goals) / len(weekly_goals))
        right_progress = (
            f"{create_progress_bar(avg, 25)} {Color.BOLD}{avg}%{Color.RESET}"
        )
    else:
        right_progress = f"{Color.DIM}No goals defined{Color.RESET}"

    spaces = LEFT_WIDTH - visual_len(left_progress)
    print(f"{left_progress}{' ' * spaces}  {right_progress}\n")

    # Build lines
    left_lines = _task_lines(pending, completed_list, active_notebook)
    right_lines = _goal_lines(weekly_goals)

    for i in range(max(len(left_lines), len(right_lines))):
        left = left_lines[i] if i < len(left_lines) else ""
        right = right_lines[i] if i < len(right_lines) else ""
        spaces = LEFT_WIDTH - visual_len(left)
        print(f"{left}{' ' * spaces}  {right}")

    print()
    print(
        f"{Color.DIM}[+] Add  [X] Complete  [E] Edit  [D] Delete  [P] Priority  [M] Goals{Color.RESET}"
    )
    print(f"{Color.BLUE}{'─' * TERMINAL_WIDTH}{Color.RESET}\n")


def _task_lines(pending: list, completed_list: list, active_notebook: str) -> list:
    lines = []
    if not pending and not completed_list:
        return [
            f"{Color.DIM}No tasks yet{Color.RESET}",
            f"{Color.DIM}Use [+] to add one!{Color.RESET}",
        ]

    if pending:
        lines.append(f"{Color.YELLOW_B}⚡ PENDING{Color.RESET}")
        for t in pending[:8]:
            emoji, color = get_priority_emoji(t.get("priority", 2))
            id_str = f"{color}#{t['id']:02d}{Color.RESET}"
            text = truncate_text(t["text"], 35)
            extras = [nb for nb in t.get("notebooks", []) if nb != active_notebook]
            indicator = (
                f" {Color.DIM}+{len(extras) if len(extras) > 1 else ''}{Color.RESET}"
                if extras
                else ""
            )
            lines.append(f"  {id_str} {emoji} {text}{indicator}")
        if len(pending) > 8:
            lines.append(
                f"  {Color.DIM}... and {len(pending) - 8} more tasks{Color.RESET}"
            )
        lines.append("")

    if completed_list:
        lines.append(f"{Color.GREEN_B}✓ COMPLETED ({len(completed_list)}){Color.RESET}")
        for t in completed_list[:3]:
            emoji, color = get_priority_emoji(t.get("priority", 2))
            id_str = f"{color}#{t['id']:02d}{Color.RESET}"
            text = truncate_text(t["text"], 35)
            lines.append(f"  {id_str} {Color.DIM}✓ {text}{Color.RESET}")
        if len(completed_list) > 3:
            lines.append(
                f"  {Color.DIM}... and {len(completed_list) - 3} more{Color.RESET}"
            )

    return lines


def _goal_lines(weekly_goals: list) -> list:
    if not weekly_goals:
        return [f"{Color.DIM}Use [M] to create goals!{Color.RESET}"]

    lines = []
    for idx, goal in enumerate(weekly_goals[:6], 1):
        prog = goal.get("progress", 0)
        text = truncate_text(goal.get("text", ""), 35)
        if goal.get("type") == "current_week":
            text = f"{Color.CYAN_B}⭐ {text}{Color.RESET}"
        lines.append(f"{Color.BOLD}{idx}.{Color.RESET} {text}")
        lines.append(
            f"   {create_progress_bar(prog, 25)} {Color.BOLD}{prog}%{Color.RESET}"
        )
        lines.append("")

    return lines


def _render_heatmap(data: dict) -> None:
    print(f"{Color.BOLD}🔥 ACTIVITY HEATMAP • CURRENT WEEK{Color.RESET}")
    print(f"{Color.DIM}{'─' * TERMINAL_WIDTH}{Color.RESET}")

    activities = data.get("daily_activities", {})
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Day names row
    names_row = "  " + "  ".join(f"{Color.BOLD}{d:^5}{Color.RESET}" for d in day_names)
    print(names_row)

    # Colored blocks row
    LEVEL_CONFIG = [
        (Color.DIM, "░"),
        (Color.GREEN, "▓"),
        (Color.GREEN_B, "▓"),
        (Color.YELLOW_B, "▓"),
        (Color.CYAN_B, "█"),
    ]
    heat_row = "  "
    for i in range(7):
        day = week_start + timedelta(days=i)
        key = day.strftime("%Y-%m-%d")
        level = activities.get(key, {}).get("level", 0)
        color, char = LEVEL_CONFIG[min(level, 4)]
        if day.date() == today.date():
            heat_row += f"{Color.BG_BLUE}{Color.WHITE} {char * 3} {Color.RESET} "
        else:
            heat_row += f"{color}{char * 5}{Color.RESET} "
    print(heat_row)

    print(
        f"\n  {Color.DIM}░░{Color.RESET} None  "
        f"{Color.GREEN}▓▓{Color.RESET} Low  "
        f"{Color.GREEN_B}▓▓{Color.RESET} Medium  "
        f"{Color.YELLOW_B}▓▓{Color.RESET} High  "
        f"{Color.CYAN_B}██{Color.RESET} Excellent"
    )

    today_key = today.strftime("%Y-%m-%d")
    today_total = sum(activities.get(today_key, {}).get("activities", {}).values())
    if today_total > 0:
        print(
            f"\n  {Color.CYAN_B}📊 Today: {today_total} activity/activities logged{Color.RESET}"
        )
    else:
        print(f"\n  {Color.DIM}💭 No activities logged today yet{Color.RESET}")

    print()
    print(f"{Color.DIM}[H] Heatmap  [S] Statistics  [A] Notes{Color.RESET}")
    print(f"{Color.BLUE}{'─' * TERMINAL_WIDTH}{Color.RESET}\n")
