from __future__ import annotations

from datetime import date, timedelta
from dataclasses import dataclass, field, replace
from itertools import combinations
from typing import Any


@dataclass
class CareTask:
    """Represents a single care activity for a pet."""
    name: str
    description: str
    duration: int  # in minutes
    frequency: str  # e.g., "daily", "weekly", "as-needed"
    priority: int  # 1-5, higher is more important
    must_do: bool
    category: str  # e.g., "feeding", "walking", "grooming"
    pet_name: str = ""
    time: str = ""  # scheduled time in "HH:MM" format, e.g. "08:00"
    due_date: date | None = None  # scheduled date as a date object
    completed: bool = False

    def mark_complete(self) -> CareTask | None:
        """Mark this task as completed.

        If the task is daily or weekly, returns the next occurrence.
        Otherwise returns None.
        """
        self.completed = True
        if self.frequency in ("daily", "weekly"):
            return self.create_next_occurrence()
        return None

    def mark_incomplete(self) -> None:
        """Set this task's completed status to False."""
        self.completed = False

    def create_next_occurrence(self) -> CareTask:
        """Return a copy of this task scheduled for the next occurrence.

        - "daily"  → 1 day later
        - "weekly" → 7 days later
        - anything else → 1 day later
        """
        base = self.due_date if self.due_date else date.today()
        days = 7 if self.frequency == "weekly" else 1
        next_due = base + timedelta(days=days)
        return replace(self, due_date=next_due, completed=False)


@dataclass
class Pet:
    """Represents a pet with its associated care tasks."""
    name: str
    species: str
    age: int
    tasks: list[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Add one care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: CareTask) -> None:
        """Remove one care task from this pet if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> list[CareTask]:
        """Return all tasks assigned to this pet."""
        return self.tasks

    def get_incomplete_tasks(self) -> list[CareTask]:
        """Return only tasks for this pet that are not completed."""
        return [task for task in self.tasks if not task.completed]


@dataclass
class DailyPlan:
    """Represents a plan for a specific day."""
    selected_tasks: list[CareTask] = field(default_factory=list)
    skipped_tasks: list[CareTask] = field(default_factory=list)
    total_time: int = 0
    reasoning: list[str] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Add a task to today's selected tasks and update total time."""
        self.selected_tasks.append(task)
        self.total_time += task.duration

    def skip_task(self, task: CareTask, reason: str) -> None:
        """Add a task to skipped tasks and store why it was skipped."""
        self.skipped_tasks.append(task)
        self.reasoning.append(f"Skipped '{task.name}': {reason}")

    def add_reason(self, reason: str) -> None:
        """Add one reason message to the plan notes."""
        self.reasoning.append(reason)

    def summarize(self) -> str:
        """Return a text summary of the daily plan."""
        summary = f"Daily Plan Summary:\n"
        summary += f"Selected tasks: {len(self.selected_tasks)}\n"
        summary += f"Skipped tasks: {len(self.skipped_tasks)}\n"
        summary += f"Total time: {self.total_time} minutes\n"
        if self.reasoning:
            summary += "Reasoning:\n"
            for reason in self.reasoning:
                summary += f"  - {reason}\n"
        return summary


@dataclass
class PetOwner:
    """Represents a pet owner managing one or more pets."""
    name: str
    available_minutes: int
    preferences: dict[str, Any] = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add one pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove one pet from this owner's pet list if it exists."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> list[CareTask]:
        """Return every task from all pets owned by this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_incomplete_tasks(self) -> list[CareTask]:
        """Return incomplete tasks from all pets owned by this owner."""
        incomplete = []
        for pet in self.pets:
            incomplete.extend(pet.get_incomplete_tasks())
        return incomplete

    def update_preferences(self, preferences: dict[str, Any]) -> None:
        """Update this owner's preferences with new values."""
        self.preferences.update(preferences)


class Scheduler:
    """The brain of the scheduling system, organizes tasks across pets."""

    def detect_conflicts(self, tasks: list[CareTask]) -> list[str]:
        """Check for tasks scheduled at the same time and return warning messages.

        Returns an empty list if no conflicts are found.
        """
        warnings = []
        # Group tasks by their time value, skipping tasks with no time set
        time_groups: dict[str, list[CareTask]] = {}
        for task in tasks:
            if not task.time:
                continue
            time_groups.setdefault(task.time, []).append(task)

        for time_slot, grouped in time_groups.items():
            for a, b in combinations(grouped, 2):
                if a.pet_name == b.pet_name:
                    warnings.append(
                        f"Conflict at {time_slot}: '{a.name}' and '{b.name}' "
                        f"are both scheduled for {a.pet_name or 'the same pet'}."
                    )
                else:
                    warnings.append(
                        f"Conflict at {time_slot}: '{a.name}' ({a.pet_name or 'unknown'}) "
                        f"and '{b.name}' ({b.pet_name or 'unknown'}) overlap."
                    )
        return warnings

    def filter_by_status(self, tasks: list[CareTask], completed: bool) -> list[CareTask]:
        """Return tasks that match the given completion status."""
        return [t for t in tasks if t.completed == completed]

    def filter_by_pet(self, tasks: list[CareTask], pet_name: str) -> list[CareTask]:
        """Return only tasks assigned to the given pet."""
        return [t for t in tasks if t.pet_name == pet_name]

    def sort_by_time(self, tasks: list[CareTask]) -> list[CareTask]:
        """Return tasks sorted by scheduled time in ascending order."""
        return sorted(tasks, key=lambda t: t.time)

    def sort_tasks(self, tasks: list[CareTask], reverse: bool = True) -> list[CareTask]:
        """Return tasks sorted by priority, highest first by default."""
        return sorted(tasks, key=lambda t: t.priority, reverse=reverse)

    def filter_must_do_tasks(self, tasks: list[CareTask]) -> list[CareTask]:
        """Return only tasks that are marked as must-do."""
        return [task for task in tasks if task.must_do]

    def retrieve_all_tasks(self, owner: PetOwner) -> list[CareTask]:
        """Return all incomplete tasks for the given owner."""
        return owner.get_incomplete_tasks()

    def generate_plan(self, owner: PetOwner, tasks: list[CareTask]) -> DailyPlan:
        """Build a daily plan that fits within the owner's available time."""
        plan = DailyPlan()

        # Step 1: Add must-do tasks first
        must_do_tasks = self.filter_must_do_tasks(tasks)
        sorted_must_do = self.sort_tasks(must_do_tasks)

        for task in sorted_must_do:
            if plan.total_time + task.duration <= owner.available_minutes:
                plan.add_task(task)
                plan.add_reason(
                    f"Added must-do task '{task.name}' (priority: {task.priority})")
            else:
                plan.skip_task(task, "Insufficient time remaining")

        # Step 2: Add optional tasks by priority if space allows
        optional_tasks = [t for t in tasks if not t.must_do]
        sorted_optional = self.sort_tasks(optional_tasks)

        for task in sorted_optional:
            if plan.total_time + task.duration <= owner.available_minutes:
                plan.add_task(task)
                plan.add_reason(
                    f"Added task '{task.name}' (priority: {task.priority})")
            else:
                plan.skip_task(task, "Time constraint")

        # Step 3: Add overall summary
        plan.add_reason(
            f"Plan uses {plan.total_time}/{owner.available_minutes} available minutes"
        )

        return plan
