from json import load, dump, JSONDecodeError
from PathConfig import FilePaths as FP
from SRC.Domain.UserProfileCollector import UserProfileType, DefaultUserProfile, InputUserProfile
from SRC.Infrastructure.Validations import check_str_value
from SRC.Infrastructure.Types import UserLogsType, LogsDictType, SystemUserInfoType, UserDataType, DataDictType
from datetime import datetime
from typing import Optional, TypedDict, Any, Callable

class BaseJsonOperation:
    file_path: str
    check_file: bool

    def __init__(self, file_name: str) -> None:
        file_paths_class: FP = FP()
        self.data_path = file_paths_class.get_path(file_name)
        self.check_file = self.check_json_file()
    
    def check_json_file(self) -> bool:
        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                return True
        except FileNotFoundError:
            print("Error: File not detected")
            return False
        except PermissionError:
            print("Error: You don't have enough permission")
            return False
        except Exception as e:
            print(f"Error in check_json_file: {e}")
            return False
    
    def load_data(self) -> Any:
        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                data: Any

                try:
                    data = load(file)
                except JSONDecodeError:
                    data = {}

                return data
        except Exception as e:
            print(f"Error in load_data: {e}")
            return {}

    def save_data(self, data: Any) -> None:
        try:
            with open(self.data_path, "r+", encoding="utf-8") as file:
                # return to begin file
                file.seek(0)
                # remove all file data
                file.truncate()
                dump(data, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error in save_data: {e}")
            return None

class Log:
    json: BaseJsonOperation
    logs_data: LogsDictType

    def __init__(self) -> None:
        self.json = BaseJsonOperation("LogsData.json")
        self.logs_data = self.json.load_data()
    
    def create_user_log(self, uid: str, username: str) -> None:
        try:
            self.logs_data[uid] = {
                "uid": uid,
                "username": username,
                "logs": {
                    str(datetime.now()): f"User #{uid} was add"
                }
            }
            self.json.save_data(self.logs_data)
        except Exception as e:
            print(f"Error in create_user_log: {e}")
            return None

    def update_user_log(self, uid: str, messsage: str) -> None:
        try:
            user_logs: UserLogsType = self.logs_data[uid]
            date: str = str(datetime.now())
            user_logs["logs"][date] = messsage
            self.json.save_data(user_logs)
        except Exception as e:
            print(f"Error in update_user_log: {e}")
            return None

class JsonOperation:
    base_json: BaseJsonOperation
    log: Log

    def __init__(self, file_name:str) -> None:
        self.base_json = BaseJsonOperation(file_name)
        self.log = Log()
    
    def check_id(self, uid: str) -> bool:
        try:
            data: DataDictType = self.base_json.load_data()
            check_id_bool: bool = data is not None and uid in data

            if check_id_bool == False:
                print(f"UID-{uid} not found or data is empty")
            return check_id_bool
        except Exception as e:
            print(f"Error in check_id: {e}")
            return False

    def add_data(self, system_info: SystemUserInfoType, user_profile: UserProfileType) -> None:
        try:
            data: DataDictType = self.base_json.load_data()
            new_id: str

            try:
                new_id = str(len(data.keys()))
            except:
                data = {}
                new_id = "0"
            
            system_info["uid"] = new_id
            data[new_id] = {
                "system_info": system_info,
                "user_profile": user_profile
            }
            self.base_json.save_data(data)
            self.log.create_user_log(new_id, system_info["username"])
        except Exception as e:
            print(f"Error in add_data: {e}")
            return None

    def get_data(self, uid: str) -> Optional[UserDataType]:
        try:
            if self.check_id(uid) == False:
                return None

            data: DataDictType = self.base_json.load_data()
            user_data: Optional[UserDataType] = data[uid]
            self.log.update_user_log(uid, f"Was get info about user #{uid}")
            return user_data
        except Exception as e:
            print(f"Error in get_data: {e}")
            return None
    
    def delete_data(self, uid: str) -> None:
        try:
            if self.check_id(uid) == False:
                return None

            data: DataDictType = self.base_json.load_data()
            data[uid] = None
            self.base_json.save_data(data)
            self.log.update_user_log(uid, f"User #{uid} was delete")
        except Exception as e:
            print(f"Error in dalete data: {e}")
            return None
    
    def update_user_profile_field(self, uid: str) -> None:
        try:
            if self.check_id(uid) == False:
                return None

            new_user_profile: UserProfileType
            data: DataDictType = self.base_json.load_data()
            user_data: Optional[UserDataType] = data[uid]
            if user_data is None:
                print(f"User #{uid} was delete")
                return None
            
            user_data_personality_info: dict[str, dict[str, Any]] = user_data["user_profile"]["personality_user_info"]
            user_info: dict[str, Any] = user_data_personality_info["user_info"]
            user_goals: dict[str, Any] = user_data_personality_info["user_goals"]

            user_info_parameters: list[str] = list(user_info.keys())
            user_goals_parameters: list[str] = list(user_goals.keys())

            list_parameters: list[str] = [*user_info_parameters, *user_goals_parameters]
            parameter: str = input(f"{list_parameters}\nChoice parameter: ").lower()
            last_value: Optional[str | float | int]
            new_value: Optional[str | float | int]

            data_funtions: dict[str, Callable[..., str | int | float]] = InputUserProfile.data_input_funtions()
            if parameter in user_info_parameters:
                last_value = user_info[parameter]
                new_value = data_funtions[parameter]()
                user_info[parameter] = new_value
            elif parameter in user_goals_parameters:
                last_value = user_info[parameter]
                if parameter == "goal_weight":
                    new_value = data_funtions[parameter](user_info["weight"], user_goals["goal"])
                elif parameter == "deficit_mode":
                    new_value = data_funtions[parameter](user_goals["goal"])
                else:
                    new_value = data_funtions[parameter]()
                user_goals[parameter] = new_value
            else:
                print(f"Invalid parameter, must be one of {list_parameters}")
                return None

            new_user_profile = create_user_profile(user_info, user_goals)
            if user_data is not None:
                user_data["user_profile"] = new_user_profile
            self.base_json.save_data(data)
            self.log.update_user_log(uid, f"Changed {parameter} from {last_value} to {new_value}")
        except Exception as e:
            print(f"Error in update_user_profile_field: {e}")
            return None
    
    def update_user_profile(self, uid: str) -> None:
        try:
            if self.check_id(uid) == False:
                return None
                
            new_user_profile: UserProfileType
            data: DataDictType = self.base_json.load_data()
            user_data: Optional[UserDataType] = data[uid]
            if user_data == None:
                print(f"User {uid} was delete")
                return None
            input_user_prifle_class: InputUserProfile = InputUserProfile()
            new_user_profile = input_user_prifle_class.return_data_inputed_user_profile()
            if user_data is not None:
                user_data["user_profile"] = new_user_profile
            self.base_json.save_data(data)
            self.log.update_user_log(uid, "Full updated user information")
        except Exception as e:
            print(f"Error in update_user_profile: {e}")
            return None

def create_user_profile(user_info: dict[str, Any], user_goals: dict[str, Any]) -> UserProfileType:
    name: str = str(user_info["name"]) if user_info["name"] is not None else "Unknown"
    gender: str = str(user_info["gender"]) if user_info["gender"] is not None else "M"
    age: int = int(user_info["age"]) if user_info["age"] is not None else 20
    height: float = float(user_info["height"]) if user_info["height"] is not None else 180.0
    weight: float = float(user_info["weight"]) if user_info["weight"] is not None else 80.0
    goal: str = str(user_goals["goal"]) if user_goals["goal"] is not None else "M"
    weekly_activity: int = int(user_goals["weekly_activity"]) if user_goals["weekly_activity"] is not None else 0
    goal_weight: Optional[float] = float(user_goals["goal_weight"]) if user_goals["goal_weight"] is not None else None
    mode: str = str(user_goals["deficit_mode"]) if user_goals["deficit_mode"] is not None else "normal"

    user_profile_class:DefaultUserProfile = DefaultUserProfile(name, gender, age, height, weight, goal, weekly_activity, goal_weight, mode)
    return user_profile_class.return_data_user_profile()
    