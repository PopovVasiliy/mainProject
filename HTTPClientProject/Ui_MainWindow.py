# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main_Window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(865, 634)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.list_of_users_table = QTableView(self.centralwidget)
        self.list_of_users_table.setObjectName(u"list_of_users_table")
        self.list_of_users_table.setGeometry(QRect(0, 20, 341, 411))
        self.label1 = QLabel(self.centralwidget)
        self.label1.setObjectName(u"label1")
        self.label1.setGeometry(QRect(10, 0, 241, 21))
        self.label1.setAlignment(Qt.AlignCenter)
        self.connect_server_pushButton = QPushButton(self.centralwidget)
        self.connect_server_pushButton.setObjectName(u"connect_server_pushButton")
        self.connect_server_pushButton.setGeometry(QRect(0, 570, 151, 23))
        self.connect_server_pushButton.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.listView = QListView(self.centralwidget)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(350, 20, 511, 411))
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(350, 450, 511, 111))
        self.label2 = QLabel(self.centralwidget)
        self.label2.setObjectName(u"label2")
        self.label2.setGeometry(QRect(350, 0, 211, 20))
        self.label3 = QLabel(self.centralwidget)
        self.label3.setObjectName(u"label3")
        self.label3.setGeometry(QRect(350, 430, 441, 21))
        self.send_message = QPushButton(self.centralwidget)
        self.send_message.setObjectName(u"send_message")
        self.send_message.setGeometry(QRect(350, 570, 511, 23))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(0, 440, 341, 121))
        self.label4 = QLabel(self.groupBox)
        self.label4.setObjectName(u"label4")
        self.label4.setGeometry(QRect(10, 20, 121, 16))
        self.label5 = QLabel(self.groupBox)
        self.label5.setObjectName(u"label5")
        self.label5.setGeometry(QRect(10, 50, 121, 16))
        self.label6 = QLabel(self.groupBox)
        self.label6.setObjectName(u"label6")
        self.label6.setGeometry(QRect(10, 80, 121, 16))
        self.adress_server = QLineEdit(self.groupBox)
        self.adress_server.setObjectName(u"adress_server")
        self.adress_server.setGeometry(QRect(150, 20, 181, 20))
        self.nick_user = QLineEdit(self.groupBox)
        self.nick_user.setObjectName(u"nick_user")
        self.nick_user.setGeometry(QRect(150, 50, 181, 20))
        self.password_user = QLineEdit(self.groupBox)
        self.password_user.setObjectName(u"password_user")
        self.password_user.setGeometry(QRect(150, 80, 181, 20))
        self.disconnect_server_pushButton = QPushButton(self.centralwidget)
        self.disconnect_server_pushButton.setObjectName(u"disconnect_server_pushButton")
        self.disconnect_server_pushButton.setGeometry(QRect(190, 570, 151, 23))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 865, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0441\u0441\u0435\u043d\u0434\u0436\u0435\u0440 \u0434\u043b\u044f \u043d\u0430\u0447\u0438\u043d\u0430\u044e\u0449\u0438\u0445", None))
        self.label1.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0438\u0441\u043e\u043a \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439", None))
        self.connect_server_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f", None))
        self.textEdit.setMarkdown("")
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label2.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0441\u0442\u043e\u0440\u0438\u044f \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0439", None))
        self.label3.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435:", None))
        self.send_message.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u043b\u0430\u0442\u044c \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0434\u0430\u043d\u043d\u044b\u0435 \u0434\u043b\u044f \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f:", None))
        self.label4.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0434\u0440\u0435\u0441 \u0441\u0435\u0440\u0432\u0435\u0440\u0430:", None))
        self.label5.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f:", None))
        self.label6.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0440\u043e\u043b\u044c \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f:", None))
        self.disconnect_server_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f", None))
    # retranslateUi

