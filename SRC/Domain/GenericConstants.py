class Realistic_Validations:
    # For userinfo class
    List_Of_Genders:list[str] = ['M', 'W']
    Min_Age:int = 15
    Max_Age :int= 100
    Min_Height:int = 140
    Max_Height:int = 220
    Min_Weight:int = 35
    Max_Weight:int = 300

    # For usergoals class
    Valid_Goals:list[str] = ["M", "L", "G"]
    Min_Activity:int = 0
    Max_Activity:int = 9

class Fitness_Constants:
    
    # For BMI calculator
    BMI_Categories:dict[tuple[float,float], str] = {
        (0, 16.0): "Severe underweight",
        (16.0, 18.5): "Underweight", 
        (18.5, 25.0): "Normal weight",
        (25.0, 30.0): "Overweight",
        (30.0, 35.0): "Obesity class I",
        (35.0, 40.0): "Obesity class II", 
        (40.0, float('inf')): "Obesity class III"
    }

    def Get_BMICategory(index:int) -> str:
        for (min_Index,max_Index) ,Category in BMI_Categories.items():
            if index >= min_Index and index < max_Index:
                return Category
        return "Unknown category"

    # For BMR calculator
    Metabolism: dict[str, int] = {
        "M": 5, "W": -161
    }

    # For TDEE calculator
    Value_Weekly_Activity:dict[int,float] = {0:1.2,
                                             1:1.375,
                                             2:1.375,
                                             3:1.55,
                                             4:1.55,
                                             5:1.55,
                                             6:1.725,
                                             7:1.725,
                                             8:1.9}
    
    # For PFC calculator
    Value_Goals_For_Calculator:dict[str,int] = {"M": 1, "G": 1, "L": -1}
    
    Protein_Coeffs:dict[str,dict[str,float]] = {
        "L": {"Min": 2.0, "Max": 2.7},
        "G": {"Min": 1.6, "Max": 2.5},
        "M": {"Min": 1.5, "Max": 2.0}
    }

    Fat_Coeffs:dict[str,float] = {
        "Min": 0.8, "Max": 1.2 
    }

    Kcalories_Per_Gramm:dict[str,float] = {
        "Protein": 4, "Fats": 9, "Carbs": 4
    }
