def progress_bar(percent: float) -> str:
    filled = round(percent / 5)
    filled = max(0, min(filled, 20))
    return "█" * filled + "░" * (20 - filled)