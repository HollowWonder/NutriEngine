from SRC.Domain.User import UserInfo, UserGoals
from SRC.Domain.Calculators import CPFCCalculator, DeficitCalculator, BMIInformation
from typing import Optional, TypedDict, Callable
from SRC.Infrastructure.Validations import check_numerical_input_value, check_str_input_value, check_str_len_value
from SRC.Domain.GenericConstants import TehnicalLimitations as TL, RealisticValidations as RV, FitnessConstants as FC


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
    
    def __init__(self, name: str = "TestUser", gender: str = "M", age: int = 20, height: float = 180, weight: float = 80, goal: str = "M", weekly_activity: int = 0, goal_weight: Optional[float] = None, mode: str = "normal") -> None:
        self._personality_user_info_class: UserInformation = UserInformation(name, gender, age, height, weight, goal, weekly_activity, goal_weight, mode)
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
    goal_weight: float
    deficit_mode: str

    def __init__(self) -> None:
        self.name = self.input_name()
        self.gender = self.input_gender()
        self.age = self.input_age()
        self.height = self.input_height()
        self.weight = self.input_weight()
        self.goal = self.input_goal()
        self.weekly_activity = self.input_weekly_activity()
        self.goal_weight = self.input_goal_weight(self.weight, self.goal)
        self.deficit_mode = self.input_deficit_mode(self.goal)
        self._user_profile_class = DefaultUserProfile(self.name,self.gender, self.age, self.height, self.weight, self.goal, self.weekly_activity, self.goal_weight, self.deficit_mode)
    
    def return_data_inputed_user_profile(self) -> UserProfileType:
        return self._user_profile_class.return_data_user_profile()

    @staticmethod
    def input_name() -> str:
        name: str = input("What's your name: ")
        check_name: Optional[str] = check_str_len_value(name, TL.MIN_LEN_NAME, TL.MAX_LEN_NAME)
        return check_name if check_name != None else name[:TL.MIN_LEN_NAME-2]
    
    @staticmethod
    def input_gender() -> str:
        gender: str = check_str_input_value("What's your gender: ", RV.LIST_OF_GENDERS)
        return gender
    
    @staticmethod
    def input_age() -> int:
        age: float = check_numerical_input_value("How old are you: ", RV.MIN_AGE, RV.MAX_AGE) 
        return int(age)
    
    @staticmethod
    def input_height() -> float:
        height: float = check_numerical_input_value("How tall are you (cm): ", RV.MIN_HEIGHT, RV.MAX_HEIGHT)
        return height
    
    @staticmethod
    def input_weight() -> float:
        weight: float = check_numerical_input_value("How much do you weigh (kg): ", RV.MIN_WEIGHT, RV.MAX_WEIGHT)
        return weight
    
    @staticmethod
    def input_goal() -> str:
        goal: str = check_str_input_value("Maintenance weight - M\nLose weight - L\nGain weight - G\nChoice: ", RV.VALID_GOALS)
        return goal
    
    @staticmethod
    def input_weekly_activity() -> int:
        weekly_activity: float = check_numerical_input_value("Workouts per week (0 if none): ", RV.MIN_ACTIVITY, RV.MAX_ACTIVITY)
        return int(weekly_activity)

    @staticmethod
    def input_goal_weight(weight: float, goal: str) -> float:
        goal_weight: float
        if goal != "M":
            weight_ranges: dict[str, dict[str, float]] = UserGoals.get_weight_range(weight)
            goal_weight = check_numerical_input_value("What weight do you want (kg): ", weight_ranges[goal]["min"], weight_ranges[goal]["max"])
        else:
            goal_weight = weight
        return goal_weight

    @staticmethod
    def input_deficit_mode(goal: str) -> str:
        list_of_deficit_modes: list[str] = list(FC.DEFICIT_MODE[goal].keys())
        dificit_mode: str = check_str_input_value(f"Choice deficit mode {list_of_deficit_modes}: ", list_of_deficit_modes)
        return dificit_mode
    
    @staticmethod
    def data_input_funtions() -> dict[str, Callable[..., str | int | float]]:
        data_funtions: dict[str, Callable[..., str | int | float]] = {
            "name" : InputUserProfile.input_name,
            "gender" : InputUserProfile.input_gender,
            "age": InputUserProfile.input_age,
            "height": InputUserProfile.input_height,
            "weight": InputUserProfile.input_weight,
            "goal": InputUserProfile.input_goal,
            "weekly_activity": InputUserProfile.input_weekly_activity,
            "goal_weight": InputUserProfile.input_goal_weight,
            "deficit_mode": InputUserProfile.input_deficit_mode
        }
        return data_funtions

class UserInformation:
    personality_user_info: dict[str, dict[str, str | int | float | None]]

    def __init__(self, name: str, gender: str, age: int, height: float, weight: float, goal: str, weekly_activity: int, goal_weight: Optional[float], mode: str) -> None:
        self._user_info:UserInfo = UserInfo(name, gender, age, height, weight)
        self._user_goals:UserGoals = UserGoals(weight, goal, weekly_activity, goal_weight, mode)
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
                "goal_weight": user_goals.goal_weight,
                "deficit_mode": user_goals.deficit_mode
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
