"""
Global constants and configuration for the application.
"""

DATA_FILE = "journal_data.json"
TERMINAL_WIDTH = 100

DAYS_EN = {
    "Monday": "Monday",
    "Tuesday": "Tuesday",
    "Wednesday": "Wednesday",
    "Thursday": "Thursday",
    "Friday": "Friday",
    "Saturday": "Saturday",
    "Sunday": "Sunday",
}

MONTHS_EN = {
    "January": "January",
    "February": "February",
    "March": "March",
    "April": "April",
    "May": "May",
    "June": "June",
    "July": "July",
    "August": "August",
    "September": "September",
    "October": "October",
    "November": "November",
    "December": "December",
}

MONTHS_LIST = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

NOTEBOOK_EMOJIS = {
    "Today": "📋",
    "College": "🎓",
    "Work": "💼",
    "Projects": "🚀",
    "Personal": "✨",
    "Health": "💪",
    "Studies": "📚",
    "Home": "🏠",
}

NOTEBOOK_COLORS = [
    "\033[96m",  # CYAN_B
    "\033[95m",  # MAGENTA_B
    "\033[92m",  # GREEN_B
    "\033[93m",  # YELLOW_B
    "\033[94m",  # BLUE_B
    "\033[91m",  # RED_B
]

SUGGESTED_ACTIVITIES = [
    "Exercise",
    "Meditation",
    "Reading",
    "Studying",
    "Coding",
    "Writing",
    "Art/Creativity",
    "Work/Projects",
]
