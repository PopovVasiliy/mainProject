from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any


@dataclass
# тип данных для сущности, отражающей историю сообщения пользователя
class HistoryMessage:
    data_message: datetime
    user_recipient: str
    user_sender: str
    text_message: str
    user_autorized: str

    @classmethod
    def dict_to_HistoryMessage(cls, data: Dict[str, Any]):
        return HistoryMessage(data.get('data_message'), data.get('user_recipient'), data.get('user_sender'), data.get('text_message'), data.get('user_autorized'))
