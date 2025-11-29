from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Habit:
    """
    Domain model for a single habit.

    Attributes:
        id: database identifier (None for new habits not stored yet)
        name: human-readable name of the habit
        periodicity: "daily" or "weekly"
        created_at: ISO-formatted datetime string (when the habit was created)
    """

    name: str
    periodicity: str
    created_at: str
    id: Optional[int] = None

    @classmethod
    def new(cls, name: str, periodicity: str) -> "Habit":
        """Factory for creating a new habit with current timestamp."""
        now = datetime.now().isoformat(timespec="seconds")
        return cls(name=name, periodicity=periodicity, created_at=now)

    def __str__(self) -> str:
        return f"Habit(id={self.id}, name={self.name!r}, periodicity={self.periodicity}, created_at={self.created_at})"
