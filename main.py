# Приложение-сервер

from enum import Enum
from dataclasses import dataclass
from abc import abstractmethod
from typing import Iterable, Tuple
import sqlite3
import asyncio
from pathlib import Path
from datetime import datetime
from asyncio.streams import StreamReader, StreamWriter
import logging
import logger

class Status(Enum):
    online = 0
    offline = 1
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


@dataclass
class ServerMessage:
    data_message: datetime
    user_recipient: FullServerUser
    user_sender: FullServerUser
    text_message: str


class AbstractServerUser:
    def __init__(self, server_user: ServerUser, status: Status):
        self._server_user = server_user
        self._status = status
        self._server_user_list = []

    @abstractmethod
    def get_all_users(self):
        return NotImplemented

    @abstractmethod
    def put_user_to_base(self):
        return NotImplemented

    @abstractmethod
    def delete_user_from_base(self):
        return NotImplemented


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


class AbstractQueueMessageStorage:
    def __init__(self):
        self._QueueMessage = []

    @abstractmethod
    def get_messages(self, user: FullServerUser):
        return NotImplemented

    @abstractmethod
    def put_message(self, server_message: ServerMessage):
        return NotImplemented

    @abstractmethod
    def clear_messages(self, user: FullServerUser):
        return NotImplemented


class DatabaseQueueMessageStorage(AbstractQueueMessageStorage):

    def __init__(self, path: Path, user_storage: AbstractServerUsersStorage):
        super(DatabaseQueueMessageStorage, self).__init__()

        self.__user_storage = user_storage
        self.__connection = sqlite3.Connection(path)
        self.__dataset = self.__connection.cursor()
        self.__dataset.execute(
            'CREATE TABLE IF NOT EXISTS queue_message (data_message datetime, nick_user_recipient text, nick_user_sender text, text_message text)')

    def get_messages(self, user: FullServerUser):
        text_of_request = 'SELECT * FROM queue_message WHERE nick_user_recipient = :nick_user_recipient'
        yield from (self.__make_server_messages(row) for row in
                    self.__dataset.execute(text_of_request, {'nick_user_recipient': user.ServerUser.nick_user}))

    def put_message(self, server_message: ServerMessage):
        try:
            self.__dataset.execute(
                'INSERT INTO queue_message VALUES (:data_message, :nick_user_recipient, :nick_user_sender, :text_message) ',
                (server_message.data_message, server_message.user_recipient.ServerUser.nick_user, server_message.user_sender.ServerUser.nick_user,
                 server_message.text_message)
            )
            self.__connection.commit()
            return True
        except Exception as Error:
            return Error

    def clear_messages(self, user: FullServerUser):
        try:
            text_of_request = 'DELETE FROM queue_message WHERE nick_user_recipient = :nick_user_recipient'
            self.__dataset.execute(text_of_request, {'nick_user_recipient': user.ServerUser.nick_user})
            self.__connection.commit()
            return True
        except Exception as Error:
            return Error

    def __make_server_messages(self, row: Tuple[datetime, str, str, str]) -> ServerMessage:
        return ServerMessage(row[0], self.__user_storage.get_user(row[1]), self.__user_storage.get_user(row[2]), row[3])

class AbstractCommand(object):
    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self._reader = reader
        self._writer = writer

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def can_execute(self, command: str) -> bool:
        pass

    @abstractmethod
    async def execute(self, line: str):
        pass

    async def _readline(self):
        return (await self._reader.readline()).decode().strip()

    def _writeline(self, line: str):
        self._writer.write((line + '\n').encode())


class UserConnected(AbstractCommand):
    @property
    def name(self) -> str:
        return 'UserConnected'

    def can_execute(self, command: str) -> bool:
        return self.name == command

    async def execute(self, line: str):
        self._writer.write((line + ' command request2').encode())



class SendServerMessage(AbstractCommand):
    @property
    def name(self) -> str:
        return 'SendServerMessage'

    def can_execute(self, command: str) -> bool:
        return self.name == command

    async def execute(self, line: str):
        self._writer.write((line + ' command request1').encode())



