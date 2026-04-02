"""
PawPal+ Demo Script
This script demonstrates the core functionality of the pet care scheduling system.
"""

from pawpal_system import CareTask, Pet, PetOwner, Scheduler

DIVIDER_WIDTH = 60


def print_section_header(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "-" * DIVIDER_WIDTH)
    print(title)
    print("-" * DIVIDER_WIDTH)


def print_task(task: CareTask) -> None:
    """Print a single task's key details."""
    status = "Done" if task.completed else "Pending"
    print(f"  [{status}] {task.name} | pet: {task.pet_name} | time: {task.time or 'N/A'} | {task.duration} min")


def main():
    scheduler = Scheduler()

    # --- Create tasks with time values out of order ---
    tasks = [
        CareTask(name="Evening Walk",    description="Walk around the block",   duration=30, frequency="daily", priority=4, must_do=True,  category="exercise",   pet_name="Mochi",    time="18:00"),
        CareTask(name="Morning Feed",    description="Breakfast for Mochi",     duration=10, frequency="daily", priority=5, must_do=True,  category="feeding",    pet_name="Mochi",    time="07:30"),
        CareTask(name="Litter Box",      description="Clean litter box",        duration=10, frequency="daily", priority=4, must_do=True,  category="cleaning",   pet_name="Whiskers", time="08:00"),
        CareTask(name="Cat Playtime",    description="Interactive play",        duration=15, frequency="daily", priority=2, must_do=False, category="enrichment", pet_name="Whiskers", time="17:00"),
        CareTask(name="Midday Walk",     description="Short park walk",         duration=20, frequency="daily", priority=3, must_do=False, category="exercise",   pet_name="Mochi",    time="12:00"),
        CareTask(name="Cat Feeding",     description="Lunch for Whiskers",      duration=5,  frequency="daily", priority=5, must_do=True,  category="feeding",    pet_name="Whiskers", time="07:00"),
    ]

    # Mark one task as completed
    tasks[2].mark_complete()  # Litter Box is done

    # --- Sort by time ---
    print_section_header("TASKS SORTED BY TIME (ascending)")
    sorted_tasks = scheduler.sort_by_time(tasks)
    for task in sorted_tasks:
        print_task(task)

    # --- Filter by pet ---
    print_section_header("TASKS FOR MOCHI")
    mochi_tasks = scheduler.filter_by_pet(tasks, "Mochi")
    for task in mochi_tasks:
        print_task(task)

    print_section_header("TASKS FOR WHISKERS")
    whiskers_tasks = scheduler.filter_by_pet(tasks, "Whiskers")
    for task in whiskers_tasks:
        print_task(task)

    # --- Filter by completion status ---
    print_section_header("COMPLETED TASKS")
    completed = scheduler.filter_by_status(tasks, completed=True)
    for task in completed:
        print_task(task)

    print_section_header("INCOMPLETE TASKS")
    incomplete = scheduler.filter_by_status(tasks, completed=False)
    for task in incomplete:
        print_task(task)

    # --- Conflict detection demo ---
    print_section_header("CONFLICT DETECTION")

    conflict_tasks = [
        CareTask(name="Morning Feed",  description="Breakfast",       duration=10, frequency="daily",  priority=5, must_do=True,  category="feeding",   pet_name="Mochi",    time="07:30"),
        CareTask(name="Morning Walk",  description="Park walk",        duration=20, frequency="daily",  priority=4, must_do=True,  category="exercise",  pet_name="Mochi",    time="07:30"),  # same pet, same time
        CareTask(name="Cat Feeding",   description="Whiskers lunch",   duration=5,  frequency="daily",  priority=5, must_do=True,  category="feeding",   pet_name="Whiskers", time="07:30"),  # different pet, same time
        CareTask(name="Evening Walk",  description="Neighborhood walk",duration=30, frequency="daily",  priority=3, must_do=False, category="exercise",  pet_name="Mochi",    time="18:00"),  # no conflict
    ]

    conflict_warnings = scheduler.detect_conflicts(conflict_tasks)
    if conflict_warnings:
        for warning in conflict_warnings:
            print(f"  WARNING: {warning}")
    else:
        print("  No conflicts found.")

    # --- Recurring task demo ---
    print_section_header("RECURRING TASK: NEXT OCCURRENCES")

    from datetime import date as dt_date
    daily_task = CareTask(
        name="Morning Feed", description="Breakfast for Mochi",
        duration=10, frequency="daily", priority=5, must_do=True,
        category="feeding", pet_name="Mochi", time="07:30", due_date=dt_date(2026, 4, 2)
    )
    weekly_task = CareTask(
        name="Bath Time", description="Full grooming session",
        duration=30, frequency="weekly", priority=3, must_do=False,
        category="grooming", pet_name="Whiskers", time="10:00", due_date=dt_date(2026, 4, 2)
    )

    daily_next = daily_task.create_next_occurrence()
    weekly_next = weekly_task.create_next_occurrence()

    print(f"  Daily task  '{daily_task.name}'  : {daily_task.due_date} -> next: {daily_next.due_date}")
    print(f"  Weekly task '{weekly_task.name}' : {weekly_task.due_date} -> next: {weekly_next.due_date}")
    print(f"  Next occurrence completed? {daily_next.completed}")

    print()


if __name__ == "__main__":
    main()
