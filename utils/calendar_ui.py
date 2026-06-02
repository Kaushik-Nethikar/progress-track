import calendar
from datetime import date


STATUS_CONFIG = {
    "excellent": {
        "emoji": "🔥",
        "color": "#22C55E"
    },
    "good": {
        "emoji": "✅",
        "color": "#3B82F6"
    },
    "average": {
        "emoji": "➖",
        "color": "#F59E0B"
    },
    "bad": {
        "emoji": "❌",
        "color": "#EF4444"
    }
}


def month_grid(year, month):
    cal = calendar.Calendar(firstweekday=6)

    return cal.monthdayscalendar(
        year,
        month
    )


def build_entry_lookup(entries):

    lookup = {}

    for entry in entries:

        lookup[entry["entry_date"]] = entry

    return lookup


def get_day_info(lookup, year, month, day):

    key = f"{year}-{month:02d}-{day:02d}"

    if key not in lookup:

        return {
            "emoji": "",
            "color": "#334155",
            "note": False
        }

    entry = lookup[key]

    status = entry["status"]

    return {
        "emoji": STATUS_CONFIG[status]["emoji"],
        "color": STATUS_CONFIG[status]["color"],
        "note": bool(entry.get("note"))
    }