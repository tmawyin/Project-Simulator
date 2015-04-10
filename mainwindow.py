# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sat Mar 28 15:49:25 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(806, 590)
        MainWindow.setStyleSheet("")
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.introframe = QtGui.QFrame(self.centralWidget)
        self.introframe.setGeometry(QtCore.QRect(0, 430, 361, 261))
        self.introframe.setStyleSheet("background-color:white;")
        self.introframe.setFrameShape(QtGui.QFrame.StyledPanel)
        self.introframe.setFrameShadow(QtGui.QFrame.Raised)
        self.introframe.setObjectName("introframe")
        self.verticalLayout = QtGui.QVBoxLayout(self.introframe)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(3, 3, 24, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setContentsMargins(200, -1, 200, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.editParticipantID = QtGui.QLineEdit(self.introframe)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(42)
        self.editParticipantID.setFont(font)
        self.editParticipantID.setStyleSheet("")
        self.editParticipantID.setAlignment(QtCore.Qt.AlignCenter)
        self.editParticipantID.setObjectName("editParticipantID")
        self.horizontalLayout.addWidget(self.editParticipantID)
        self.btnDone = QtGui.QPushButton(self.introframe)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(42)
        self.btnDone.setFont(font)
        self.btnDone.setStyleSheet("padding:0px 30px;")
        self.btnDone.setObjectName("btnDone")
        self.horizontalLayout.addWidget(self.btnDone)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gameframe = QtGui.QFrame(self.centralWidget)
        self.gameframe.setGeometry(QtCore.QRect(160, 0, 640, 420))
        self.gameframe.setStyleSheet("background-color:white;")
        self.gameframe.setFrameShape(QtGui.QFrame.StyledPanel)
        self.gameframe.setFrameShadow(QtGui.QFrame.Raised)
        self.gameframe.setObjectName("gameframe")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gameframe)
        self.verticalLayout_4.setContentsMargins(100, 20, 100, 20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lblGlance = QtGui.QLabel(self.gameframe)
        font = QtGui.QFont()
        font.setPointSize(42)
        self.lblGlance.setFont(font)
        self.lblGlance.setStyleSheet("")
        self.lblGlance.setText("")
        self.lblGlance.setObjectName("lblGlance")
        self.verticalLayout_4.addWidget(self.lblGlance)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setContentsMargins(100, -1, 20, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.btnUp = QtGui.QPushButton(self.gameframe)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(42)
        self.btnUp.setFont(font)
        self.btnUp.setObjectName("btnUp")
        self.verticalLayout_5.addWidget(self.btnUp)
        self.btnDown = QtGui.QPushButton(self.gameframe)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(42)
        self.btnDown.setFont(font)
        self.btnDown.setObjectName("btnDown")
        self.verticalLayout_5.addWidget(self.btnDown)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.btnLabelUp = QtGui.QPushButton(self.gameframe)
        font = QtGui.QFont()
        font.setPointSize(42)
        font.setWeight(50)
        font.setBold(False)
        self.btnLabelUp.setFont(font)
        self.btnLabelUp.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btnLabelUp.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.btnLabelUp.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnLabelUp.setAutoFillBackground(False)
        self.btnLabelUp.setStyleSheet("QPushButton{ border:0px; margin:0px; padding:0px; color:black; text-align:left;}\n"
"\n"
"")
        self.btnLabelUp.setAutoDefault(False)
        self.btnLabelUp.setFlat(True)
        self.btnLabelUp.setObjectName("btnLabelUp")
        self.verticalLayout_6.addWidget(self.btnLabelUp)
        self.btnLabelDown = QtGui.QPushButton(self.gameframe)
        font = QtGui.QFont()
        font.setPointSize(42)
        self.btnLabelDown.setFont(font)
        self.btnLabelDown.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btnLabelDown.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnLabelDown.setStyleSheet("QPushButton{ border:0px; margin:0px; padding:0px;    color:black; text-align:left;}")
        self.btnLabelDown.setFlat(True)
        self.btnLabelDown.setObjectName("btnLabelDown")
        self.verticalLayout_6.addWidget(self.btnLabelDown)
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem4)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem5)
        self.btnSubmit = QtGui.QPushButton(self.gameframe)
        font = QtGui.QFont()
        font.setPointSize(42)
        self.btnSubmit.setFont(font)
        self.btnSubmit.setObjectName("btnSubmit")
        self.verticalLayout_4.addWidget(self.btnSubmit)
        self.feedbackframe = QtGui.QFrame(self.centralWidget)
        self.feedbackframe.setGeometry(QtCore.QRect(520, 430, 411, 161))
        self.feedbackframe.setStyleSheet("background-color:white;")
        self.feedbackframe.setFrameShape(QtGui.QFrame.StyledPanel)
        self.feedbackframe.setFrameShadow(QtGui.QFrame.Raised)
        self.feedbackframe.setObjectName("feedbackframe")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.feedbackframe)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.lblFeedback = QtGui.QLabel(self.feedbackframe)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(42)
        self.lblFeedback.setFont(font)
        self.lblFeedback.setStyleSheet("#label{\n"
"    width:auto;\n"
"}")
        self.lblFeedback.setObjectName("lblFeedback")
        self.horizontalLayout_3.addWidget(self.lblFeedback)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.readyframe = QtGui.QFrame(self.centralWidget)
        self.readyframe.setGeometry(QtCore.QRect(20, 30, 721, 531))
        self.readyframe.setStyleSheet("background-color:white;")
        self.readyframe.setFrameShape(QtGui.QFrame.StyledPanel)
        self.readyframe.setFrameShadow(QtGui.QFrame.Raised)
        self.readyframe.setObjectName("readyframe")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.readyframe)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        spacerItem8 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.verticalLayout_7.addItem(spacerItem8)
        self.lblGlance_2 = QtGui.QLabel(self.readyframe)
        self.lblGlance_2.setText("")
        self.lblGlance_2.setObjectName("lblGlance_2")
        self.verticalLayout_7.addWidget(self.lblGlance_2)
        spacerItem9 = QtGui.QSpacerItem(20, 100, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.verticalLayout_7.addItem(spacerItem9)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem10 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem10)
        self.label = QtGui.QLabel(self.readyframe)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(42)
        self.label.setFont(font)
        self.label.setStyleSheet("#label{\n"
"    width:auto;\n"
"}")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem11)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        spacerItem12 = QtGui.QSpacerItem(20, 200, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.verticalLayout_7.addItem(spacerItem12)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem13 = QtGui.QSpacerItem(100, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem13)
        self.btnStart = QtGui.QPushButton(self.readyframe)
        font = QtGui.QFont()
        font.setPointSize(42)
        self.btnStart.setFont(font)
        self.btnStart.setObjectName("btnStart")
        self.horizontalLayout_5.addWidget(self.btnStart)
        spacerItem14 = QtGui.QSpacerItem(100, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem14)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        spacerItem15 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.verticalLayout_7.addItem(spacerItem15)
        self.verticalLayout_2.addLayout(self.verticalLayout_7)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.editParticipantID.setText(QtGui.QApplication.translate("MainWindow", "Participant ID", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDone.setText(QtGui.QApplication.translate("MainWindow", "DONE", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUp.setText(QtGui.QApplication.translate("MainWindow", "▲", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDown.setText(QtGui.QApplication.translate("MainWindow", "▼", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLabelUp.setText(QtGui.QApplication.translate("MainWindow", "Missions Discover Project", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLabelDown.setText(QtGui.QApplication.translate("MainWindow", "Mistypes Missions Disavows", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSubmit.setText(QtGui.QApplication.translate("MainWindow", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.lblFeedback.setText(QtGui.QApplication.translate("MainWindow", "Correct", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Task is ready", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStart.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))

