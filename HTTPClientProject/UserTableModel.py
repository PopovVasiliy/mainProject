from PySide2.QtCore import Slot, Qt, QAbstractTableModel, QModelIndex, QTimer

from UserApiProvider import UserApiProvider


# класс табличной модели для списка пользователей - подгружиется по таймеру раз в 10 сек
class UserTableModel(QAbstractTableModel):
    __update_timeout = 10_000
    __columns = ['nick_user', 'name_user', 'status']

    def __init__(self, provider, parent=None):
        super().__init__(parent)
        self.__api: UserApiProvider = provider
        self._users = []

        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.update_model)
        self.__timer.start(self.__update_timeout)
        self.update_model()

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.__columns)

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._users)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row, column = index.row(), index.column()

            if row < self.rowCount() and column < self.columnCount():
                return self.__get_display_data(row, column)

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        return self.__columns[section] \
                if orientation == Qt.Horizontal and role == Qt.DisplayRole \
                else None

    def note(self, row):
        return self.__notes[row]

    @Slot()
    def update_model(self):
        users = self.__api.get_users()

        if users != self._users:
            self.beginResetModel()
            self._users = users
            self.endResetModel()

    def __get_display_data(self, row: int, column: int) -> str:
        return self._users[row][self.__columns[column]]
