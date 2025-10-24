from os import path

class File_Paths:
    def __init__(self) -> None:
        self.Base_Dir:str = path.dirname(__file__)
        self._Paths:dict[str,str] = {
            "NutriEngine" : self.Base_Dir,
            "TestData.json" : path.join(self.Base_Dir, "Data","TestData", "TestData.json")
        }
    
    def get_path(self, File_Name) -> str:
        return self._Paths.get(File_Name, "")

    def get_paths(self) -> dict[str,str]:
        return self._Paths

class Checker_Paths(File_Paths):
    def Check_Path(self, File_Name:str) -> bool:
        return path.exists(self.get_path(File_Name))

    def Check_Paths(self) -> dict[str,dict[str, bool]]:
        Directory_Info:dict[dict[str,str], bool] = {}
        for File, File_Path in self._Paths.items():
            Directory_Info[File] = {
                "Path" : File_Path,
                "Found" : path.exists(File_Path)
            }
        return Directory_Info

