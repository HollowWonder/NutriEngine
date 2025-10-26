from SRC.Domain.User import UserInfo, UserGoals
from SRC.Domain.Calculators import CPFCCalculator, DeficitCalculator, BMIInformation
from typing import Optional, TypedDict
from SRC.Domain.GenericConstants import FitnessConstants as FC
from SRC.Infrastructure.Validations import check_numerical_input_value, check_str_input_value
from SRC.Domain.GenericConstants import RealisticValidations as RV


class FitnessInformationType(TypedDict):
    bmi_info: dict[str, float | str]
    bmr: float
    tdee: float
    pfc: dict[str, float]
    deficit_info: dict[str, dict[str, float | dict[str, float]]] | None

class UserProfileType(TypedDict):
    personality_user_info: dict[str, dict[str, str | int | float | None]]
    fitness_info: FitnessInformationType

# alternative type: dict[str, Any]    

class DefaultUserProfile:
    _personality_user_info: dict[str, dict[str, str | int | float | None]]
    _fitness_info: FitnessInformationType

    def __init__(self, name: str = "TestUser", gender: str = "M", age: int = 20, height: float = 180, weight: float = 80, goal: str = "M", weekly_activity: int = 0, goal_weight: Optional[float] = None, mode: str = "mormal") -> None:
        self._personality_user_info_class: UserInformation = UserInformation(name, gender, age, height, weight, goal, weekly_activity, goal_weight)
        self._fitness_info_class = FitnessInformation(gender, age, height, weight, weekly_activity, goal, mode)

    def return_data_user_profile(self) -> UserProfileType:
        self._personality_user_info = self._personality_user_info_class.personality_user_info
        self._fitness_info = self._fitness_info_class.fitness_info

        return {
            "personality_user_info": self._personality_user_info,
            "fitness_info": self._fitness_info
        }

class InputUserProfile:
    name: str
    gender: str
    age: int
    height: float
    weight: float
    goal: str
    weekly_activity: int
    goal_weight: Optional[float]
    mode: str

    def __init__(self) -> None:
        self._input_user_info()
        self._input_user_goals()
        if self.goal != "M":
            self._choice_deficit_mode()
        else:
            self.mode = "Normal"
        self._user_profile_class = DefaultUserProfile(self.name,self.gender, self.age, self.height, self.weight, self.goal, self.weekly_activity, self.goal_weight, self.mode)
    
    def return_data_inputed_user_profile(self) -> UserProfileType:
        return self._user_profile_class.return_data_user_profile()
    
    def _input_user_info(self) -> None:
        self.name = input("What's your name: ")
        self.gender = check_str_input_value("What's your gender: ", RV.LIST_OF_GENDERS)
        self.age = int(check_numerical_input_value("How old are you: ", RV.MIN_AGE, RV.MAX_AGE))
        self.height = check_numerical_input_value("How tall are you (cm): ", RV.MIN_HEIGHT, RV.MAX_HEIGHT)
        self.weight = check_numerical_input_value("How much do you weigh (kg): ", RV.MIN_WEIGHT, RV.MAX_WEIGHT)
    
    def _input_user_goals(self) -> None:
        weight_ranges: dict[str, dict[str, float]] = {
            "M": {"min": self.weight, "max": self.weight},
            "G": {"min": self.weight + 1, "max": RV.MAX_WEIGHT},
            "L": {"min": RV.MIN_WEIGHT, "max": self.weight - 1}
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
            self.goal_weight = self.weight
    
    def _choice_deficit_mode(self) -> None:
        list_deficit_mode: list[str] = list(mode for mode in FC.DEFICIT_MODE[self.goal].keys())

        self.mode = check_str_input_value(f"Choice deficit mode {list_deficit_mode}: ", list_deficit_mode)

class UserInformation:
    personality_user_info: dict[str, dict[str, str | int | float | None]]

    def __init__(self, name: str, gender: str, age: int, height: float, weight: float, goal: str, weekly_activity: int, goal_weight: Optional[float]) -> None:
        self._user_info:UserInfo = UserInfo(name, gender, age, height, weight)
        self._user_goals:UserGoals = UserGoals(weight, goal, weekly_activity, goal_weight)
        self._collect_info(self._user_info, self._user_goals)

    def _collect_info(self, information_about_user: 'UserInfo', information_about_user_goals: 'UserGoals') -> None:
        user_info:UserInfo = information_about_user
        user_goals:UserGoals = information_about_user_goals

        self.personality_user_info  = {
            "user_info": {
                "name": user_info.name,
                "gender": user_info.gender,
                "age": user_info.age,
                "height": user_info.height,
                "weight": user_info.weight
            },
            "user_goals": {
                "goal": user_goals.goal,
                "weekly_activity": user_goals.weekly_activity,
                "goal_weight": user_goals.goal_weight
            }
        }

class FitnessInformation:
    #Type: for bmi_info, for cpfc_info, for dificit_info
    fitness_info: FitnessInformationType

    _bmi_info:BMIInformation
    _cpfc_info:CPFCCalculator
    _deficit_cpfc:dict[str, dict[str, float | dict[str, float]]] | None

    def __init__(self, gender: str, age: int, height: float, weight: float, weekly_activity: int, goal: str, mode: str) -> None:
        self._bmi_info = BMIInformation(height, weight)
        self._cpfc_info = CPFCCalculator(gender, age, height, weight, weekly_activity, goal)
        tdee = self._cpfc_info.tdee
        if goal != "M":
            deficit_info = DeficitCalculator(tdee, weight, goal, mode)
            self._deficit_cpfc = deficit_info.deficit_cpfc
        else:
            self._deficit_cpfc = None
        
        self._collect_result()

    def _collect_result(self) -> None:
        self.fitness_info = {
            "bmi_info": self._bmi_info.bmi_info,
            "bmr": self._cpfc_info.bmr,
            "tdee": self._cpfc_info.tdee,
            "pfc": self._cpfc_info.pfc,
            "deficit_info": self._deficit_cpfc
        }
        