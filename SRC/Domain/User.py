from SRC.Infrastructure.Validations import check_numerical_inputvalue, check_str_inputvalue
from SRC.Domain.GenericConstants import Realistic_Validations as RV
from typing import Optional
from dataclasses import dataclass

class User:
    def __init__(self) -> None:
        self.Info = UserInfo()
        self.Goals = UserGoals(self.Info.Weight)
    def Collect_Data(self) -> None:
        self.Info.input_info()
        self.Goals.Current_Weight = self.Info.Weight
        self.Goals.input_goals()

@dataclass
class UserInfo:
    Name: str
    Gender: str
    Age: int
    Height: float
    Weight: float

    def __init__(self, Name:str="TestUser", Gender:str="M", Age:int=20, Height:float=180, Weight:float=80) -> None:
        self.Name = Name
        self.Gender= Gender
        self.Age = Age
        self.Height = Height
        self.Weight = Weight
    
    def input_info(self) -> None:
        self.Name = input("What's your name: ")
        self.Gender = check_str_inputvalue("What's your gender: ", RV.List_Of_Genders)
        self.Age = check_numerical_inputvalue("How old are you: ", RV.Min_Age, RV.Max_Age)
        self.Height = check_numerical_inputvalue("How tall are you (cm): ", RV.Min_Height, RV.Max_Height)
        self.Weight = check_numerical_inputvalue("How much do you weigh (kg): ", RV.Min_Weight, RV.Max_Weight)

@dataclass
class UserGoals:
    Current_Weight: float
    Goal: str
    Weekly_Activity: int
    Goal_Weight: float|None

    def __init__(self, Current_Weight:float=60, Goal:str="M", Weekly_Activity:int=0, Goal_Weight:Optional[float]=None) -> None:
        self.Current_Weight = Current_Weight
        self.Goal = Goal
        self.Weekly_Activity = Weekly_Activity
        self.Goal_Weight= Goal_Weight
        

    def input_goals(self) -> None:
        Weight_Ranges:dict[str, dict[str,float]] = {
            "M": {"Min":self.Current_Weight, "Max":self.Current_Weight},
            "G": {"Min":self.Current_Weight+1, "Max":RV.Max_Weight},
            "L": {"Min":RV.Min_Weight, "Max":self.Current_Weight-1}
        }
        
        self.Goal = check_str_inputvalue("Maintenance weight - M\nLose weight - L\nGain weight - G\nChoice: ", RV.Valid_Goals)
        self.Weekly_Activity = check_numerical_inputvalue("Workouts per week (0 if none): ", RV.Min_Activity, RV.Max_Activity)

        if self.Goal != "M":
            self.Goal_Weight = check_numerical_inputvalue("What weight do you want (kg): ", Weight_Ranges[self.Goal]["Min"], Weight_Ranges[self.Goal]["Max"])
        else:
            self.Goal_Weight = self.Current_Weight