from typing import Optional
from dataclasses import dataclass

@dataclass
class UserInfo:
    name: str
    gender: str
    age: int
    height: float
    weight: float

    def __init__(self, name: str, gender: str, age: int, height: float, weight: float) -> None:
        self.name = name
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight


@dataclass
class UserGoals:
    goal: str
    weekly_activity: int
    goal_weight: Optional[float]

    def __init__(self, _current_weight: float, goal: str, weekly_activity: int, goal_weight: Optional[float]) -> None:
        self._current_weight:float = _current_weight
        self.goal = goal
        self.weekly_activity = weekly_activity
        self.goal_weight = goal_weight