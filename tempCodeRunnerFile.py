from pawpal_system import CareTask, Pet, PetOwner, Scheduler

DIVIDER_WIDTH = 60


def create_task(name: str, description: str, duration: int, priority: int,
                must_do: bool, category: str, frequency: str = "daily") -> CareTask:
    """Helper function to create a CareTask with consistent structure."""
    return CareTask(
        name=name,
        description=description,
        duration=duration,
        frequency=frequency,
        priority=priority,
        must_do=must_do,
        category=category
    )


def build_pet_task_map(owner: PetOwner) -> dict[CareTask, str]:
    """Create a mapping of tasks to pet names for quick lookup."""
    task_to_pet = {}
    for pet in owner.pets:
        for task in pet.tasks:
            task_to_pet[task] = pet.name
    return task_to_pet


def print_section_header(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "-" * DIVIDER_WIDTH)
    print(title)
    print("-" * DIVIDER_WIDTH)


def print_task_details(task: CareTask, pet_name: str, task_number: int) -> None:
    """Print detailed information for a single task."""
    print(f"\n{task_number}. {task.name} ({pet_name})")
    print(f"   Description: {task.description}")
    print(f"   Duration: {task.duration} minutes")
    print(f"   Priority: {task.priority}/5")
    print(f"   Category: {task.category}")


def setup_sample_data() -> PetOwner:
    """Create sample owner, pets, and tasks for the demo."""
    owner = PetOwner(name="Jordan", available_minutes=120)

    # Add pets
    dog = Pet(name="Mochi", species="dog", age=3)
    cat = Pet(name="Whiskers", species="cat", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Task data: (pet, name, description, duration, priority, must_do, category)
    tasks_data = [
        (dog, "Morning Walk", "Take Mochi for a walk in the park", 30, 5, True, "exercise"),
        (dog, "Feed Dog", "Feed Mochi breakfast", 10, 5, True, "feeding"),
        (dog, "Play with Dog", "Interactive playtime with Mochi", 20, 3, False, "enrichment"),
        (cat, "Feed Cat", "Feed Whiskers breakfast and fresh water", 5, 5, True, "feeding"),
        (cat, "Change Litter Box", "Clean and refresh litter box", 15, 4, True, "cleaning"),
        (cat, "Play with Cat", "Fetch toy and interactive play", 15, 2, False, "enrichment"),
    ]

    for pet, *task_info in tasks_data:
        task = create_task(*task_info)
        pet.add_task(task)

    return owner


def print_schedule(owner: PetOwner, daily_plan) -> None:
    """Print the complete daily schedule to terminal."""
    print("\n" + "=" * DIVIDER_WIDTH)
    print("🐾 PawPal+ Today's Schedule 🐾".center(DIVIDER_WIDTH))
    print("=" * DIVIDER_WIDTH)

    print(f"\nOwner: {owner.name}")
    print(f"Available time: {owner.available_minutes} minutes")
    print(f"Pets: {', '.join(pet.name for pet in owner.pets)}")

    # Build task-to-pet mapping for efficient lookup
    task_to_pet = build_pet_task_map(owner)

    print_section_header("SELECTED TASKS FOR TODAY:")
    if daily_plan.selected_tasks:
        for i, task in enumerate(daily_plan.selected_tasks, 1):
            pet_name = task_to_pet.get(task, "Unknown")
            print_task_details(task, pet_name, i)
    else:
        print("  (None)")

    print_section_header("SKIPPED TASKS:")
    if daily_plan.skipped_tasks:
        for task in daily_plan.skipped_tasks:
            print(f"  • {task.name}")
    else:
        print("  (None)")

    print_section_header(
        f"TOTAL TIME: {daily_plan.total_time}/{owner.available_minutes} minutes"
    )

    print_section_header("SCHEDULING REASONING:")
    for reason in daily_plan.reasoning:
        print(f"  • {reason}")

    print("\n" + "=" * DIVIDER_WIDTH + "\n")


def main():
    """Main demo function."""
    owner = setup_sample_data()
    scheduler = Scheduler()
    all_tasks = owner.get_incomplete_tasks()
    daily_plan = scheduler.generate_plan(owner, all_tasks)
    print_schedule(owner, daily_plan)


if __name__ == "__main__":
    main()
