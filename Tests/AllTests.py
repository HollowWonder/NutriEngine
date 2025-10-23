import pytest
from typing import Optional
from SRC.Domain.Calculators import Fitness_Calculate, CPFC_Inforamation
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
    Common_Test_Data: list[tuple[str,int,float,float,int,str]] = [
        ("M", 25, 180.0, 75.0, 3, "G"),
        ("W", 30, 165.0, 60.0, 2, "L"), 
        ("M", 22, 175.0, 70.0, 4, "G"),
        ("W", 28, 160.0, 55.0, 1, "L")
    ]

    @pytest.mark.parametrize("Gender, Age, Height, Weight, Weekly_Activity, Goal", Common_Test_Data)
    def test_Info(self, Gender:str, Age:int, Height:float, Weight:float, Weekly_Activity:int, Goal:str) -> None:
        Fitness_Info = Fitness_Calculate(Gender, Age, Height, Weight, Weekly_Activity, Goal)
        CPFC_Info = CPFC_Inforamation(Gender, Age, Height, Weight, Weekly_Activity, Goal)

        assert Fitness_Info.Gender == Gender
        assert Fitness_Info.Age == Age
        assert Fitness_Info.Height == Height
        assert Fitness_Info.Weight == Weight
        assert Fitness_Info.Weekly_Activity == Weekly_Activity
        assert Fitness_Info.Goal == Goal

        assert (Fitness_Info.BMR == CPFC_Info.BMR) != 0
        assert (Fitness_Info.TDEE == CPFC_Info.TDEE) != 0
        assert (Fitness_Info.PFC == CPFC_Info.PFC) != None

    @pytest.mark.parametrize("Gender, Age, Height, Weight, Weekly_Activity, Goal", Common_Test_Data)

    def test_result(self, Gender:str, Age:int, Height:float, Weight:float, Weekly_Activity:int, Goal:str) -> None:
        CPFC_Info = CPFC_Inforamation(Gender, Age, Height, Weight, Weekly_Activity, Goal)

        assert CPFC_Info.BMR == round(10 * Weight + 6.25 * Height - 5 * Age + FC.Metabolism[Gender.upper()])
        assert CPFC_Info.TDEE == round(CPFC_Info.BMR * FC.Value_Weekly_Activity[Weekly_Activity])
        Protein_Min = round(Weight * FC.Protein_Coeffs[Goal.upper()]["Min"])
        Protein_Max = round(Weight * FC.Protein_Coeffs[Goal.upper()]["Max"])

        Fats_Min = round(Weight * FC.Fat_Coeffs["Min"])
        Fats_Max = round(Weight * FC.Fat_Coeffs["Max"])

        Carbs_Min = round((CPFC_Info.TDEE - Protein_Max * FC.Kcalories_Per_Gramm["Protein"] - Fats_Max * FC.Kcalories_Per_Gramm["Fats"]) / FC.Kcalories_Per_Gramm["Carbs"])
        Carbs_Max = round((CPFC_Info.TDEE - Protein_Min * FC.Kcalories_Per_Gramm["Protein"] - Fats_Min * FC.Kcalories_Per_Gramm["Fats"]) / FC.Kcalories_Per_Gramm["Carbs"])

        assert CPFC_Info.PFC == {"Protein_Min": Protein_Min, "Protein_Max": Protein_Max,
                        "Fats_Min": Fats_Min, "Fats_Max": Fats_Max,
                        "Carbs_Min": Carbs_Min, "Carbs_Max": Carbs_Max}