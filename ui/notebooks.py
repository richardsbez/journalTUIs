"""
Notebook selection screen with card layout.
"""

from core.colors import Color
from core.constants import TERMINAL_WIDTH, NOTEBOOK_EMOJIS, NOTEBOOK_COLORS
from ui.utils import (
    clear_screen,
    date_header,
    create_progress_bar,
    calculate_stats,
    visual_len,
)


def show_notebook_selection(data: dict) -> None:
    clear_screen()
    WIDTH = TERMINAL_WIDTH

    print(date_header())
    print(f"{Color.CYAN_B}{'━' * WIDTH}{Color.RESET}\n")
    print(f"{Color.BOLD}📚 CHOOSE YOUR NOTEBOOK{Color.RESET}")
    print(f"{Color.DIM}{'─' * WIDTH}{Color.RESET}\n")

    _render_cards(data["notebooks"], data["tasks"])

    print(f"{Color.DIM}{'─' * WIDTH}{Color.RESET}")
    print(f"{Color.BOLD}COMMANDS:{Color.RESET}")
    print(f"  {Color.BOLD}1-{len(data['notebooks'])}{Color.RESET} Select notebook")
    print(
        f"  {Color.BOLD}[N]{Color.RESET} New notebook  {Color.BOLD}[R]{Color.RESET} Remove notebook  {Color.BOLD}[Q]{Color.RESET} Quit"
    )
    print(f"{Color.DIM}{'─' * WIDTH}{Color.RESET}\n")


def _render_cards(notebooks: list, tasks: list, cards_per_row: int = 3) -> None:
    for i in range(0, len(notebooks), cards_per_row):
        row = notebooks[i : i + cards_per_row]
        _card_row(row, i, tasks)
        print()


def _card_row(notebooks_row: list, offset: int, tasks: list) -> None:
    inner_width = 26  # Adjusted for best fit in 3 columns
    reset = Color.RESET

    cards_data = []
    for j, name in enumerate(notebooks_row):
        emoji = NOTEBOOK_EMOJIS.get(name, "📓")
        total, done, prog = calculate_stats(tasks, name)

        # Dynamic color based on progress
        progress_color = (
            Color.GREEN if prog == 100 else (Color.YELLOW if prog > 0 else Color.RESET)
        )
        border_color = NOTEBOOK_COLORS[(offset + j) % len(NOTEBOOK_COLORS)]

        cards_data.append(
            {
                "id": f"{offset + j + 1}",
                "emoji": emoji,
                "name": name[: inner_width - 5],  # Trim to avoid layout break
                "color": border_color,
                "prog_color": progress_color,
                "stats": (total, done, prog),
            }
        )

    def print_row(content_list):
        print("  " + "    ".join(content_list))

    # 1. Top with rounded corners
    print_row([f"{c['color']}╭{'─' * inner_width}╮{reset}" for c in cards_data])

    # 2. Title (highlighted ID + Name)
    titles = []
    for c in cards_data:
        id_str = f"{Color.BOLD}{c['color']}{c['id']}.{reset}"
        text = f" {id_str} {c['emoji']} {Color.BOLD}{c['name']}{reset}"
        spaces = (
            inner_width
            - (
                visual_len(c["id"])
                + 2
                + visual_len(c["emoji"])
                + 1
                + visual_len(c["name"])
            )
            - 2
        )
        titles.append(f"{c['color']}│{reset}{text}{' ' * spaces}{c['color']}│{reset}")
    print_row(titles)

    # 3. Subtle separator
    print_row([f"{c['color']}├{'─' * inner_width}┤{reset}" for c in cards_data])

    # 4. Task info (compact and clean)
    stats_row = []
    for c in cards_data:
        txt = f"  {Color.DIM}Tasks:{reset} {c['stats'][0]:02}  {Color.DIM}Done:{reset} {c['prog_color']}{c['stats'][1]:02}{reset}"
        pad = inner_width - visual_len(
            f"  Tasks: {c['stats'][0]:02}  Done: {c['stats'][1]:02}"
        )
        stats_row.append(f"{c['color']}│{reset}{txt}{' ' * pad}{c['color']}│{reset}")
    print_row(stats_row)

    # 5. Styled progress bar
    bars = []
    for c in cards_data:
        prog = c["stats"][2]
        bar_str = create_progress_bar(prog, 14)
        txt_prog = f"  {bar_str} {c['prog_color']}{prog:>3}%{reset} "
        pad = inner_width - visual_len(f"  {bar_str} {prog:>3}% ")
        bars.append(f"{c['color']}│{reset}{txt_prog}{' ' * pad}{c['color']}│{reset}")
    print_row(bars)

    # 6. Footer
    print_row([f"{c['color']}╰{'─' * inner_width}╯{reset}" for c in cards_data])
