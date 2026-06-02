from datetime import datetime


def is_success(status):
    return status in ["excellent", "good"]


def calculate_success_rate(entries):

    if not entries:
        return 0

    successful = 0

    for entry in entries:

        if is_success(entry["status"]):
            successful += 1

    return round(
        (successful / len(entries)) * 100
    )


def calculate_current_streak(entries):

    if not entries:
        return 0

    sorted_entries = sorted(
        entries,
        key=lambda x: x["entry_date"],
        reverse=True
    )

    streak = 0

    for entry in sorted_entries:

        if is_success(entry["status"]):
            streak += 1
        else:
            break

    return streak


def calculate_best_streak(entries):

    if not entries:
        return 0

    sorted_entries = sorted(
        entries,
        key=lambda x: x["entry_date"]
    )

    best = 0
    current = 0

    for entry in sorted_entries:

        if is_success(entry["status"]):
            current += 1
            best = max(best, current)

        else:
            current = 0

    return best