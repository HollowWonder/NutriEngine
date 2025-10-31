import pytest
from typing import Optional
from SRC.Domain.Calculators import CPFCCalculator, BMIInformation, DeficitCalculator
from SRC.Domain.User import UserInfo, UserGoals
from SRC.Domain.GenericConstants import FitnessConstants as FC, RealisticValidations as RV


class TestUserData:
    
    @pytest.mark.parametrize("name, gender, age, height, weight", [
        ("Bob", "M", 20, 190, 90),
        ("Mike", "M", 19, 170, 70),
        ("Tom", "m", 22, 192, 88),
        ("Alica", "w", 27, 170, 60),
        ("Rose", "w", 30, 166, 66),
        ("Amelie", "w", 22, 162, 56),
        ("Lily", "w", 17, 180, 69)
    ])
    def test_user_info(self, name: str, gender: str, age: int, height: float, weight: float) -> None:
        user_info = UserInfo(name, gender, age, height, weight)

        assert user_info.name == name
        assert user_info.gender == gender.upper()
        assert user_info.age == age
        assert user_info.height == height
        assert user_info.weight == weight

    @pytest.mark.parametrize("current_weight, goal, weekly_activity, goal_weight, mode", [
        (60, "l", 4, 59, "normal"),
        (70, "G", 7, 80, "normal"),
        (80, "M", 2, 80, "normal"),
        (66, "m", 1, 66, "normal")
    ])
    def test_user_goals(self, current_weight: int, goal: str, weekly_activity: int, goal_weight: Optional[float], mode: str) -> None:
        goals = UserGoals(current_weight, goal, weekly_activity, goal_weight, mode)

        assert goals.current_weight == current_weight
        assert goals.goal == goal.upper()
        assert goals.weekly_activity == weekly_activity
        assert goals.goal_weight == goal_weight
        assert goals.deficit_mode == mode


class TestCalculator:
    common_test_data: list[tuple[str, int, float, float, int, str, str]] = [
        ("M", 25, 180.0, 75.0, 3, "G", "normal"),
        ("W", 30, 165.0, 60.0, 2, "L", "extra"), 
        ("M", 22, 175.0, 70.0, 4, "G", "normal"),
        ("W", 28, 160.0, 55.0, 1, "L", "normal")
    ]

    @pytest.mark.parametrize("gender, age, height, weight, weekly_activity, goal, mode", common_test_data)
    def test_calculators_result(self, gender: str, age: int, height: float, weight: float, 
                   weekly_activity: int, goal: str, mode: str) -> None:
        cpfc_info = CPFCCalculator(gender, age, height, weight, weekly_activity, goal)
        bmi_info = BMIInformation(height, weight)

        calculated_bmi_info = BMIInformation.bmi_calculate(weight, height)
        calculated_bmr = CPFCCalculator.bmr_calculate(weight, height, age, gender)
        calculated_tdee = CPFCCalculator.tdee_calculate(calculated_bmr, weekly_activity)
        calculated_pfc = CPFCCalculator.pfc_calculate(weight, calculated_tdee, goal)

        deficit_info = DeficitCalculator(calculated_tdee, weight, goal, mode)
        calculated_deficit_info = DeficitCalculator.collect_deficit_data(
            calculated_tdee, weight, goal, mode
        )

        assert bmi_info.bmi_info == calculated_bmi_info
        assert cpfc_info.bmr == calculated_bmr
        assert cpfc_info.tdee == calculated_tdee
        assert cpfc_info.pfc == calculated_pfc
        assert deficit_info.deficit_cpfc == calculated_deficit_info