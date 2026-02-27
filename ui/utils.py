"""
UI utilities: reusable rendering functions.
"""

import os
import re
from datetime import datetime

from core.colors import Color
from core.constants import DAYS_EN, TERMINAL_WIDTH


# ─── Visual helpers ──────────────────────────────────────────────────────────


def visual_len(text: str) -> int:
    """Text length ignoring ANSI escape codes."""
    return len(re.sub(r"\033\[[0-9;]+m", "", text))


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def date_header(width: int = TERMINAL_WIDTH) -> str:
    """Returns formatted date/time line for the header."""
    now = datetime.now()
    weekday = DAYS_EN.get(now.strftime("%A"), now.strftime("%A"))
    date = now.strftime("%m/%d/%Y")
    time = now.strftime("%H:%M")
    return f"{Color.DIM}{f'{weekday} • {date} • {time}'.center(width)}{Color.RESET}"


def create_progress_bar(progress: int, width: int = 20) -> str:
    """Creates a colored progress bar with Unicode blocks."""
    num_blocks = int(progress / 100 * width)

    if progress >= 80:
        color = Color.GREEN_B
    elif progress >= 50:
        color = Color.YELLOW_B
    elif progress > 0:
        color = Color.RED_B
    else:
        color = Color.DIM

    bar = f"{color}{'█' * num_blocks}{Color.RESET}{Color.DIM}{'░' * (width - num_blocks)}{Color.RESET}"
    return bar


def get_priority_emoji(priority: int) -> tuple[str, str]:
    """Returns (emoji, color) based on priority level."""
    config = {
        1: ("🔴", Color.RED_B),
        2: ("🟡", Color.YELLOW_B),
        3: ("🟢", Color.GREEN_B),
    }
    return config.get(priority, ("⚪", Color.RESET))


def show_feedback(message: str, feedback_type: str = "success") -> None:
    """Displays a feedback message with icon and color based on type."""
    colors = {
        "success": Color.GREEN_B,
        "error": Color.RED_B,
        "info": Color.BLUE_B,
        "warning": Color.YELLOW_B,
    }
    icons = {"success": "✓", "error": "✗", "info": "ℹ", "warning": "⚠"}

    color = colors.get(feedback_type, Color.RESET)
    icon = icons.get(feedback_type, "•")

    print(f"\n{color}{icon} {message}{Color.RESET}")
    input(f"{Color.DIM}Press ENTER...{Color.RESET}")


# ─── Task helpers ────────────────────────────────────────────────────────────


def calculate_stats(tasks: list, notebook: str) -> tuple[int, int, int]:
    """Returns (total, completed, progress%) for tasks in a notebook."""
    notebook_tasks = [
        t for t in tasks if notebook in t.get("notebooks", [t["notebook"]])
    ]
    total = len(notebook_tasks)
    completed = sum(1 for t in notebook_tasks if t["status"] == "X")
    progress = int(completed / total * 100) if total > 0 else 0
    return total, completed, progress


def truncate_text(text: str, limit: int) -> str:
    """Truncates text to visual limit, adding '...' if needed."""
    if visual_len(text) > limit:
        return text[: limit - 3] + "..."
    return text
