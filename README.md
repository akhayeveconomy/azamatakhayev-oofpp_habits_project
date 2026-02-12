# Akhayev-Azamat_9216790_OOFPP_Habits_Submission_Final
# Habit tracking app - OOFPP Project

# introduction
This project implements Habit tracking app in Python

The application allows users to:
- Create daily and weekly habits
- Mark Habits as completed
- Delete Habits
- Track completion history
- Calculation streaks
- Analyse habits using functional programming

All data stored in an SQLite database.

# Project Structure
models.py # Domain model
db.py # SQLite connection and schema
repository.py # Database operations
analytics.py # Functional programming analytics
cli.py # Command-line interface
seed.py # Demo data (5 habits, 4 weeks)
tests/
test_app.py # Unit tests using pytest

# Core Functions
- Support for daily and weekly habits
- Create, delete and complete habits
- Store creation date and completion timestamps
- SQLite
- Command Line Interface (CLI)

# Analytics part
- List all habits
- Filter habits by periodicity
- Calculate longest streak

# Database schema
Habits table
- id (INTEGER PRIMARY KEY)
- name (TEXT UNIQUE)
- periodicity (TEXT, daily or weekly)
- created_at (TEXT)

Completions table
- id (INTEGER PRIMARY KEY)
- habit_id (FOREIGN KEY - habits.id)
- completed_at (TEXT)

#How to Run
- > pip install pytest
- > python -m habit_tracker.cli
