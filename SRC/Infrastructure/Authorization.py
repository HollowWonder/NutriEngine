from SRC.Infrastructure.JsonHandler import JsonOperation, BaseJsonOperation, Log
from SRC.Infrastructure.Types import DataDictType as DDT, SystemUserInfoType as SUIT, UserDataType as UDT, UserProfileType as UPT
from SRC.Domain.UserProfileCollector import InputUserProfile
from SRC.Infrastructure.Validations import check_numerical_input_value as CNIV
from datetime import datetime
from passlib.hash import bcrypt
from typing import Optional, Callable, Any
from random import choice
from json import dumps
import sys

class AutoService:
    base_json: BaseJsonOperation
    json: JsonOperation
    logs: Log
    data: DDT
    login_b: bool

    def __init__(self, base_json: BaseJsonOperation, json: JsonOperation, logs: Log) -> None:
        self.base_json = base_json
        self.json = json
        self.logs = logs
        self.data = self.base_json.load_data()
    
    def regist_user(self) -> None:
        try:
            username_class: UserNameHandler = UserNameHandler(self.data)
            if username_class.username is None:
                return None
            password_class: PasswordHandler = PasswordHandler()
            if password_class.hash_password is None:
                return None

            system_info: SUIT = {
                "uid": "None",
                "username": username_class.username,
                "password": password_class.hash_password,
                "created": str(datetime.now()),
                "last_login": str(datetime.now())
            }
            user_profile_class: InputUserProfile = InputUserProfile()
            self._add_profile_logic(system_info, user_profile_class.return_data_inputed_user_profile(), username_class.username)
        except Exception as e:
            print(f"Error in regist_user: {e}")

    def login(self) -> None:
        max_attemps: int = 3
        attemp: int = 0
        while attemp < max_attemps:
            try:
                username: str = input("Enter username: ").lower()
                password: str = input("Enter password: ")

                uid: Optional[str] = UserRepository.find_user(self.data, username)
                if uid is not None:
                    user_data = self.json.get_data(uid)
                    if user_data is None:
                        print("something went wrong")
                        return None
                    user_hash_password: str = user_data["system_info"]["password"]
                    if PasswordHandler.verify_hash_password(password, user_hash_password):
                        self.login_b = True
                        self._update_login_time(uid)
                        self.logs.update_user_log(uid, "log in")
                        self._login_logic(uid)
                        return None
                    print("invalid password")
                print("user not found")
            except Exception as e:
                print(f"Error in login: {e}")
        print("too much attemps, try lates")
        return None
    
    def _login_logic(self, uid: str) -> None:
        try:
            while self.login_b:
                funtions: dict[str, Callable[..., Optional[UDT]]] = {
                    "update_profile": lambda: self._update_profile_logic(uid),
                    "update": lambda: self._update_value_logic(uid),
                    "get": lambda: self._get_info_logic(uid),
                    "delete": lambda: self._delete_logic(uid),
                    "log_out": lambda: self._log_out_logic(uid)
                }
                for num, command in enumerate(funtions):
                    print(f"{num} - {command}")
                commands: list[str] = list(funtions.keys())
                current_command: int = int(CNIV("Choice command: ", 0, len(funtions.keys())))
                funtions[commands[current_command]]()
            return None
        except Exception as e:
            print(f"Error in _login_logic: {e}")
            return None
    
    def _add_profile_logic(self, system_info: SUIT, user_profile: UPT, username: str) -> None:
        uid: Optional[str] = self.json.add_data(system_info, user_profile)
        if uid is None:
            print("Error in _add_profile_logic")
            return None
        self.logs.create_user_log(uid, username)
    
    def _log_out_logic(self, uid: str) -> None:
        self.logs.update_user_log(uid, "log out")
        self.login_b = False
        return None
    
    def _delete_logic(self, uid: str) -> None:
        self.json.delete_data(uid)
        self.logs.update_user_log(uid, "User was delete")
        self._log_out_logic(uid)
    
    def _get_info_logic(self, uid: str) -> None:
        info: Optional[UDT] = self.json.get_data(uid)
        print(dumps(info, ensure_ascii=False, indent=2))
        self.logs.update_user_log(uid, "Got user data")
    
    def _update_profile_logic(self, uid: str) -> None:
        self.json.update_user_profile(uid)
        self.logs.update_user_log(uid, "Update user info")
    
    def _update_value_logic(self, uid: str) -> None:
        change_info: Optional[dict[str, Any]] = self.json.update_user_profile_field(uid)
        if change_info is None:
            print("Error in update_value_logic")
            return None
        self.logs.update_user_log(uid, f"Update value {change_info["parameter"]} from {change_info["old_value"]} to {change_info["new_value"]}")

    def _update_login_time(self, uid: str) -> None:
        date: str = str(datetime.now())
        data = self.base_json.load_data()
        user_data: Optional[UDT] = data[uid]
        if user_data is None:
            print("something went wrong")
            return None
        user_system_info = user_data["system_info"]
        user_system_info["last_login"] = date
        self.base_json.save_data(data)

        

