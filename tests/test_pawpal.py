from datetime import date, timedelta

from pawpal_system import CareTask, Pet, Scheduler


def make_task(name, time="", frequency="daily", pet_name="", due_date=None, must_do=True):
    """Helper to create a CareTask with sensible defaults."""
    return CareTask(
        name=name,
        description="",
        duration=10,
        frequency=frequency,
        priority=3,
        must_do=must_do,
        category="feeding",
        pet_name=pet_name,
        time=time,
        due_date=due_date,
    )


# --- Existing tests ---

def test_task_completion_changes_status() -> None:
    task = CareTask(
        name="Feed Dog",
        description="Feed breakfast",
        duration=10,
        frequency="daily",
        priority=5,
        must_do=True,
        category="feeding",
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_task_addition_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog", age=3)
    task = CareTask(
        name="Morning Walk",
        description="Walk in the park",
        duration=30,
        frequency="daily",
        priority=4,
        must_do=True,
        category="exercise",
    )

    before_count = len(pet.tasks)
    pet.add_task(task)
    after_count = len(pet.tasks)

    assert after_count == before_count + 1


# --- Sorting ---

def test_sort_by_time_returns_tasks_in_chronological_order():
    tasks = [
        make_task("Evening Feed",  time="18:00"),
        make_task("Morning Feed",  time="07:00"),
        make_task("Midday Walk",   time="12:00"),
    ]

    sorted_tasks = Scheduler().sort_by_time(tasks)
    times = [t.time for t in sorted_tasks]

    assert times == ["07:00", "12:00", "18:00"]


def test_sort_by_time_with_identical_times_does_not_crash():
    tasks = [
        make_task("Task A", time="08:00"),
        make_task("Task B", time="08:00"),
    ]

    sorted_tasks = Scheduler().sort_by_time(tasks)
    assert len(sorted_tasks) == 2


def test_sort_by_time_with_empty_list_returns_empty():
    assert Scheduler().sort_by_time([]) == []


# --- Recurrence ---

def test_daily_task_mark_complete_returns_next_day():
    today = date(2026, 4, 2)
    task = make_task("Morning Feed", frequency="daily", due_date=today)

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False


def test_weekly_task_mark_complete_returns_seven_days_later():
    today = date(2026, 4, 2)
    task = make_task("Bath Time", frequency="weekly", due_date=today)

    next_task = task.mark_complete()

    assert next_task.due_date == today + timedelta(days=7)


def test_recurrence_with_no_due_date_does_not_crash():
    task = make_task("Morning Feed", frequency="daily", due_date=None)

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_non_recurring_task_mark_complete_returns_none():
    task = make_task("One-off task", frequency="as-needed")

    result = task.mark_complete()

    assert task.completed is True
    assert result is None


# --- Conflict detection ---

def test_detect_conflicts_returns_warning_for_same_time():
    tasks = [
        make_task("Morning Feed", time="07:30", pet_name="Mochi"),
        make_task("Morning Walk", time="07:30", pet_name="Mochi"),
    ]

    warnings = Scheduler().detect_conflicts(tasks)

    assert len(warnings) == 1
    assert "07:30" in warnings[0]


def test_detect_conflicts_cross_pet_overlap():
    tasks = [
        make_task("Dog Feed",  time="08:00", pet_name="Mochi"),
        make_task("Cat Feed",  time="08:00", pet_name="Whiskers"),
    ]

    warnings = Scheduler().detect_conflicts(tasks)

    assert len(warnings) == 1
    assert "Mochi" in warnings[0]
    assert "Whiskers" in warnings[0]


def test_detect_conflicts_no_conflicts_returns_empty_list():
    tasks = [
        make_task("Morning Feed", time="07:00", pet_name="Mochi"),
        make_task("Evening Walk", time="18:00", pet_name="Mochi"),
    ]

    warnings = Scheduler().detect_conflicts(tasks)

    assert warnings == []


def test_detect_conflicts_tasks_without_time_are_ignored():
    tasks = [
        make_task("Task A", time="", pet_name="Mochi"),
        make_task("Task B", time="", pet_name="Mochi"),
    ]

    warnings = Scheduler().detect_conflicts(tasks)

    assert warnings == []


def test_detect_conflicts_empty_list_returns_empty():
    assert Scheduler().detect_conflicts([]) == []
