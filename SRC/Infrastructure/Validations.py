def Check_Int_Error(message:str, min_Value:int|float, max_Value:int|float) -> int:
    while True:
        try:
            Value:int = int(input(message))
            if Value < min_Value:
                print(f"Enter number >= {min_Value}")
            elif Value >= max_Value:
                print(f"Enter number < {max_Value}")
            else:
                return Value
        except ValueError:
            print("Enter number format int")
def Check_String(message:str, Valid_Chars:list[str]) -> str:
    while True:
        String:str = input(message).upper()
        if String in Valid_Chars:
            return String
        print(f"Enter one of {Valid_Chars}")

def Check_Len_String(message:str, Len_string:int) -> str:
    while True:
        String:str = input(message)
        if len(String) <= Len_string:
            return String
        else:
            print("String is too large")