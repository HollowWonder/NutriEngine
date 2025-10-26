from SRC.Domain.GenericConstants import FitnessConstants as FC, RealisticValidations as RV
from SRC.Infrastructure.Validations import check_str_value

     
class BMIInformation:
    def __init__(self, height: float, weight: float) -> None:
        self.bmi_info = self.bmi_calculate(weight, height)

    @staticmethod
    def bmi_calculate(weight: float, height: float) -> dict[str, float | str]:
        bmi: float = weight / (height / 100) ** 2

        bmi_info: dict[str, float | str] = {
            "bmi": round(bmi, 1),
            "category": FC.get_bmi_category(bmi),
            "recommended_bmi": f"{FC.RECOMMENDED_BMI['min']} - {FC.RECOMMENDED_BMI['max']}"
        }
        return bmi_info


class CPFCCalculator:
    bmr: float
    tdee: float
    pfc: dict[str, float]

    def __init__(self, gender: str = "M", age: int = 20, height: float = 180, 
                 weight: float = 80, weekly_activity: int = 3, goal: str = "G") -> None:
        self.bmr = self.bmr_calculate(weight, height, age, gender)
        self.tdee = self.tdee_calculate(self.bmr, weekly_activity)
        self.pfc = self.pfc_calculate(weight, self.tdee, goal)
    
    @staticmethod
    def bmr_calculate(weight: float, height: float, age: float, gender: str) -> float:
        bmr: float = 10 * weight + 6.25 * height - 5 * age
        bmr += FC.METABOLISM[gender]
        return round(bmr)

    @staticmethod
    def tdee_calculate(bmr: float, weekly_activity: int) -> float:
        return round(bmr * FC.VALUE_WEEKLY_ACTIVITY[weekly_activity])
    
    @staticmethod
    def pfc_calculate(weight: float, tdee: float, goal: str) -> dict[str, float]:
        goal_value: int = FC.VALUE_GOALS_FOR_CALCULATOR[goal.upper()]
        kcal: float = tdee

        protein_min: float = round(weight * FC.PROTEIN_COEFFS[goal.upper()]["min"])
        protein_max: float = round(weight * FC.PROTEIN_COEFFS[goal.upper()]["max"])

        fats_min: float = round(weight * FC.FAT_COEFFS["min"])
        fats_max: float = round(weight * FC.FAT_COEFFS["max"])

        carbs_min: float = round(
            (kcal - protein_max * FC.KCALORIES_PER_GRAM["protein"] - 
             fats_max * FC.KCALORIES_PER_GRAM["fats"]) / FC.KCALORIES_PER_GRAM["carbs"]
        )
        carbs_max: float = round(
            (kcal - protein_min * FC.KCALORIES_PER_GRAM["protein"] - 
             fats_min * FC.KCALORIES_PER_GRAM["fats"]) / FC.KCALORIES_PER_GRAM["carbs"]
        )

        pfc: dict[str, float] = {
            "protein_min": protein_min, "protein_max": protein_max,
            "fats_min": fats_min, "fats_max": fats_max,
            "carbs_min": carbs_min, "carbs_max": carbs_max
        }
        return pfc


class DeficitCalculator:
    deficit_cpfc: dict[str, dict[str, float | dict[str, float]]]

    def __init__(self, tdee: float = 2000, weight: float = 80, goal: str = "G", 
                 mode: str = "normal") -> None:
        self.deficit_cpfc = self.collect_deficit_data(tdee, weight, goal, mode)
    
    @staticmethod
    def calories_calculate(tdee: float, goal: str, coef_deficit: int) -> float:
        return tdee * (1 + FC.VALUE_GOALS_FOR_CALCULATOR[goal] * (coef_deficit / 100))
    
    @staticmethod
    def collect_deficit_data(tdee: float, weight: float, goal: str, mode: str) -> dict[str, dict[str, float | dict[str, float]]]:
        deficit_modes: list[str] = list(FC.DEFICIT_MODE[goal].keys())
        valid_mode: str | None = check_str_value(mode, deficit_modes)
        if valid_mode is None:
            valid_mode = deficit_modes[0]

        coefficients: tuple[int, int] = FC.DEFICIT_MODE[goal][valid_mode]
        deficit_cpfc: dict[str, dict[str, float | dict[str, float]]] = {}
        
        for deficit in coefficients:
            kcal: float = round(DeficitCalculator.calories_calculate(tdee, goal, deficit))
            deficit_cpfc[str(deficit)] = {
                "kcal": kcal,
                "pfc": CPFCCalculator.pfc_calculate(weight, kcal, goal)
            }
        return deficit_cpfc