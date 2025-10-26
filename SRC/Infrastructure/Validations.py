def check_numerical_value(value:int|float, min_value:int|float, max_value:int|float) -> int|float|None:
    try:
        if max_value > value >= min_value:
            return value
        else:
            if value < min_value:
                print(f"Value must be >= {min_value}")
            else:
                print(f"value must be < {max_value}")
            return None
    except ValueError:
        print("Invalid value, needed format: int or float")
        return None

def check_numerical_inputvalue(message: str, min_value: int|float, max_value: int|float) -> int|float:
    while True:
        value:int  = int(input(message))
        if check_numerical_value(value, min_value, max_value) == value:
            return value

def check_str_value(value: str, list_valid_value: list[str]) -> str|None:
    try:
        for word in list_valid_value:
            if value.lower() == word.lower():
                return word 
    except ValueError:
        print("Invalid value, needed format: str")
        return None

def check_str_inputvalue(message:str, list_valid_value: list[str]) -> str:
    while True:
        value = input(message)
        if check_str_value(value, list_valid_value)  == value:
            return value

def check_str_lenvalue(value: str, min_len:int, max_len: int) -> str|None:
    len_value = len(value)
    if check_numerical_value(len_value, min_len, max_len) != None:
        return value
    else:
        return None
