from SRC.Infrastructure.Authorization import AutoService
from SRC.Infrastructure.JsonHandler import BaseJsonOperation, JsonOperation, Log
from typing import Callable
import sys

class Interface:
    auto_service: AutoService

    def __init__(self, base_json: BaseJsonOperation, user_json: JsonOperation, logs: Log) -> None:
        self.auto_service = AutoService(base_json, user_json, logs)
        self.unlogin_user()

    def unlogin_user(self) -> None:
        while True:
            UNLOGIN_COMMANDS: dict[str, Callable[..., None]] = {
                "0": self.regist_command,
                "1": self.login_command,
                "2": self.exit_command
            }

            print("0 - regist")
            print("1 - login")
            print("2 - exit")
            command = input("choice command: ")
            if command not in UNLOGIN_COMMANDS.keys():
                print("invalid command")
                continue
            UNLOGIN_COMMANDS[command]()
    
    def regist_command(self) -> None:
        try:
            self.auto_service.regist_user()
            self.exit_command()
        except Exception as e:
            print(f"Error in regist_command: {e}")
            self.exit_command()

    def login_command(self) -> None:
        try:
            self.auto_service.login()
        except Exception as e:
            print(f"Error in login_command: {e}")
            self.exit_command()
    
    def exit_command(self) -> None:
        sys.exit(0)
