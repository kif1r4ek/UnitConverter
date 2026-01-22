from datetime import datetime, timezone

def format_relative_time(iso_date: str) -> str:
    created = datetime.fromisoformat(
        iso_date.replace("Z", "+00:00")
    )
    now = datetime.now(timezone.utc)

    diff = now - created
    seconds = diff.total_seconds()

    if seconds < 60:
        return "Just now"

    minutes = seconds // 60
    if minutes < 60:
        return f"{int(minutes)}m ago"

    hours = minutes // 60
    if hours < 24:
        return f"{int(hours)}h ago"

    return created.strftime("%d.%m.%Y")
