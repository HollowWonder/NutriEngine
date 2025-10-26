from SRC.Domain.GenericConstants import Fitness_Constants as FC, Realistic_Validations as RV

class Fitness_Inforamation:
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

class CPFC_Calculator():
    Gender: str
    Age: int
    Height: float
    Weight: float
    Weekly_Activity: int
    Goal: str
    BMR: float
    TDEE: float

    def __init__(self, Gender:str = "M", Age:int = 20, Height:float = 180, Weight:float = 80, Weekly_Activity:int = 3, Goal:str = "G") -> None:
        self.Gender = Gender
        self.Age = Age
        self.Height = Height
        self.Weight = Weight
        self.Weekly_Activity = Weekly_Activity
        self.Goal = Goal
        self.BMR = round(self._BMR_Calculate())
        self.TDEE = round(self._TDEE_Calculate())
        self.PFC = self.PFC_Calculate(self.Weight, self.TDEE, self.Goal)
    
    def _BMR_Calculate(self) -> float:
        BMR:float = 10 * self.Weight + 6.25 * self.Height - 5 * self.Age
        BMR += FC.Metabolism[self.Gender]
        return BMR

    def _TDEE_Calculate(self) -> float:
        return self.BMR*FC.Value_Weekly_Activity[self.Weekly_Activity]
    
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
        self._Goal:str = Goal
        self._TDEE:float = TDEE
        self._Weight:float = Weight

        coeficients:tuple[int,int] = FC.Deficit_Mode[self._Goal][Mode]

        CPFC_Class = CPFC_Calculator()
        self.Deficit_CPFC = self._Collect_Deficit_Data(coeficients)
    
    def _Calories_Calculate(self, coef_dificit:int) -> float:
        return self._TDEE * (1 + FC.Value_Goals_For_Calculator[self._Goal]*(coef_dificit/100))
    
    def _Collect_Deficit_Data(self, coeficients:tuple[int,int]) -> dict[str, dict[str, float|dict[str, float]]]:
        Deficit_CPFC:dict[str, dict[str, float|dict[str, float]]] = {}
        for deficit in coeficients:
            kcal:float = round(self._Calories_Calculate(deficit))
            Deficit_CPFC[str(deficit)] = {
                "Kcal" : kcal,
                "PFC" : CPFC_Calculator.PFC_Calculate(self._Weight, kcal, self._Goal)
            }
        return Deficit_CPFC
        