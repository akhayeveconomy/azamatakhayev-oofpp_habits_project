from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from .db import init_db
from .models import Habit

ALLOWED = {"daily", "weekly"}

def create_habit(conn, name: str, periodicity: str) -> Optional[int]:
    init_db(conn)
    periodicity = periodicity.strip().lower()
    name = name.strip()

    if periodicity not in ALLOWED or not name:
        return None

    now = datetime.now().isoformat(timespec="seconds")
    try:
        cur = conn.execute(
            "INSERT INTO habits(name, periodicity, created_at) VALUES (?, ?, ?)",
            (name, periodicity, now),
        )
        conn.commit()
        return int(cur.lastrowid)
    except Exception:
        return None

def list_habits(conn) -> List[Habit]:
    init_db(conn)
    rows = conn.execute(
        "SELECT id, name, periodicity, created_at FROM habits ORDER BY id"
    ).fetchall()

    habits: List[Habit] = []
    for r in rows:
        habits.append(
            Habit(
                id=r["id"],
                name=r["name"],
                periodicity=r["periodicity"],
                created_at=datetime.fromisoformat(r["created_at"]),
            )
        )
    return habits

def delete_habit(conn, habit_id: int) -> bool:
    init_db(conn)
    cur = conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    return cur.rowcount > 0

def complete_habit(conn, habit_id: int, when: datetime | None = None) -> bool:
    init_db(conn)
    when = when or datetime.now()

    row = conn.execute("SELECT id FROM habits WHERE id = ?", (habit_id,)).fetchone()
    if not row:
        return False

    conn.execute(
        "INSERT INTO completions(habit_id, completed_at) VALUES (?, ?)",
        (habit_id, when.isoformat(timespec="seconds")),
    )
    conn.commit()
    return True

def get_completions(conn, habit_id: int) -> list[datetime]:
    init_db(conn)
    rows = conn.execute(
        "SELECT completed_at FROM completions WHERE habit_id = ? ORDER BY completed_at",
        (habit_id,),
    ).fetchall()
    return [datetime.fromisoformat(r["completed_at"]) for r in rows]