from UserStorage import *
from ServerMessages import ServerMessage
from datetime import datetime


class AbstractQueueMessageStorage:
    def __init__(self):
        self._QueueMessage = []

    @abstractmethod
    def get_messages_sender(self, user: FullServerUser):
        return NotImplemented

    @abstractmethod
    def get_messages_recipient(self, user: FullServerUser):
        return NotImplemented

    @abstractmethod
    def get_all_messages(self):
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

    def get_messages_sender(self, user: FullServerUser):
        text_of_request = 'SELECT * FROM queue_message WHERE nick_user_sender = :nick_user_sender'
        yield from (self.__make_server_messages(row) for row in
                    self.__dataset.execute(text_of_request, {'nick_user_sender': user.ServerUser.nick_user}))

    def get_messages_recipient(self, user: FullServerUser):
        text_of_request = 'SELECT * FROM queue_message WHERE nick_user_recipient = :nick_user_recipient'
        yield from (self.__make_server_messages(row) for row in
                    self.__dataset.execute(text_of_request, {'nick_user_recipient': user.ServerUser.nick_user}))

    def get_all_messages(self):
        text_of_request = 'SELECT * FROM queue_message'
        yield from (self.__make_server_messages(row) for row in self.__dataset.execute(text_of_request))

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
