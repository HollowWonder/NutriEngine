"""from SRC.Domain.User import User
from SRC.Domain.Calculators import *

User_Data = User()
print(f" Name: {User_Data.Info.Name} | Gender: {User_Data.Info.Gender} | Age: {User_Data.Info.Age} | Height: {User_Data.Info.Height} | Weight {User_Data.Info.Weight}")
print(f" Goals: {User_Data.Goals.Goal} | Weekly activity: {User_Data.Goals.Weekly_Activity} | Wanted weight: {User_Data.Goals.Goal_Weight}")

User_Data_CPFC = CPFC_Inforamation()
print(f" BMR: {User_Data_CPFC.BMR} | TDEE: {User_Data_CPFC.TDEE}")
print(f" Protein per day: {User_Data_CPFC.PFC['Protein_Min']} - {User_Data_CPFC.PFC['Protein_Max']} ")

User_Data.Collect_Data()
User_Data_CPFC = CPFC_Inforamation(User_Data.Info.Gender, User_Data.Info.Age, User_Data.Info.Height, User_Data.Info.Weight, User_Data.Goals.Weekly_Activity, User_Data.Goals.Goal)

print(f" Name: {User_Data.Info.Name} | Gender: {User_Data.Info.Gender} | Age: {User_Data.Info.Age} | Height: {User_Data.Info.Height} | Weight {User_Data.Info.Weight}")
print(f" Goals: {User_Data.Goals.Goal} | Weekly activity: {User_Data.Goals.Weekly_Activity} | Wanted weight: {User_Data.Goals.Goal_Weight}")
print(f" BMR: {User_Data_CPFC.BMR} | TDEE: {User_Data_CPFC.TDEE}")
print(f" Protein per day: {User_Data_CPFC.PFC['Protein_Min']} - {User_Data_CPFC.PFC['Protein_Max']} ")

input("Press enter to exit")"""

from Config import Files_Path as FP
from Tests.TestDataMaker import UserInfo_Data_Maker
User_Data = UserInfo_Data_Maker(100)

for i in User_Data:
    print(f"{i}")