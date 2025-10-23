from Config import Files_Path as FP

class Json_Check:
    def __init__(self) -> None:
        self.File_TestData = None
        try:
            with open(FP.Test_UserData, "r", encoding="utf-8") as F:
                self.File = F.read()
        except FileNotFoundError:
            print("Error: File not detected")
        except PermissionError:
            print("Errpr: You don't have enough permission")
        except Exception as e:
            print(f"Error: {e}")

class Tests_Data_Add(Json_Check):
    UserInfo: tuple[str,str,int,float,float]

    def __init__(self, UserInfo: tuple[str,str,int,float,float]) -> None:
        self.UserInfo = UserInfo
        self._Add_Info()
    def _Add_Info(self, Data_Name) -> None:
        with open(FP.Test_UserData, "a", encoding="utf-8"):
            pass
        pass