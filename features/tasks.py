"""
Task CRUD commands and notebook management.
"""

from core.colors import Color
from core.storage import save_data
from ui.utils import show_feedback


# ─── Tasks ───────────────────────────────────────────────────────────────────


def add_task(data: dict) -> None:
    print(f"\n{Color.GREEN_B}➕ NEW TASK{Color.RESET}")
    print(f"{Color.DIM}{'─' * 50}{Color.RESET}")
    txt = input("Description: ").strip()
    if not txt:
        return

    priority = _ask_priority()
    task_notebooks = _ask_additional_notebooks(data)

    data["tasks"].append(
        {
            "id": data["next_id"],
            "text": txt,
            "status": "•",
            "notebook": data["active_notebook"],
            "notebooks": task_notebooks,
            "priority": priority,
        }
    )
    data["next_id"] += 1

    if save_data(data):
        msg = "Task added!"
        if len(task_notebooks) > 1:
            msg += f" (in {len(task_notebooks)} notebooks)"
        show_feedback(msg, "success")


def complete_task(data: dict) -> None:
    try:
        task_id = int(input(f"\n{Color.YELLOW}Task ID:{Color.RESET} "))
        for t in data["tasks"]:
            if t["id"] == task_id:
                t["status"] = "X" if t["status"] == "•" else "•"
                status_msg = "completed" if t["status"] == "X" else "reopened"
                if save_data(data):
                    show_feedback(f"Task {status_msg}!", "success")
                return
        show_feedback("Task not found!", "error")
    except ValueError:
        show_feedback("Invalid ID!", "error")


def edit_task(data: dict) -> None:
    try:
        task_id = int(input(f"\n{Color.BLUE}Task ID to edit:{Color.RESET} "))
        for t in data["tasks"]:
            if t["id"] == task_id:
                print(f"{Color.DIM}Current text: {t['text']}{Color.RESET}")
                new_text = input("New text (Enter to keep): ").strip()
                if new_text:
                    t["text"] = new_text
                    if save_data(data):
                        show_feedback("Task edited!", "success")
                return
        show_feedback("Task not found!", "error")
    except ValueError:
        show_feedback("Invalid ID!", "error")


def delete_task(data: dict) -> None:
    try:
        task_id = int(input(f"\n{Color.RED}Task ID to delete:{Color.RESET} "))
        task = next((t for t in data["tasks"] if t["id"] == task_id), None)
        if not task:
            show_feedback("Task not found!", "error")
            return
        confirm = input(f"Confirm delete '{task['text']}'? (y/n): ").lower()
        if confirm == "y":
            data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
            if save_data(data):
                show_feedback("Task deleted!", "success")
    except ValueError:
        show_feedback("Invalid ID!", "error")


def change_priority(data: dict) -> None:
    try:
        task_id = int(input(f"\n{Color.BLUE}Task ID:{Color.RESET} "))
        new_priority = int(
            input(
                f"New priority ({Color.RED_B}1{Color.RESET}=High, "
                f"{Color.YELLOW_B}2{Color.RESET}=Medium, {Color.GREEN_B}3{Color.RESET}=Low): "
            )
        )
        for t in data["tasks"]:
            if t["id"] == task_id:
                t["priority"] = max(1, min(3, new_priority))
                if save_data(data):
                    show_feedback("Priority updated!", "success")
                return
        show_feedback("Task not found!", "error")
    except ValueError:
        show_feedback("Invalid input!", "error")


# ─── Notebooks ───────────────────────────────────────────────────────────────


def add_notebook(data: dict) -> None:
    print(f"\n{Color.BLUE_B}📚 NEW NOTEBOOK{Color.RESET}")
    print(f"{Color.DIM}{'─' * 50}{Color.RESET}")
    name = input("Name: ").strip().title()
    if not name:
        return
    if name in data["notebooks"]:
        show_feedback("A notebook with that name already exists!", "warning")
        return
    data["notebooks"].append(name)
    if save_data(data):
        show_feedback(f"Notebook '{name}' created!", "success")


def remove_notebook(data: dict) -> None:
    if len(data["notebooks"]) <= 1:
        show_feedback("You need at least one notebook!", "warning")
        return

    print(f"\n{Color.RED}🗑️  REMOVE NOTEBOOK{Color.RESET}")
    print(f"{Color.DIM}{'─' * 50}{Color.RESET}")
    for i, nb in enumerate(data["notebooks"], 1):
        n = len([t for t in data["tasks"] if nb in t.get("notebooks", [t["notebook"]])])
        print(f"  {i}. {nb} ({n} tasks)")

    try:
        idx = int(input("\nNotebook number: ")) - 1
        if not (0 <= idx < len(data["notebooks"])):
            show_feedback("Invalid number!", "error")
            return

        name = data["notebooks"][idx]
        confirm = input(
            f"\n{Color.YELLOW}Remove '{name}'? (tasks removed from this notebook only) (y/n):{Color.RESET} "
        ).lower()
        if confirm != "y":
            return

        data["notebooks"].pop(idx)
        for t in data["tasks"]:
            if name in t.get("notebooks", []):
                t["notebooks"].remove(name)
        data["tasks"] = [t for t in data["tasks"] if t.get("notebooks")]

        if data["active_notebook"] == name:
            data["active_notebook"] = data["notebooks"][0]
        if save_data(data):
            show_feedback("Notebook removed!", "success")
    except ValueError:
        show_feedback("Invalid input!", "error")


def select_notebook(data: dict, idx: int) -> bool:
    """Selects a notebook by index (0-based). Returns True if valid."""
    if 0 <= idx < len(data["notebooks"]):
        data["active_notebook"] = data["notebooks"][idx]
        save_data(data)
        return True
    return False


# ─── Internal helpers ────────────────────────────────────────────────────────


def _ask_priority() -> int:
    try:
        value = input(
            f"Priority ({Color.RED_B}1{Color.RESET}=High, "
            f"{Color.YELLOW_B}2{Color.RESET}=Medium, {Color.GREEN_B}3{Color.RESET}=Low) "
            f"[{Color.YELLOW_B}2{Color.RESET}]: "
        ).strip()
        return max(1, min(3, int(value))) if value else 2
    except ValueError:
        return 2


def _ask_additional_notebooks(data: dict) -> list:
    task_notebooks = [data["active_notebook"]]
    others = [nb for nb in data["notebooks"] if nb != data["active_notebook"]]
    if not others:
        return task_notebooks

    print(f"\n{Color.CYAN}Add to other notebooks as well?{Color.RESET}")
    for i, nb in enumerate(others, 1):
        print(f"  {i}. {nb}")
    print(f"\n{Color.DIM}Comma-separated numbers or Enter to skip{Color.RESET}")

    choices = input(f"{Color.CYAN}Notebooks:{Color.RESET} ").strip()
    if choices:
        try:
            indices = [int(x.strip()) - 1 for x in choices.split(",")]
            for i in indices:
                if 0 <= i < len(others) and others[i] not in task_notebooks:
                    task_notebooks.append(others[i])
        except ValueError:
            print(
                f"{Color.YELLOW}⚠ Invalid input, task created in current notebook only{Color.RESET}"
            )
            input(f"{Color.DIM}Press ENTER...{Color.RESET}")

    return task_notebooks
