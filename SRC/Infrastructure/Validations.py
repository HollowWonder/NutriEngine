def check_numerical_value(value: int | float, min_value: int | float, max_value: int | float) -> int | float | None:
    try:
        if max_value > value >= min_value:
            return value
        else:
            if value < min_value:
                print(f"Value must be >= {min_value}")
            else:
                print(f"Value must be < {max_value}")
            return None
    except Exception as e:
        print(f"Error in check_numerical_value: {e}")
        return None


def check_numerical_input_value(message: str, min_value: int | float, max_value: int | float) -> int | float:
    while True:
        try:
            value_input = input(message)
            value = float(value_input)
            if value.is_integer():
                value = int(value)
            
            checked_value = check_numerical_value(value, min_value, max_value)
            if checked_value is not None:
                return checked_value
        except Exception as e:
            print(f"Error in check_numerical_input_value: {e}")


def check_str_value(value: str, list_valid_value: list[str]) -> str | None:
    try:
        for word in list_valid_value:
            if value.lower() == word.lower():
                return word 
        return None
    except Exception as e:
        print(f"Error in check_str_value: {e}")
        return None


def check_str_input_value(message: str, list_valid_value: list[str]) -> str:
    while True:
        value = input(message)
        validated_value = check_str_value(value, list_valid_value)
        if validated_value is not None:
            return validated_value
        print(f"Invalid input. Please choose from: {', '.join(list_valid_value)}")


def check_str_len_value(value: str, min_len: int, max_len: int) -> str | None:
    try:
        len_value = len(value)
        if check_numerical_value(len_value, min_len, max_len) is not None:
            return value
        else:
            return None
    except Exception as e:
        print(f"Error in check_len_str_value: {e}")
        return None