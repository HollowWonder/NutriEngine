from SRC.presentation.CLI import Interface
from SRC.Infrastructure.JsonHandler import JsonOperation, BaseJsonOperation, Log
file_name: str = "UsersData.json"

base_json = BaseJsonOperation(file_name)
user_json = JsonOperation(file_name)
logs_json = Log()

Interface(base_json, user_json, logs_json)