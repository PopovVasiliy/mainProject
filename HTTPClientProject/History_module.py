from datetime import datetime
from pathlib import Path
import sqlite3
from typing import Tuple
from HistoryMessage import HistoryMessage

# класс для хранения на клиенте истории сообщений пользователя. Для каждого авторизованного пользователя хранится своя история.
class HistoryMessagesDatabaseStorage(object):
    def __init__(self, path: Path):
        self.__path = path
        self.__connection = sqlite3.Connection(self.__path)
        self.__cursor = self.__connection.cursor()
        self.list_of_messages_user = []
        self.__cursor.execute(
            'CREATE TABLE IF NOT EXISTS history_messages (data_message datetime, user_recipient text, user_sender text, text_message text, user_autorized text)')

    # метод получить сообщения из истории
    def get_history_messages(self,  user_recipient: str, user_sender: str, user_autorized: str):
        _request_dict = {'user_recipient': user_recipient,
                         'user_sender': user_sender,
                         'user_autorized': user_autorized}

        text_request = 'SELECT DISTINCT  data_message as data_message, user_recipient, user_sender, text_message, user_autorized FROM history_messages WHERE user_recipient=:user_recipient AND user_sender=:user_sender AND user_autorized=:user_autorized  UNION SELECT DISTINCT data_message, user_recipient, user_sender, text_message, user_autorized FROM history_messages WHERE user_recipient=:user_sender AND user_sender=:user_recipient AND user_autorized=:user_autorized ORDER BY data_message'

        rows = self.__cursor.execute(text_request, _request_dict)

        yield from (self._make_history_message(row) for row in rows)

    # метод сохранить сообщение в истории
    def set_history_messages(self, history_message: HistoryMessage):
        self.__cursor.execute(
            'INSERT INTO history_messages VALUES (:data_message, :user_recipient, :user_sender, :text_message, :user_autorized) ', (history_message.data_message, history_message.user_recipient, history_message.user_sender, history_message.text_message, history_message.user_autorized))
        self.__connection.commit()

    # метод очистить сообщения в истории
    def clear_history_user(self, nick_user: str, user_autorized: str):
        if nick_user is None:
          self.__cursor.execute('DELETE FROM history_messages')
          self.__connection.commit()

        else:
            self.__cursor.execute('DELETE FROM history_messages  WHERE user_recipient=:nick_user AND user_autorized=:user_autorized', {'user_recipient': nick_user, 'user_autorized': user_autorized})
            self.__connection.commit()

            self.__cursor.execute('DELETE FROM history_messages  WHERE user_sender=:nick_user', {'user_sender': nick_user})
            self.__connection.commit()

    # метод преобразовать данные запроса SQL в сущность сообщения истории
    @staticmethod
    def _make_history_message(row: Tuple[datetime, str, str, str]) -> HistoryMessage:

        return HistoryMessage(row[0], row[1], row[2], row[3], row[4])
