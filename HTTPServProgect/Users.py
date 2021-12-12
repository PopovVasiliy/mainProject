from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any


class Status(Enum):
    offline = 0
    online = 1
    printing = 2


@dataclass
class ServerUser:
    nick_user: str
    password_user: str
    name_user: str


@dataclass
class FullServerUser:
    ServerUser: ServerUser
    status: Status

    def to_json(self) -> Dict[str, Any]:
        return {
                'nick_user': self.ServerUser.nick_user,
                'name_user': self.ServerUser.name_user,
                'status':    str(self.status.value)}


@dataclass()
class RequestUser:
    ErrorKode: str
    @classmethod
    def to_json_error(cls) -> Dict[str, Any]:
        return {
                'ErrorKode': 'Error',
                }

    @classmethod
    def to_json_OK(cls) -> Dict[str, Any]:
        return {
                'ErrorKode': 'OK',
                }

