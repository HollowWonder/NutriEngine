from json import load, dump, JSONDecodeError
from PathConfig import FilePaths as FP
from SRC.Domain.UserProfileCollector import UserProfileType, DefaultUserProfile, InputUserProfile
from SRC.Infrastructure.Validations import check_str_value
from typing import Optional

DataDictType = dict[str, UserProfileType | None]
class JsonOperations:
    data_path:str

    def __init__(self, file_name:str) -> None:
        file_paths_class = FP()
        self.data_path = file_paths_class.get_path(file_name)

    def add_data(self, user_data: UserProfileType) -> None:
        if self._check_json_file() == False:
            return None

        try:
            with open(self.data_path, "r+", encoding="utf-8") as file:
                data: DataDictType
                new_id: int

                try:
                    data = load(file)
                    new_id = len(data.keys())
                except JSONDecodeError:
                    data = {}
                    new_id = 0
                    
                data[str(new_id)] = user_data

                self._save_data(data)
        except Exception as e:
            print(f"Error in add_data: {e}")
            return None

    def get_data(self, id: str) -> UserProfileType | None:
        if self._check_json_file() == False:
            return None

        try:
            with open(self.data_path, "r+", encoding="utf-8") as file:
                if self._check_id(id) == False:
                    print(f"UID-{id} not found or data is empty")
                    return None
                    
                data: DataDictType = load(file)
                user_data: UserProfileType | None = data[id]
                return user_data
        except Exception as e:
            print(f"Error in get_data: {e}")
            return None
    
    def delete_data(self, id: str) -> None:
        if self._check_json_file() == False:
            return None

        try:
            with open(self.data_path, "r+", encoding="utf-8") as file:
                if self._check_id(id) == False:
                    print(f"UID-{id} not found or data is empty")
                    return None

                data: DataDictType = load(file)
                data[id] = None
                self._save_data(data)
        except Exception as e:
            print(f"Error in dalete data: {e}")
            return None
    
    def update_data(self, id: str, parameter: str | None = None, value: str | float | int | None = None) -> None:
        if self._check_json_file() == False:
            return None

        try:
            with open(self.data_path, "r+", encoding="utf-8") as file:
                new_user_profile: UserProfileType
                
                if self._check_id(id) == False:
                    print(f"UID-{id} not found or data is empty")
                    return None

                data: DataDictType = load(file)
                user_data: UserProfileType | None = data[id]
                
                if user_data != None:
                    user_data_personality_info: dict[str, dict[str, str | int | float | None]] = user_data["personality_user_info"]

                user_info: dict[str, str | int | float | None] = user_data_personality_info["user_info"]
                user_goals: dict[str, str | int | float | None] = user_data_personality_info["user_goals"]
                if parameter != None:
                    if value != None and user_data != None:
                        user_info_parameters: list[str] = list(user_info.keys())
                        user_goals_parameters: list[str] = list(user_goals.keys())

                        if parameter in user_info_parameters:
                            user_info[parameter] = value
                        elif parameter in user_goals_parameters:
                            user_goals[parameter] = value

                        name = str(user_info["name"]) if user_info["name"] is not None else "Unknown"
                        gender = str(user_info["gender"]) if user_info["gender"] is not None else "M"
                        age = int(user_info["age"]) if user_info["age"] is not None else 20
                        height = float(user_info["height"]) if user_info["height"] is not None else 180.0
                        weight = float(user_info["weight"]) if user_info["weight"] is not None else 80.0
                        goal = str(user_goals["goal"]) if user_goals["goal"] is not None else "M"
                        weekly_activity = int(user_goals["weekly_activity"]) if user_goals["weekly_activity"] is not None else 0
                        goal_weight = float(user_goals["goal_weight"]) if user_goals["goal_weight"] is not None else None
                        mode = str(user_goals["deficit_mode"]) if user_goals["deficit_mode"] is not None else "normal"

                        user_profile_class:DefaultUserProfile = DefaultUserProfile(name, gender, age, height, weight, goal, weekly_activity, goal_weight, mode)
                        new_user_profile = user_profile_class.return_data_user_profile()
                    else:
                        print("Value mustn't be None")
                        return None
                else:
                    input_class: InputUserProfile = InputUserProfile()
                    new_user_profile = input_class.return_data_inputed_user_profile()
                data[id] = new_user_profile

                self._save_data(data)
        except Exception as e:
            print(f"Error in update_data: {e}")
            return None
    
    def _check_json_file(self) -> bool:
        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                return True
        except FileNotFoundError:
            print("Error: File not detected")
            return False
        except PermissionError:
            print("Errpr: You don't have enough permission")
            return False
        except Exception as e:
            print(f"Error in _check_json_file: {e}")
            return False
    
    def _save_data(self, data: DataDictType) -> None:
        with open(self.data_path, "r+", encoding="utf-8") as file:
            # return to begin file
            file.seek(0)
            # remove all file data
            file.truncate()
            dump(data, file, ensure_ascii=False, indent=2)
    
    def _check_id(self, id: str) -> bool:
        if self._check_json_file == False:
            return False
        
        try:
            with open(self.data_path, "r+", encoding="utf-8") as file:
                data: DataDictType = load(file)
                return data is not None and id in data
        except Exception as e:
            print(f"Error in _check_id: {e}")
            return False
