from SRC.Domain.UserProfileCollector import UserProfileType
from typing import TypedDict, Optional

#Types for Autorization.py
class SystemUserInfoType(TypedDict):
    uid: str
    username: str
    password: str
    created: str
    last_login: str

#types for JSONHandler.py
class UserDataType(TypedDict):
    system_info: SystemUserInfoType
    user_profile: UserProfileType

DataDictType = dict[str, Optional[UserDataType]]

class UserLogsType(TypedDict):
    uid: str
    username: str
    logs: dict[str, str]

LogsDictType = dict[str, UserLogsType] 


