from os import path


class FilePaths:
    def __init__(self) -> None:
        self.base_dir: str = path.dirname(__file__)
        self._paths: dict[str, str] = {
            "NutriEngine": self.base_dir,
            "UsersData.json": path.join(self.base_dir, "Data", "UsersData.json"),
            "LogsData.json": path.join(self.base_dir, "Data", "LogsData.json"),
            "TestData.json": path.join(self.base_dir, "Data", "TestData", "TestData.json")
        }
    
    def get_path(self, file_name: str) -> str:
        return self._paths.get(file_name, "")

    def get_paths(self) -> dict[str, str]:
        return self._paths


class CheckerPaths(FilePaths):
    def check_path(self, file_name: str) -> bool:
        return path.exists(self.get_path(file_name))

    def check_paths(self) -> dict[str, dict[str, bool | str]]:
        directory_info: dict[str, dict[str, bool | str]] = {}
        for file, file_path in self._paths.items():
            directory_info[file] = {
                "path": file_path,
                "found": path.exists(file_path)
            }
        return directory_info