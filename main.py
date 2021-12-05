# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from enum import Enum
from datetime import datetime


class Status(Enum):
    online = 0
    offline = 1
    printing = 2

# Первоначальная версия


list_of_Users = []
list_of_messages = []
list_of_commands = []


class ClientUsers:
    def __init__(self, nick_user: str, name_user: str, status: Status):
        self._nick_user = nick_user
        self._name_user = name_user
        self._status = status

    # ///////получить список пользователей ///////
    @property
    def get_users(self):
        return list_of_Users

    # здесь будет добавлен код
    @staticmethod
    def get_users_from_server():
        return None


class HistoryMessages:
    def __init__(self, message_datetime: datetime, message_user: ClientUsers, message_text: str):
        self._message_datetime = message_datetime
        self._message_user = message_user
        self._message_text = message_text

    # добавить сообщение в историю сообщений
    def set_message_in_history(self):
        list_of_messages.append(self)

    # получить историю сообщений по пользователю
    @staticmethod
    def get_history_messages(user: ClientUsers = None):
        if user is None:
            return list_of_messages
        else:
            list_of_messages_user = []
            for elem in list_of_messages:
                if elem.message_user == user:
                    list_of_messages_user.append(elem)
            return list_of_messages_user

    # очистить историю сообщений по пользователю
    @staticmethod
    def clear_history_user(user: ClientUsers = None):
        if user is None:
            list_of_Users.clear()
        else:
            pulldel = 0
            while pulldel == 0:
                for elem in list_of_messages:
                    if elem.message_user == user:
                        list_of_messages.remove(elem)
                        break
                    pulldel = 1


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
