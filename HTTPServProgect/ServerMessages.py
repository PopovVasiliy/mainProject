from dataclasses import dataclass
from datetime import datetime
from Users import FullServerUser
from typing import Dict, Any


@dataclass
class ServerMessage:
    data_message: datetime
    user_recipient: FullServerUser
    user_sender: FullServerUser
    text_message: str
    def to_json(self) -> Dict[str, Any]:
        return {
                'data_message': self.data_message,
                'user_recipient': self.user_recipient.ServerUser.nick_user,
                'user_sender':    self.user_sender.ServerUser.nick_user,
                'text_message':    self.text_message}
