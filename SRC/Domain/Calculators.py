from SRC.Domain.GenericConstants import Fitness_Constants as FC, Realistic_Validations as RV
from SRC.Infrastructure.Validations import check_str_value as csv

class Fitness_Information:
    BMI_Info: dict[str, float|str]
    BMR: float
    TDEE: float
    PFC: dict[str,float]
    deficit_info: dict[str, dict[str, float|dict[str, float]]]

    def __init__(self, Gender:str = "M", Age:int = 20, Height:float = 180, Weight:float = 80, Weekly_Activity:int = 0, Goal:str = "G", mode: str = "Normal") -> None:
        CPFC_Info = CPFC_Calculator(Gender, Age, Height, Weight, Weekly_Activity, Goal)
        BMI_Info_Class = BMI_Information(Height, Weight)

        self.BMI_Info = BMI_Info_Class.bmi_info

        self.BMR = CPFC_Info.BMR
        self.TDEE = CPFC_Info.TDEE
        self.PFC = CPFC_Info.PFC

        if Goal != "M":
            Deficit_Info = DeficitCalculator(self.TDEE, Weight, Goal, mode)
            self.deficit_info = Deficit_Info.Deficit_CPFC
        
class BMI_Information():
    def __init__(self, Height: float, Weight: float) -> None:
        self.bmi_info = self.BMI_Calculate(Weight, Height)

    @staticmethod
    def BMI_Calculate(weight:float, height:float) -> dict[str, float|str]:
        BMI:float = weight/(height/100)**2

        BMI_Info:dict[str, float|str] = {
            "BMI" : round(BMI, 1),
            "Category": FC.Get_BMICategory(BMI),
            "Recommended BMI" : f"{FC.Recommended_BMI['Min']} - {FC.Recommended_BMI['Max']}"
        }
        return BMI_Info

class CPFC_Calculator():
    BMR: float
    TDEE: float
    PFC: dict[str, float]

    def __init__(self, Gender:str = "M", Age:int = 20, Height:float = 180, Weight:float = 80, Weekly_Activity:int = 3, Goal:str = "G") -> None:
        self.BMR = self.BMR_Calculate(Weight, Height, Age, Gender)
        self.TDEE = self.TDEE_Calculate(self.BMR, Weekly_Activity)
        self.PFC = self.PFC_Calculate(Weight, self.TDEE, Goal)
    
    @staticmethod
    def BMR_Calculate(weight:float, height:float, age:float, gender:str) -> float:
        BMR:float = 10 * weight + 6.25 * height - 5 * age
        BMR += FC.Metabolism[gender]
        return round(BMR)

    @staticmethod
    def TDEE_Calculate(BMR:float, weekly_activity:int) -> float:
        return round(BMR*FC.Value_Weekly_Activity[weekly_activity])
    
    @staticmethod
    def PFC_Calculate(Weight:float, TDEE:float, Goal:str ) -> dict[str, float]:

        Goal_Value:int = FC.Value_Goals_For_Calculator[Goal.upper()]
        Kcal:float = TDEE

        Protein_Min:float = round(Weight * FC.Protein_Coeffs[Goal.upper()]["Min"])
        Protein_Max:float = round(Weight * FC.Protein_Coeffs[Goal.upper()]["Max"])

        Fats_Min:float = round(Weight * FC.Fat_Coeffs["Min"])
        Fats_Max:float = round(Weight * FC.Fat_Coeffs["Max"])

        Carbs_Min:float = round((Kcal - Protein_Max * FC.Kcalories_Per_Gramm["Protein"] - Fats_Max * FC.Kcalories_Per_Gramm["Fats"]) / FC.Kcalories_Per_Gramm["Carbs"])
        Carbs_Max:float = round((Kcal - Protein_Min * FC.Kcalories_Per_Gramm["Protein"] - Fats_Min * FC.Kcalories_Per_Gramm["Fats"]) / FC.Kcalories_Per_Gramm["Carbs"])

        PFC:dict[str,float] = {"Protein_Min": Protein_Min, "Protein_Max": Protein_Max,
                    "Fats_Min": Fats_Min, "Fats_Max": Fats_Max,
                    "Carbs_Min": Carbs_Min, "Carbs_Max": Carbs_Max}
        return PFC

class DeficitCalculator():
    Deficit_CPFC:dict[str, dict[str, float|dict[str, float]]]

    def __init__(self, TDEE:float = 2000, Weight:float = 80, Goal:str = "G", Mode:str = "Normal") -> None:
        self.Deficit_CPFC = self.Collect_Deficit_Data(TDEE, Weight, Goal, Mode)
    
    @staticmethod
    def Calories_Calculate(TDEE:float, goal:str, coef_dificit:int) -> float:
        return TDEE * (1 + FC.Value_Goals_For_Calculator[goal]*(coef_dificit/100))
    
    @staticmethod
    def Collect_Deficit_Data(TDEE:float, weight:float, goal:str, mode:str) -> dict[str, dict[str, float|dict[str, float]]]:
        deficit_modes:list[str] = list(FC.Deficit_Mode[goal].keys())
        valid_mode:str|None = csv(mode, deficit_modes)
        if valid_mode == None:
            valid_mode = deficit_modes[0]

        coeficients:tuple[int,int] = FC.Deficit_Mode[goal][valid_mode]
        Deficit_CPFC:dict[str, dict[str, float|dict[str, float]]] = {}
        for deficit in coeficients:
            kcal:float = round(DeficitCalculator.Calories_Calculate(TDEE, goal, deficit))
            Deficit_CPFC[str(deficit)] = {
                "Kcal" : kcal,
                "PFC" : CPFC_Calculator.PFC_Calculate(weight, kcal, goal)
            }
        return Deficit_CPFC
        