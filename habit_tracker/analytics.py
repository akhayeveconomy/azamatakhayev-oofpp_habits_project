from __future__ import annotations
from datetime import datetime, timedelta
from typing import Iterable
from .models import Habit

def filter_by_periodicity(habits: Iterable[Habit], periodicity: str) -> list[Habit]:
    p = periodicity.strip().lower()
    return [h for h in habits if h.periodicity == p]

def _to_period_key(dt: datetime, periodicity: str) -> datetime:
    if periodicity == "daily":
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    day_start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return day_start - timedelta(days=day_start.weekday())

def longest_streak_for_habit(periodicity: str, completions: list[datetime]) -> int:
    if not completions:
        return 0

    keys = sorted({_to_period_key(c, periodicity) for c in completions})
    step = timedelta(days=1) if periodicity == "daily" else timedelta(days=7)

    best = 1
    streak = 1
    for i in range(1, len(keys)):
        if keys[i] == keys[i - 1] + step:
            streak += 1
        else:
            streak = 1
        best = max(best, streak)

    return best

def longest_streak_all(habits: list[Habit], completions_by_id: dict[int, list[datetime]]) -> int:
    streaks = [
        longest_streak_for_habit(h.periodicity, completions_by_id.get(h.id, []))
        for h in habits
    ]
    return max(streaks, default=0)