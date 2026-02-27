"""
Data persistence module.
Responsible for loading and saving application state to JSON.
"""

import json
import os
from datetime import datetime

from core.colors import Color
from core.constants import DATA_FILE, MONTHS_EN, MONTHS_LIST


def _get_initial_state() -> dict:
    """Returns the default state for a fresh installation."""
    now = datetime.now()
    current_month = MONTHS_EN.get(now.strftime("%B"), now.strftime("%B"))
    week_of_month = ((now.day - 1) // 7) + 1

    return {
        "notebooks": ["Today", "College", "Work", "Projects"],
        "active_notebook": "Today",
        "tasks": [
            {
                "id": 1,
                "text": "Study calculus",
                "status": "•",
                "notebook": "College",
                "notebooks": ["College"],
                "priority": 2,
            },
            {
                "id": 2,
                "text": "Drink water",
                "status": "X",
                "notebook": "Today",
                "notebooks": ["Today"],
                "priority": 1,
            },
            {
                "id": 3,
                "text": "Review code",
                "status": "•",
                "notebook": "Work",
                "notebooks": ["Work"],
                "priority": 3,
            },
        ],
        "goals": {
            "weekly": [
                {
                    "text": f"{current_month} - Week {week_of_month}",
                    "progress": 0,
                    "type": "current_week",
                },
                {"text": "Study 10h", "progress": 60},
                {"text": "Read 1 book", "progress": 30},
            ],
            "monthly": [
                {"text": f"{name} - {days} days", "progress": 0, "total_days": days}
                for name, days in zip(
                    MONTHS_LIST, [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                )
            ],
            "yearly": [
                {"text": "Finish degree", "progress": 80},
                {"text": "Learn Python", "progress": 65},
            ],
        },
        "notes": {},
        "calendar": {},
        "daily_activities": {},
        "next_id": 4,
    }


def _migrate_data(data: dict) -> dict:
    """Applies migrations for compatibility with older versions (including Portuguese keys)."""

    # Migrate Portuguese top-level keys to English
    key_map = {
        "cadernos": "notebooks",
        "caderno_ativo": "active_notebook",
        "tarefas": "tasks",
        "metas": "goals",
        "notas": "notes",
        "calendario": "calendar",
        "atividades_diarias": "daily_activities",
        "proximo_id": "next_id",
    }
    for old_key, new_key in key_map.items():
        if old_key in data and new_key not in data:
            data[new_key] = data.pop(old_key)

    # Migrate task field names
    for task in data.get("tasks", []):
        if "texto" in task and "text" not in task:
            task["text"] = task.pop("texto")
        if "caderno" in task and "notebook" not in task:
            task["notebook"] = task.pop("caderno")
        if "cadernos" in task and "notebooks" not in task:
            task["notebooks"] = task.pop("cadernos")
        if "prioridade" in task and "priority" not in task:
            task["priority"] = task.pop("prioridade")
        if "notebooks" not in task:
            task["notebooks"] = [task.get("notebook", "")]

    # Migrate goals keys
    if "goals" in data:
        goals = data["goals"]
        goal_key_map = {"semanais": "weekly", "mensais": "monthly", "anuais": "yearly"}
        for old_key, new_key in goal_key_map.items():
            if old_key in goals and new_key not in goals:
                goals[new_key] = goals.pop(old_key)
        for goal_type in ("weekly", "monthly", "yearly"):
            for goal in goals.get(goal_type, []):
                if "texto" in goal and "text" not in goal:
                    goal["text"] = goal.pop("texto")
                if "progresso" in goal and "progress" not in goal:
                    goal["progress"] = goal.pop("progresso")
                if "dias_total" in goal and "total_days" not in goal:
                    goal["total_days"] = goal.pop("dias_total")
                if goal.get("tipo") == "semana_atual" and "type" not in goal:
                    goal["type"] = "current_week"
                    del goal["tipo"]

    # Ensure required keys exist
    if "calendar" not in data:
        data["calendar"] = {}
    if "daily_activities" not in data:
        data["daily_activities"] = {}

    return data


def load_data() -> dict:
    """Loads data from the JSON file. Returns default state if not found."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return _migrate_data(data)
        except Exception:
            pass

    return _get_initial_state()


def save_data(data: dict) -> bool:
    """Persists data to the JSON file. Returns True if successful."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"{Color.RED}✗ Error saving: {e}{Color.RESET}")
        return False
