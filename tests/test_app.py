from pathlib import Path
from datetime import datetime, timedelta
from habit_tracker.db import connect, init_db
from habit_tracker.repository import create_habit, complete_habit, list_habits, get_completions
from habit_tracker.analytics import longest_streak_for_habit

def test_create_and_complete(tmp_path: Path):
    db = tmp_path / "test.db"
    with connect(db) as conn:
        init_db(conn)

        hid = create_habit(conn, "Test habit", "daily")
        assert hid is not None

        ok = complete_habit(conn, hid)
        assert ok is True

        habits = list_habits(conn)
        assert len(habits) == 1
        assert habits[0].name == "Test habit"

        completions = get_completions(conn, hid)
        assert len(completions) == 1

def test_streak_daily(tmp_path: Path):
    db = tmp_path / "test.db"
    with connect(db) as conn:
        init_db(conn)

        hid = create_habit(conn, "Daily", "daily")
        assert hid is not None

        start = datetime(2025, 1, 1, 10, 0, 0)
        complete_habit(conn, hid, start)
        complete_habit(conn, hid, start + timedelta(days=1))
        complete_habit(conn, hid, start + timedelta(days=2))

        cs = get_completions(conn, hid)
        assert longest_streak_for_habit("daily", cs) == 3