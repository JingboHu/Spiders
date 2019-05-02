# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(500, 400))
        MainWindow.setMaximumSize(QtCore.QSize(500, 400))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.send_pb = QtWidgets.QPushButton(self.centralwidget)
        self.send_pb.setGeometry(QtCore.QRect(180, 180, 93, 28))
        self.send_pb.setObjectName("send_pb")
        self.send_text = QtWidgets.QTextEdit(self.centralwidget)
        self.send_text.setGeometry(QtCore.QRect(0, 220, 500, 130))
        self.send_text.setObjectName("send_text")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1, 10, 105, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 100, 105, 16))
        self.label_2.setObjectName("label_2")
        self.last_text = QtWidgets.QTextEdit(self.centralwidget)
        self.last_text.setGeometry(QtCore.QRect(0, 120, 500, 50))
        self.last_text.setObjectName("last_text")
        self.first_text = QtWidgets.QTextEdit(self.centralwidget)
        self.first_text.setGeometry(QtCore.QRect(0, 30, 500, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.first_text.sizePolicy().hasHeightForWidth())
        self.first_text.setSizePolicy(sizePolicy)
        self.first_text.setObjectName("first_text")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.first_text, self.last_text)
        MainWindow.setTabOrder(self.last_text, self.send_pb)
        MainWindow.setTabOrder(self.send_pb, self.send_text)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "WeatherWarning"))
        self.send_pb.setText(_translate("MainWindow", "发送信息"))
        self.label.setText(_translate("MainWindow", "开头要说的话："))
        self.label_2.setText(_translate("MainWindow", "最后要说的话："))

