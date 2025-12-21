from pathlib import Path
from .db import connect, init_db
from .repository import create_habit, list_habits, delete_habit, complete_habit, get_completions
from .analytics import filter_by_periodicity, longest_streak_all, longest_streak_for_habit
from .seed import seed_demo_data

DB_PATH = Path("habits.db")

def main() -> None:
    with connect(DB_PATH) as conn:
        init_db(conn)

        while True:
            print("\n=== Habit Tracker ===")
            print("1) List habits")
            print("2) Add habit")
            print("3) Delete habit")
            print("4) Complete habit")
            print("5) List daily habits")
            print("6) List weekly habits")
            print("7) Longest streak overall")
            print("8) Longest streak for a habit")
            print("9) Load demo data (5 habits + 4 weeks)")
            print("0) Exit")

            choice = input("Choose: ").strip()

            if choice == "1":
                habits = list_habits(conn)
                for h in habits:
                    print(f"{h.id}: {h.name} ({h.periodicity}) created {h.created_at}")

            elif choice == "2":
                name = input("Habit name: ")
                p = input("Periodicity (daily/weekly): ")
                hid = create_habit(conn, name, p)
                print("OK" if hid else "Failed (wrong periodicity or duplicate name)")

            elif choice == "3":
                hid = int(input("Habit id: "))
                print("Deleted" if delete_habit(conn, hid) else "Not found")

            elif choice == "4":
                hid = int(input("Habit id: "))
                print("Completed" if complete_habit(conn, hid) else "Not found")

            elif choice == "5":
                habits = filter_by_periodicity(list_habits(conn), "daily")
                for h in habits:
                    print(f"{h.id}: {h.name}")

            elif choice == "6":
                habits = filter_by_periodicity(list_habits(conn), "weekly")
                for h in habits:
                    print(f"{h.id}: {h.name}")

            elif choice == "7":
                habits = list_habits(conn)
                compl = {h.id: get_completions(conn, h.id) for h in habits}
                print("Longest overall streak =", longest_streak_all(habits, compl))

            elif choice == "8":
                hid = int(input("Habit id: "))
                habits_map = {h.id: h for h in list_habits(conn)}
                if hid not in habits_map:
                    print("Not found")
                else:
                    h = habits_map[hid]
                    cs = get_completions(conn, hid)
                    print("Longest streak =", longest_streak_for_habit(h.periodicity, cs))

            elif choice == "9":
                seed_demo_data(conn)
                print("Demo data loaded.")

            elif choice == "0":
                break
            else:
                print("Unknown option")

if __name__ == "__main__":
    main()