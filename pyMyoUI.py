# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyMyo.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from base64 import b64decode
from pyMyoPath import myoPath
from logo import img as logo

linkpath = myoPath()

sss = os.path.exists(linkpath + r'\logo.png')
if not sss:
    tmp = open(linkpath + r'\logo.png', 'wb')
    tmp.write(b64decode(logo))
    tmp.close()
else:
    pass


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1568, 843)
        Form.setFixedSize(Form.width(), Form.height())

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(linkpath + r'\logo.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.plotGroup = QtWidgets.QGroupBox(Form)
        self.plotGroup.setGeometry(QtCore.QRect(10, 10, 1231, 821))
        self.plotGroup.setTitle("")
        self.plotGroup.setObjectName("plotGroup")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.plotGroup)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1211, 801))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.graph_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.graph_layout.setContentsMargins(0, 0, 0, 0)
        self.graph_layout.setObjectName("graph_layout")
        self.funcArea = QtWidgets.QGroupBox(Form)
        self.funcArea.setGeometry(QtCore.QRect(1280, 10, 261, 141))
        self.funcArea.setTitle("")
        self.funcArea.setObjectName("funcArea")
        self.layoutWidget = QtWidgets.QWidget(self.funcArea)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 221, 101))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.rssi = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.rssi.setFont(font)
        self.rssi.setObjectName("rssi")
        self.gridLayout.addWidget(self.rssi, 0, 0, 1, 1)
        self.setRSSI = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.setRSSI.setFont(font)
        self.setRSSI.setText("")
        self.setRSSI.setObjectName("setRSSI")
        self.gridLayout.addWidget(self.setRSSI, 0, 1, 1, 1)
        self.rssi_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.rssi_2.setFont(font)
        self.rssi_2.setObjectName("rssi_2")
        self.gridLayout.addWidget(self.rssi_2, 1, 0, 1, 1)
        self.setBETTERY = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.setBETTERY.setFont(font)
        self.setBETTERY.setText("")
        self.setBETTERY.setObjectName("setBETTERY")
        self.gridLayout.addWidget(self.setBETTERY, 1, 1, 1, 1)
        self.btnGroup = QtWidgets.QGroupBox(Form)
        self.btnGroup.setGeometry(QtCore.QRect(1280, 170, 261, 321))
        self.btnGroup.setTitle("")
        self.btnGroup.setObjectName("btnGroup")
        self.connectBtn = QtWidgets.QPushButton(self.btnGroup)
        self.connectBtn.setGeometry(QtCore.QRect(10, 20, 111, 61))
        self.connectBtn.setObjectName("connectBtn")
        self.disConnectBtn = QtWidgets.QPushButton(self.btnGroup)
        self.disConnectBtn.setGeometry(QtCore.QRect(140, 20, 111, 61))
        self.disConnectBtn.setObjectName("disConnectBtn")
        self.startBtn = QtWidgets.QPushButton(self.btnGroup)
        self.startBtn.setGeometry(QtCore.QRect(50, 100, 161, 101))
        self.startBtn.setObjectName("startBtn")
        self.saveBtn = QtWidgets.QPushButton(self.btnGroup)
        self.saveBtn.setGeometry(QtCore.QRect(50, 210, 161, 101))
        self.saveBtn.setObjectName("saveBtn")
        self.msgGroup = QtWidgets.QGroupBox(Form)
        self.msgGroup.setGeometry(QtCore.QRect(1280, 510, 261, 321))
        self.msgGroup.setTitle("")
        self.msgGroup.setObjectName("msgGroup")
        self.msgBrowser = QtWidgets.QTextBrowser(self.msgGroup)
        self.msgBrowser.setGeometry(QtCore.QRect(10, 10, 241, 251))
        self.msgBrowser.setObjectName("msgBrowser")
        self.label = QtWidgets.QLabel(self.msgGroup)
        self.label.setGeometry(QtCore.QRect(10, 270, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "pyMyo"))
        self.rssi.setText(_translate("Form", "RSSI:"))
        self.rssi_2.setText(_translate("Form", "BETTERY:"))
        self.connectBtn.setText(_translate("Form", "Connect"))
        self.disConnectBtn.setText(_translate("Form", "Disconnect"))
        self.startBtn.setText(_translate("Form", "Start"))
        self.saveBtn.setText(_translate("Form", "Save"))
        self.label.setText(_translate("Form", "KEY ALT can also save EMG "))
