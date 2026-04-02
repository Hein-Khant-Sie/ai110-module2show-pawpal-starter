from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Pet:
    name: str
    species: str
    age: int


@dataclass
class CareTask:
    name: str
    duration: int
    priority: int
    must_do: bool
    category: str


@dataclass
class DailyPlan:
    selected_tasks: list[CareTask] = field(default_factory=list)
    skipped_tasks: list[CareTask] = field(default_factory=list)
    total_time: int = 0
    reasoning: list[str] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        pass

    def add_reason(self, reason: str) -> None:
        pass


@dataclass
class PetOwner:
    name: str
    available_minutes: int
    preferences: dict[str, Any] = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def update_preferences(self, preferences: dict[str, Any]) -> None:
        pass


class Scheduler:
    def sort_tasks(self, tasks: list[CareTask]) -> list[CareTask]:
        pass

    def generate_plan(self, owner: PetOwner, tasks: list[CareTask]) -> DailyPlan:
        pass
