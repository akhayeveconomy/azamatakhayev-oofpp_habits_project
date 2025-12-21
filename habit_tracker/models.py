from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Habit:
    id: int
    name: str
    periodicity: str  # "daily" or "weekly"
    created_at: datetime