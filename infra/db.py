import sqlite3
from pathlib import Path

DB_PATH = Path("habits.db")

def get_connection() -> sqlite3.Connection:
    """Return sqlite connection to the database."""
    return sqlite3.connect(DB_PATH)

def init_db() -> None:
    """Create table if not exists."""
    conn = get_connection()
    cur = conn.cursor()

    #Table for habits
    cur.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        periodicity TEXT CHECK (periodicity IN ('daily', 'weekly', 'monthly')) NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    #Table for completed habit actions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS completions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habits_id INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (habit_id) REFERENCES habits(id)
    )
    """)

    conn.commit()
    conn.close()
    