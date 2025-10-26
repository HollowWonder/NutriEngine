from SRC.Infrastructure.Validations import check_numerical_input_value, check_str_input_value
from SRC.Domain.GenericConstants import RealisticValidations as RV
from typing import Optional
from dataclasses import dataclass


class User:
    def __init__(self) -> None:
        self.info = UserInfo()
        self.goals = UserGoals(self.info.weight)
    
    def collect_data(self) -> None:
        self.info.input_info()
        self.goals.current_weight = self.info.weight
        self.goals.input_goals()


@dataclass
class UserInfo:
    name: str
    gender: str
    age: int
    height: float
    weight: float

    def __init__(self, name: str = "TestUser", gender: str = "M", age: int = 20, 
                 height: float = 180, weight: float = 80) -> None:
        self.name = name
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight
    
    def input_info(self) -> None:
        self.name = input("What's your name: ")
        self.gender = check_str_input_value("What's your gender: ", RV.LIST_OF_GENDERS)
        self.age = int(check_numerical_input_value("How old are you: ", RV.MIN_AGE, RV.MAX_AGE))
        self.height = check_numerical_input_value("How tall are you (cm): ", RV.MIN_HEIGHT, RV.MAX_HEIGHT)
        self.weight = check_numerical_input_value("How much do you weigh (kg): ", RV.MIN_WEIGHT, RV.MAX_WEIGHT)


@dataclass
class UserGoals:
    current_weight: float
    goal: str
    weekly_activity: int
    goal_weight: Optional[float]

    def __init__(self, current_weight: float = 60, goal: str = "M", 
                 weekly_activity: int = 0, goal_weight: Optional[float] = None) -> None:
        self.current_weight = current_weight
        self.goal = goal
        self.weekly_activity = weekly_activity
        self.goal_weight = goal_weight
        
    def input_goals(self) -> None:
        weight_ranges: dict[str, dict[str, float]] = {
            "M": {"min": self.current_weight, "max": self.current_weight},
            "G": {"min": self.current_weight + 1, "max": RV.MAX_WEIGHT},
            "L": {"min": RV.MIN_WEIGHT, "max": self.current_weight - 1}
        }
        
        self.goal = check_str_input_value(
            "Maintenance weight - M\nLose weight - L\nGain weight - G\nChoice: ", 
            RV.VALID_GOALS
        )
        self.weekly_activity = int(check_numerical_input_value(
            "Workouts per week (0 if none): ", RV.MIN_ACTIVITY, RV.MAX_ACTIVITY
        ))

        if self.goal != "M":
            self.goal_weight = check_numerical_input_value(
                "What weight do you want (kg): ", 
                weight_ranges[self.goal]["min"], 
                weight_ranges[self.goal]["max"]
            )
        else:
            self.goal_weight = self.current_weight