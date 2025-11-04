from SRC.Domain.UserProfileCollector import UserProfileType
from typing import TypedDict, Optional

#Types for Autorization.py
class SystemUserInfoType(TypedDict):
    id: str
    user_name: str
    password: str

#types for JSONHandler.py
class UserDataType(TypedDict):
    system_info: SystemUserInfoType
    user_profile: UserProfileType

DataDictType = Optional[dict[str, Optional[UserDataType]]]


