from SRC.Domain.GenericConstants import Fitness_Constants as FC, Realistic_Validations as RV
from SRC.Infrastructure.Validations import Check_String

class Fitness_Inforamation:
    BMI_Info: dict[str, float|str]
    BMR: float
    TDEE: float
    PFC: dict[str,int]

    def __init__(self, Gender:str = "M", Age:int = 20, Height:float = 180, Weight:float = 80, Weekly_Activity:int = 0, Goal:str = "G") -> None:
        CPFC_Info = CPFC_Calculate(Gender, Age, Height, Weight, Weekly_Activity, Goal)
        BMI_Info_Class = BMI_Information(Height, Weight)

        self.BMI_Info = BMI_Info_Class.bmi_info

        self.BMR = CPFC_Info.BMR
        self.TDEE = CPFC_Info.TDEE
        self.PFC = CPFC_Info.PFC
        
class BMI_Information():
    Height: float
    Weight: float

    BMI: float
    Category: str

    def __init__(self, Height: float, Weight: float) -> None:
        self._Height = Height
        self._Weight = Weight

        self.bmi_info = self._BMI_Calculate()

    def _BMI_Calculate(self) -> dict[str, float|str]:
        BMI:float = self._Weight/(self._Height/100)**2

        BMI_Info:dict[str, float|str] = {
            "BMI" : round(BMI, 1),
            "Category": FC.Get_BMICategory(BMI),
            "Recommended BMI" : f"{FC.Recommended_BMI['Min']} - {FC.Recommended_BMI['Max']}"
        }
        return BMI_Info

class CPFC_Calculate():
    Gender: str
    Age: int
    Height: float
    Weight: float
    Weekly_Activity: int
    Goal: str
    BMR: float
    TDEE: float
    PFC: dict[str,int]

    def __init__(self, Gender:str, Age:int, Height:float, Weight:float, Weekly_Activity:int, Goal:str) -> None:
        self.Gender = Gender
        self.Age = Age
        self.Height = Height
        self.Weight = Weight
        self.Weekly_Activity = Weekly_Activity
        self.Goal = Goal
        self.BMR = round(self._BMR_Calculate())
        self.TDEE = round(self._TDEE_Calculate())
        self.PFC = self._PFC_Calculate()
    
    def _BMR_Calculate(self) -> float:
        BMR:float = 10 * self.Weight + 6.25 * self.Height - 5 * self.Age
        BMR += FC.Metabolism[self.Gender]
        return BMR

    def _TDEE_Calculate(self) -> float:
        return self.BMR*FC.Value_Weekly_Activity[self.Weekly_Activity]
    
    def _PFC_Calculate(self) -> dict[str, int]:

        self.Goal_Value = FC.Value_Goals_For_Calculator[self.Goal.upper()]
        self.Kcal = self.TDEE

        self.Protein_Min = round(self.Weight * FC.Protein_Coeffs[self.Goal.upper()]["Min"])
        self.Protein_Max = round(self.Weight * FC.Protein_Coeffs[self.Goal.upper()]["Max"])

        self.Fats_Min = round(self.Weight * FC.Fat_Coeffs["Min"])
        self.Fats_Max = round(self.Weight * FC.Fat_Coeffs["Max"])

        self.Carbs_Min = round((self.Kcal - self.Protein_Max * FC.Kcalories_Per_Gramm["Protein"] - self.Fats_Max * FC.Kcalories_Per_Gramm["Fats"]) / FC.Kcalories_Per_Gramm["Carbs"])
        self.Carbs_Max = round((self.Kcal - self.Protein_Min * FC.Kcalories_Per_Gramm["Protein"] - self.Fats_Min * FC.Kcalories_Per_Gramm["Fats"]) / FC.Kcalories_Per_Gramm["Carbs"])

        self.PFC = {"Protein_Min": self.Protein_Min, "Protein_Max": self.Protein_Max,
                    "Fats_Min": self.Fats_Min, "Fats_Max": self.Fats_Max,
                    "Carbs_Min": self.Carbs_Min, "Carbs_Max": self.Carbs_Max}
        return self.PFC

