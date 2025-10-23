from SRC.Domain.GenericConstants import Realistic_Validations as RV
from random import randint, uniform, choice

def UserInfo_Data_Maker(Count) -> dict[str,tuple[str,str,int,float,float]]:
    Users_Data:dict[str,tuple[str,str,int,float,float]] = {}
    for User in range(Count):
        UserData:tuple[str,str,int,float,float] = (f"Test_User-{User}", choice(RV.List_Of_Genders), randint(RV.Min_Age, RV.Max_Age), uniform(RV.Min_Height, RV.Max_Height), uniform(RV.Min_Weight, RV.Max_Weight))
        Users_Data[f"Test_User-{User}"] = UserData
    return Users_Data