class UserNameHandler:
    MIN_LEN_USERNAME: int = 6
    MAX_LEN_USERNAME: int = 20

    username: Optional[str]

    def __init__(self, data: DDT) -> None:
        self.username = self.input_username(data)

    @staticmethod
    def get_usernames(data: DDT) -> list[str]:
        list_of_usernames: list[str] = ["admin"]
        for uid in data:
            user_data = data[uid]
            if user_data == None:
                continue
            current_user_username: Optional[str] = user_data["system_info"]["username"]
            if current_user_username is not None:
                list_of_usernames.append(current_user_username)
        return list_of_usernames
    
    @staticmethod
    def check_username(data: DDT, username: str) -> bool:
        try:
            list_of_usernames: list[str] = UserNameHandler.get_usernames(data)
            check_username: bool = username not in list_of_usernames
            check_len: bool = UserNameHandler.check_len_username(username)
            if check_len and check_username:
                return True
            else:
                if check_username == False:
                    print(f"Username: {username} already taken")
            return False
        except Exception as e:
            print(f"Error in check_username: {e}")
            return False
    
    @staticmethod
    def check_len_username(username: str) -> bool:
        return UserNameHandler.MIN_LEN_USERNAME <= len(username) < UserNameHandler.MAX_LEN_USERNAME
    
    def input_username(self, data: DDT) -> Optional[str]:
        max_attemps: int = 3
        attemp: int = 0
        while attemp < max_attemps:
            try:
                username: str = input("Enter username: ")
                check_name: bool = self.check_username(data, username)
                check_len: bool = self.MIN_LEN_USERNAME <= len(username) < self.MAX_LEN_USERNAME
                if check_name is True:
                    if check_len:
                        return username.lower()
                    attemp += 1
                else:
                    print(f"Username must be > or = {self.MIN_LEN_USERNAME} symbols")
                    attemp += 1
            except Exception as e:
                print(f"Error in input_username: {e}")
        print("too much attemps, try lates")
        return None

class PasswordHandler:
    MIN_PASSWORD_LEN: int = 6
    MAX_PASSWORD_LEN: int = 20

    password: str
    hash_password: str

    def __init__(self) -> None:
        self.input_password()

    def input_password(self) -> None:
        max_attemps: int = 3
        attemp: int = 0
        while attemp < max_attemps:
            try:
                password: str = input("Enter password: ")
                if PasswordHandler.check_len_password(password):
                    password_second_attempt: str = input("Enter password again: ")
                    if password == password_second_attempt:
                        self.password = password
                        self.hash_password = self.hash_password_function(password)
                        return None
                    print("Passwords don't match")
                    attemp += 1
                else:
                    print(f"Password must be >= {PasswordHandler.MIN_PASSWORD_LEN}")
                    attemp += 1
            except Exception as e:
                print(f"Error in input_password: {e}")
        print("too much attemps, try lates")
        return None

    @staticmethod
    def hash_password_function(password: str) -> str:
        return bcrypt.hash(password)
    
    @staticmethod
    def verify_hash_password(password: str, hask_password: str) -> bool:
        return bcrypt.verify(password, hask_password)

    @staticmethod
    def check_len_password(password: str) -> bool:
        return PasswordHandler.MIN_PASSWORD_LEN <= len(password) < PasswordHandler.MAX_PASSWORD_LEN

class UserRepository:
    @staticmethod
    def find_user(data: DDT, username: str) -> Optional[str]:
        data_usersname: dict[str, str] = UserRepository.get_data_usersname(data)

        if username in data_usersname:
            return data_usersname[username]
        else:
            print("User not found")
            return None
    
    @staticmethod
    def get_data_usersname(data: DDT) -> dict[str, str]:
        if data is None:
            print("Data is empty")
            return {}

        data_usersname: dict[str, str] = {}
        for user_id in data.keys():
            user_data: Optional[UDT] = data[user_id]
            if user_data is None:
                continue
            system_info: Optional[SUIT] = user_data.get("system_info")
            if system_info is None:
                continue
            data_usersname[system_info["username"]] = user_id
        return data_usersname