import pytest
from typing import Optional
from SRC.Domain.Calculators import CPFC_Calculator, BMI_Information, DeficitCalculator
from SRC.Domain.User import UserInfo, UserGoals
from SRC.Domain.GenericConstants import Fitness_Constants as FC, Realistic_Validations as RV

class Test_User_Data:
    
    @pytest.mark.parametrize("Name,Gender,Age,Height,Weight", [
        ("Bob", "M", 20, 190, 90),
        ("Mike", "M", 19, 170, 70),
        ("Tom", "m", 22, 192, 88),
        ("Alica", "w", 27, 170, 60),
        ("Rose", "w", 30, 166, 66),
        ("Amelie", "w", 22, 162, 56),
        ("Lily", "w", 17, 180, 69)
    ])

    def test_UserInfo(self, Name:str, Gender:str, Age:int, Height:float, Weight:float) -> None:
        User_Info = UserInfo(Name, Gender, Age, Height, Weight)

        assert User_Info.Name == Name
        assert User_Info.Gender == Gender
        assert User_Info.Age == Age
        assert User_Info.Height == Height
        assert User_Info.Weight == Weight

    @pytest.mark.parametrize("Current_Weight,Goal,Weekly_Activity,Goal_Weight",[
        (60, "l", 4, 59),
        (70, "G", 7, 80),
        (80, "M", 2, 90),
        (66, "m", 1, None)
    ])
    def test_UserGoals(self, Current_Weight:int, Goal:str, Weekly_Activity:int, Goal_Weight:Optional[float]) -> None:
        Goals = UserGoals(Current_Weight, Goal, Weekly_Activity, Goal_Weight)

        assert Goals.Current_Weight == Current_Weight
        assert Goals.Goal == Goal
        assert Goals.Weekly_Activity == Weekly_Activity
        assert Goals.Goal_Weight == Goal_Weight

class Test_Calculator():
    Common_Test_Data: list[tuple[str,int,float,float,int,str,str]] = [
        ("M", 25, 180.0, 75.0, 3, "G", "Normal"),
        ("W", 30, 165.0, 60.0, 2, "L", "Extra"), 
        ("M", 22, 175.0, 70.0, 4, "G", "Normal"),
        ("W", 28, 160.0, 55.0, 1, "L", "normal")
    ]

    @pytest.mark.parametrize("gender, age, height, weight, weekly_activity, goal, mode", Common_Test_Data)

    def test_result(self, gender:str, age:int, height:float, weight:float, weekly_activity:int, goal:str, mode:str) -> None:
        CPFC_Info:CPFC_Calculator = CPFC_Calculator(gender, age, height, weight, weekly_activity, goal)
        Bmi_Info:BMI_Information = BMI_Information(height, weight)

        bmi_info:dict[str, float|str] = BMI_Information.BMI_Calculate(weight, height)
        bmr:float = CPFC_Calculator.BMR_Calculate(weight, height, age, gender)
        tdee:float = CPFC_Calculator.TDEE_Calculate(bmr, weekly_activity)
        pfc:dict[str,float] = CPFC_Calculator.PFC_Calculate(weight, tdee, goal)

        Deficit_Info:DeficitCalculator = DeficitCalculator(tdee, weight, goal, mode)
        deficit_info:dict[str, dict[str, float|dict[str, float]]] = DeficitCalculator.Collect_Deficit_Data(tdee,weight,goal,mode)


        assert Bmi_Info.bmi_info == bmi_info
        assert CPFC_Info.BMR == bmr
        assert CPFC_Info.TDEE == tdee
        assert CPFC_Info.PFC == pfc
        assert Deficit_Info.Deficit_CPFC == deficit_info