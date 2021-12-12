import datetime
from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import Slot, QTimer, QStringListModel
from History_module import *
from UserTableModel import UserTableModel
from UserApiProvider import UserApiProvider
from HistoryMessage import HistoryMessage
from Ui_MainWindow import Ui_MainWindow
from warnings import warn


class MainWindow(QMainWindow):
    # переменная длительности таймера для обработчика, который раз в 2 секунды проверяет очередь сообщения на сервере
    __timer_update_timeout_queue_message = 2_000

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__HistoryMessagesDatabaseStorage = HistoryMessagesDatabaseStorage(Path('history_messages.db'))
        # эта модель используется для обновления списка пользователя актуальной информацией с сервера(окно list_of_users_table)
        self.__model = None
        # эта модель используется для обновления истории сообщений на клиенте(окно listView)
        self.model_1 = QStringListModel(self)
        self.__ui.adress_server.setText('http://localhost:8080')
        self.__ui.nick_user.setText('loki')
        self.__ui.password_user.setText('123456')
        self.__UserApiProvider = UserApiProvider(self.__ui.adress_server.text())
        # сигналы элементов графического интерфейса для соотв слотов
        self.__ui.connect_server_pushButton.clicked.connect(self.autorise_to_server)
        self.__ui.list_of_users_table.clicked.connect(self.select_user_on_string)
        self.__ui.send_message.clicked.connect(self.send_message_to_server)
        self.__ui.disconnect_server_pushButton.clicked.connect(self.disconnect_from_server)
        # сигнал таймера для периодической проверки сообщений на сервере
        self.__timer_queue_message = QTimer(self)
        self.__timer_queue_message.timeout.connect(self.get_messages_from_server)
        self.__timer_queue_message.start(self.__timer_update_timeout_queue_message)

    @Slot()
    # Обработчик выбора пользователя для отправки сообщения на списке пользователей
    def select_user_on_string(self):

        list_of_ind = self.__ui.list_of_users_table.selectedIndexes()
        if len(list_of_ind) != 0:
            row = list_of_ind[0].row()
            item_list = []
            for HMes in self.__HistoryMessagesDatabaseStorage.get_history_messages(self.__ui.nick_user.text(), self.__model._users[row]['nick_user'], self.__ui.nick_user.text()):
                item_list.append(str(HMes.data_message) + '  ' + HMes.user_sender)
                item_list.append(HMes.text_message)

            self.model_1.setStringList(item_list)
            self.__ui.listView.setModel(self.model_1)

    @Slot()
    # Обработчик нажатия на кнопку "подключиться" - авторизация на сервере
    def autorise_to_server(self):

        dict_to_send_user = {'nick_user': str(self.__ui.nick_user.text()),
                             'password_user': str(self.__ui.password_user.text())}
        try:
            self.__UserApiProvider = UserApiProvider(self.__ui.adress_server.text())
            request_to_serv = self.__UserApiProvider.autorize_user(dict_to_send_user)
            if request_to_serv.get('ErrorKode', 'Error') == 'OK':

                self.__model = UserTableModel(self.__UserApiProvider, self)
                self.__ui.list_of_users_table.setModel(self.__model)
                self.__model.update_model()
            else:
                self.__ui.list_of_users_table.setModel(None)
        except Exception as error:
            print(error)

    @Slot()
    # обработчик нажатия кнопки посылки сообщения пользователю
    def send_message_to_server(self):

        list_of_ind = self.__ui.list_of_users_table.selectedIndexes()
        if len(list_of_ind) != 0:
            nick_user_recipient = self.__model._users[list_of_ind[0].row()]['nick_user']

            if nick_user_recipient == self.__ui.nick_user.text():
                warn('Нельзя отправлять сообщения самому себе!')
            else:

                dict_to_send_message = {'command': 'send_message',
                                        'user_recipient':  str(nick_user_recipient),
                                        'user_sender': str(self.__ui.nick_user.text()),
                                        'text_message': str(self.__ui.textEdit.toMarkdown())
                                        }
                try:
                    request_to_serv = self.__UserApiProvider.send_message(dict_to_send_message)
                    if request_to_serv.get('ErrorKode', 'Error') == 'OK':

                        self.__HistoryMessagesDatabaseStorage.set_history_messages(HistoryMessage.dict_to_HistoryMessage({**dict_to_send_message, **{'data_message': datetime.now(), 'user_autorized': self.__ui.nick_user.text()}}))
                        self.__ui.textEdit.clear()
                        self.select_user_on_string()
                        print('OK')

                    else:
                        print('Error')
                except Exception as error:
                    print(error)

    @Slot()
    # обработчик, срабатывающий по таймеру - проверяет очередь сообщений на сервере
    # и подгружает сообщения, пришедшие авторизованному в клиенте пользователю
    # также там прописано обновление истории сообщений - чтобы полученные сообщения сразу отображались для пользователя
    def get_messages_from_server(self):

        nick_user_recipient = str(self.__ui.nick_user.text())
        dict_to_send_message = {'command': 'get_message',
                                'user_recipient': str(nick_user_recipient),
                                'user_sender': '',
                                'text_message': ''
                                }
        if self.__model is not None:
            try:
                request_from_serv1 = self.__UserApiProvider.send_message(dict_to_send_message)
                for _message in request_from_serv1:
                    self.__HistoryMessagesDatabaseStorage.set_history_messages(HistoryMessage.dict_to_HistoryMessage({**dict(_message), **{'user_autorized': self.__ui.nick_user.text()}}))
            except Exception as error:
                print(error)

            try:
                self.select_user_on_string()
            except Exception as error:
                print(error)

    @Slot()
    # обработчик кнопки отключения от сервера
    def disconnect_from_server(self):
        self.__ui.list_of_users_table.setModel(None)
        self.__ui.listView.setModel(None)
        self.__ui.textEdit.clear()
        self.__UserApiProvider = None

