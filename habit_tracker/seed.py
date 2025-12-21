from datetime import datetime, timedelta
from .repository import create_habit, complete_habit

def seed_demo_data(conn) -> None:
    habits = [
        ("Play Football", "daily"),
        ("Read 10 pages", "daily"),
        ("Drink water", "daily"),
        ("Go to gym", "weekly"),
        ("Call parents", "weekly"),
    ]

    ids = []
    for name, p in habits:
        hid = create_habit(conn, name, p)
        if hid is not None:
            ids.append((hid, p))

    start = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) - timedelta(days=28)

    for hid, p in ids:
        if p == "daily":
            for d in range(28):
                if d % 7 not in (5, 6):  # пропускаем часть дней
                    complete_habit(conn, hid, start + timedelta(days=d))
        else:
            for w in range(4):
                complete_habit(conn, hid, start + timedelta(days=w * 7))