class CommandFactory(object):
    class __UnknownCommand(AbstractCommand):
        @property
        def name(self) -> str:
            raise NotImplementedError

        def can_execute(self, command: str) -> bool:
            self.__command = command
            return True

        async def execute(self, line: str):
            self._writeline('Error: "Unknown command"')

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.__reader = reader
        self.__writer = writer
        self.commands = [
            UserConnected(self.__reader, self.__writer),
            SendServerMessage(self.__reader, self.__writer),
        ]

    # def get_command(self, command: str) -> AbstractCommand:
    #     return self._commands.get(command, self.__UnknownCommand)(
    #         self.__storage, self.__reader, self.__writer
    #     )
    def get_command(self, line: str) -> AbstractCommand:
        for command in self.commands:
            if command.can_execute(line):
                return command


class CommandProcessor(object):

    async def __call__(self, reader: StreamReader, writer: StreamWriter):
        # получаем информацию о созданном соединении
        host, port = writer.transport.get_extra_info('peername')

        logging.info(f'Connected to: {host}:{port}')

        factory = CommandFactory(reader, writer)

        while not writer.is_closing():
            # построчно читаем команды и выполняем их
            line = (await reader.readline()).decode().strip()
            command = factory.get_command(line)
            await command.execute(line)

        logging.info(f'Disconnected from {host}:{port}')


def test_myserver_user_storage():
    print('begining')
    our_user1 = ServerUser('loki', '123456', 'Василий')
    our_user2 = ServerUser('iv', '654321', 'Иван')
    our_user3 = ServerUser('dartveider', '7819', 'Самый злой')

    user_storage = DatabaseServerUsersStorage(Path('server_users_base.db'))

    res = user_storage.put_user_to_base(our_user1)
    if res is not True:
        print(res)
    res = user_storage.put_user_to_base(our_user2)
    if res is not True:
        print(res)

    res = user_storage.put_user_to_base(our_user3)
    if res is not True:
        print(res)

    # res = user_storage.delete_user_from_base(our_user2)
    # if res is not True:
    #     print(res)

    for index, elem_user in enumerate(user_storage.get_all_users()):
        print(index, ", ", elem_user.ServerUser)

    print(user_storage.get_user(our_user1.nick_user).ServerUser.name_user)

    print('The end')


def test_myserver_queue_message_storage():
    print('begining')

    our_user1 = ServerUser('loki', '123456', 'Василий')
    our_user2 = ServerUser('iv', '654321', 'Иван')
    our_user3 = ServerUser('dartveider', '7819', 'Самый злой')

    user_storage = DatabaseServerUsersStorage(Path('server_users_base.db'))

    message1 = ServerMessage(datetime.now(), user_storage.get_user(our_user2.nick_user), user_storage.get_user(our_user2.nick_user), 'тестовое сообщение123')
    message2 = ServerMessage(datetime.now(), user_storage.get_user(our_user1.nick_user), user_storage.get_user(our_user3.nick_user), 'тестовое сообщение456')
    message3 = ServerMessage(datetime.now(), user_storage.get_user(our_user1.nick_user),
                             user_storage.get_user(our_user2.nick_user), 'тестовое сообщение789')

    queue_messages = DatabaseQueueMessageStorage(Path('queue_messages.db'), user_storage)

    # res = queue_messages.put_message(message1)
    # if res is not True:
    #     print(res)
    #
    # res = queue_messages.put_message(message2)
    # if res is not True:
    #     print(res)
    #
    # res = queue_messages.put_message(message3)
    # if res is not True:
    #     print(res)
    res = queue_messages.clear_messages(user_storage.get_user(our_user1.nick_user))
    if res is not True:
        print(res)

    res = queue_messages.clear_messages(user_storage.get_user(our_user2.nick_user))
    if res is not True:
        print(res)

    res = queue_messages.clear_messages(user_storage.get_user(our_user3.nick_user))
    if res is not True:
        print(res)


    for elem in queue_messages.get_messages(user_storage.get_user(our_user2.nick_user)):
        print(elem)

    print('The end')

async def test_async_await_tcp_server():

    processor = CommandProcessor()

    # запускаем сервер на localhost:3333
    server = await asyncio.start_server(processor, '192.168.1.185', 3335)
    logging.info('Server started')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    # test_myserver_user_storage()
    # test_myserver_queue_message_storage()
    logger.configure_logger('tcp_server_example')

    try:
        asyncio.run(test_async_await_tcp_server())
    except KeyboardInterrupt:
        logging.info('Server stopped')
