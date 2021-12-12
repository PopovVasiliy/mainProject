from Users import *
from abc import abstractmethod
from typing import Tuple, Iterable
import sqlite3
from pathlib import Path


class AbstractServerUsersStorage(object):
    @abstractmethod
    def get_all_users(self) -> Iterable[FullServerUser]:
        return NotImplemented

    @abstractmethod
    def get_user(self, nick_user: str) -> FullServerUser:
        return NotImplemented

    @abstractmethod
    def put_user_to_base(self, user: ServerUser):
        return NotImplemented

    @abstractmethod
    def delete_user_from_base(self, user: ServerUser):
        return NotImplemented


class DatabaseServerUsersStorage(AbstractServerUsersStorage):

    def __init__(self, path: Path):

        self.__connection = sqlite3.Connection(path)
        self.__dataset = self.__connection.cursor()
        self.__dataset.execute(
            'CREATE TABLE IF NOT EXISTS server_users (nick_user text PRIMARY KEY, password_user text, name_user text, status int)')

    def get_all_users(self) -> Iterable[FullServerUser]:
        yield from (self.__make_full_user(row) for row in self.__dataset.execute('SELECT * FROM server_users'))

    def get_user(self, nick_user: str) -> FullServerUser:
        rows = self.__dataset.execute('SELECT * FROM server_users WHERE nick_user=:nick_user', {'nick_user': nick_user})
        return self.__make_full_user(next(rows))

    def put_user_to_base(self, user: ServerUser):
        try:
            self.__dataset.execute(
                'INSERT INTO server_users VALUES (:nick_user, :password_user, :name_user, :status) '
                'ON CONFLICT (nick_user) DO UPDATE SET nick_user=:nick_user, password_user=:password_user, name_user=:name_user',
                (user.nick_user, user.password_user, user.name_user, 0)
            )
            self.__connection.commit()
            return True
        except Exception as Error:
            return Error

    def delete_user_from_base(self, user: ServerUser):
        try:
            self.__dataset.execute('DELETE FROM server_users WHERE nick_user=:nick_user', {'nick_user': user.nick_user})
            self.__connection.commit()
            return True
        except Exception as Error:
            return Error

    @staticmethod
    def __make_full_user(row: Tuple[str, str, str, int]) -> FullServerUser:
        return FullServerUser(ServerUser(row[0], row[1], row[2]), Status(row[3]))
