from pawpal_system import CareTask, Pet


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
