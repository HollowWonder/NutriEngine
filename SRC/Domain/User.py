from typing import Optional
from dataclasses import dataclass
from SRC.Domain.GenericConstants import TehnicalLimitations as TL, RealisticValidations as RV, FitnessConstants as FC
from SRC.Infrastructure.Validations import check_str_value, check_numerical_value, check_str_len_value

@dataclass
class UserInfo:
    name: str
    gender: str
    age: int
    height: float
    weight: float

    def __init__(self, name: str, gender: str, age: int, height: float, weight: float) -> None:
        check_name: Optional[str] = check_str_len_value(name, TL.MIN_LEN_NAME, TL.MAX_LEN_NAME)
        self.name = check_name if check_name != None else "Jo"

        check_gender: Optional[str] | None= check_str_value(gender, RV.LIST_OF_GENDERS)
        self.gender = check_gender if check_gender != None else "M"

        check_age: Optional[float] = check_numerical_value(age, RV.MIN_AGE, RV.MAX_AGE) 
        self.age = int(check_age) if check_age != None else 20

        check_height: Optional[float] = check_numerical_value(height, RV.MIN_HEIGHT, RV.MAX_HEIGHT)
        self.height = check_height if check_height != None else 180

        check_weight: Optional[float] = check_numerical_value(weight, RV.MIN_WEIGHT, RV.MAX_WEIGHT)
        self.weight = check_weight if check_weight != None else 80


@dataclass
class UserGoals:
    current_weight: float
    goal: str
    weekly_activity: int
    goal_weight: Optional[float]
    deficit_mode: str

    def __init__(self, current_weight: float, goal: str, weekly_activity: int, goal_weight: Optional[float], mode: str) -> None:
        self.current_weight = current_weight

        check_goal: Optional[str] = check_str_value(goal, RV.VALID_GOALS)
        self.goal = check_goal if check_goal != None else "M"

        check_weekly_activity: Optional[float] = check_numerical_value(weekly_activity, RV.MIN_ACTIVITY, RV.MAX_ACTIVITY)
        self.weekly_activity = int(check_weekly_activity) if check_weekly_activity != None else 0

        if self.goal != "M":
            weight_ranges: dict[str, dict[str, float]] = self.get_weight_range(current_weight)

            if goal_weight != None:
                check_goal_weight: Optional[float] = check_numerical_value(goal_weight, weight_ranges[self.goal]["min"], weight_ranges[self.goal]["max"])
                self.goal_weight = check_goal_weight if check_goal_weight != None else self.current_weight + 10 * FC.VALUE_GOALS_FOR_CALCULATOR[self.goal]
            else:
                self.goal_weight = current_weight + FC.VALUE_GOALS_FOR_CALCULATOR[self.goal] * 10
            list_of_deficit_modes: list[str] = list(FC.DEFICIT_MODE[self.goal].keys())
            check_dificit_mode: Optional[str] = check_str_value(mode, list_of_deficit_modes)
            self.deficit_mode = check_dificit_mode if check_dificit_mode != None else "normal"
        else:
            self.goal_weight = self.current_weight
            self.deficit_mode = "normal"

    
    @staticmethod
    def get_weight_range(weight) -> dict[str, dict[str, float]]:
        return {
            "M": {"min": weight, "max": weight},
            "G": {"min": weight + 1, "max": RV.MAX_WEIGHT},
            "L": {"min": RV.MIN_WEIGHT, "max": weight}
        }