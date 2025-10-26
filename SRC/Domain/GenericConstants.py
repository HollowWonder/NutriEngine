class RealisticValidations:
    # For userinfo class
    LIST_OF_GENDERS: list[str] = ['M', 'W']
    MIN_AGE: int = 15
    MAX_AGE: int = 100
    MIN_HEIGHT: int = 140
    MAX_HEIGHT: int = 220
    MIN_WEIGHT: int = 35
    MAX_WEIGHT: int = 300

    # For usergoals class
    VALID_GOALS: list[str] = ["M", "L", "G"]
    MIN_ACTIVITY: int = 0
    MAX_ACTIVITY: int = 9


class FitnessConstants:
    # For BMI calculator
    BMI_CATEGORIES: dict[tuple[float, float], str] = {
        (0, 16.0): "Severe underweight",
        (16.0, 18.5): "Underweight", 
        (18.5, 25.0): "Normal weight",
        (25.0, 30.0): "Overweight",
        (30.0, 35.0): "Obesity class I",
        (35.0, 40.0): "Obesity class II", 
        (40.0, float('inf')): "Obesity class III"
    }

    RECOMMENDED_BMI: dict[str, float] = {
        "min": 18.5,
        "max": 25.0
    }

    @classmethod
    def get_bmi_category(cls, bmi_value: float) -> str:
        for (min_index, max_index), category in cls.BMI_CATEGORIES.items():
            if min_index <= bmi_value < max_index:
                return category
        return "Unknown category"

    # For BMR calculator
    METABOLISM: dict[str, int] = {
        "M": 5, "W": -161
    }

    # For TDEE calculator
    VALUE_WEEKLY_ACTIVITY: dict[int, float] = {
        0: 1.2, 1: 1.375, 2: 1.375, 3: 1.55, 4: 1.55, 
        5: 1.55, 6: 1.725, 7: 1.725, 8: 1.9
    }
    
    # For PFC calculator
    VALUE_GOALS_FOR_CALCULATOR: dict[str, int] = {"M": 1, "G": 1, "L": -1}
    
    PROTEIN_COEFFS: dict[str, dict[str, float]] = {
        "L": {"min": 2.0, "max": 2.7},
        "G": {"min": 1.6, "max": 2.5},
        "M": {"min": 1.5, "max": 2.0}
    }

    FAT_COEFFS: dict[str, float] = {
        "min": 0.8, "max": 1.2 
    }

    KCALORIES_PER_GRAM: dict[str, float] = {
        "protein": 4, "fats": 9, "carbs": 4
    }

    DEFICIT_MODE: dict[str, dict[str, tuple[int, int]]] = {
        "L": {
            "normal": (15, 20),
            "extra": (25, 30)
        },
        "G": {
            "low": (10, 15),
            "normal": (15, 20),
            "extra": (20, 25)
        }
    }