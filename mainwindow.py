# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Tue Feb  3 16:21:37 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(521, 355)
        MainWindow.setStyleSheet("")
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.readyframe = QtGui.QFrame(self.centralWidget)
        self.readyframe.setGeometry(QtCore.QRect(650, 259, 411, 161))
        self.readyframe.setStyleSheet("background-color:white;")
        self.readyframe.setFrameShape(QtGui.QFrame.StyledPanel)
        self.readyframe.setFrameShadow(QtGui.QFrame.Raised)
        self.readyframe.setObjectName("readyframe")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.readyframe)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtGui.QLabel(self.readyframe)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setStyleSheet("#label{\n"
"    width:auto;\n"
"}")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.introframe = QtGui.QFrame(self.centralWidget)
        self.introframe.setGeometry(QtCore.QRect(650, 10, 361, 261))
        self.introframe.setStyleSheet("background-color:white;")
        self.introframe.setFrameShape(QtGui.QFrame.StyledPanel)
        self.introframe.setFrameShadow(QtGui.QFrame.Raised)
        self.introframe.setObjectName("introframe")
        self.verticalLayout = QtGui.QVBoxLayout(self.introframe)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(3, 3, 24, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setContentsMargins(200, -1, 200, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.editParticipantID = QtGui.QLineEdit(self.introframe)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(36)
        self.editParticipantID.setFont(font)
        self.editParticipantID.setStyleSheet("")
        self.editParticipantID.setAlignment(QtCore.Qt.AlignCenter)
        self.editParticipantID.setObjectName("editParticipantID")
        self.horizontalLayout.addWidget(self.editParticipantID)
        self.btnDone = QtGui.QPushButton(self.introframe)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(36)
        self.btnDone.setFont(font)
        self.btnDone.setStyleSheet("padding:0px 30px;")
        self.btnDone.setObjectName("btnDone")
        self.horizontalLayout.addWidget(self.btnDone)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.gameframe = QtGui.QFrame(self.centralWidget)
        self.gameframe.setGeometry(QtCore.QRect(0, 0, 640, 420))
        self.gameframe.setStyleSheet("background-color:white;")
        self.gameframe.setFrameShape(QtGui.QFrame.StyledPanel)
        self.gameframe.setFrameShadow(QtGui.QFrame.Raised)
        self.gameframe.setObjectName("gameframe")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gameframe)
        self.verticalLayout_4.setContentsMargins(100, 20, 100, 20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lblGlance = QtGui.QLabel(self.gameframe)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.lblGlance.setFont(font)
        self.lblGlance.setStyleSheet("background-color:#5cb85c;")
        self.lblGlance.setText("")
        self.lblGlance.setObjectName("lblGlance")
        self.verticalLayout_4.addWidget(self.lblGlance)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem4)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setContentsMargins(100, -1, 20, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.btnUp = QtGui.QPushButton(self.gameframe)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(36)
        self.btnUp.setFont(font)
        self.btnUp.setObjectName("btnUp")
        self.verticalLayout_5.addWidget(self.btnUp)
        self.btnDown = QtGui.QPushButton(self.gameframe)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(36)
        self.btnDown.setFont(font)
        self.btnDown.setObjectName("btnDown")
        self.verticalLayout_5.addWidget(self.btnDown)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.btnLabelUp = QtGui.QPushButton(self.gameframe)
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setWeight(50)
        font.setBold(False)
        self.btnLabelUp.setFont(font)
        self.btnLabelUp.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btnLabelUp.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.btnLabelUp.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.btnLabelUp.setAutoFillBackground(False)
        self.btnLabelUp.setStyleSheet("QPushButton{\n"
"    border:0px;\n"
"    margin:0px;\n"
"    padding:0px;\n"
"    color:black;\n"
"}\n"
"\n"
"")
        self.btnLabelUp.setAutoDefault(False)
        self.btnLabelUp.setFlat(True)
        self.btnLabelUp.setObjectName("btnLabelUp")
        self.verticalLayout_6.addWidget(self.btnLabelUp)
        self.btnLabelDown = QtGui.QPushButton(self.gameframe)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.btnLabelDown.setFont(font)
        self.btnLabelDown.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btnLabelDown.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.btnLabelDown.setStyleSheet("QPushButton{\n"
"    border:0px;\n"
"    margin:0px;\n"
"    padding:0px;\n"
"    color:black;\n"
"}\n"
"")
        self.btnLabelDown.setFlat(True)
        self.btnLabelDown.setObjectName("btnLabelDown")
        self.verticalLayout_6.addWidget(self.btnLabelDown)
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem6)
        spacerItem7 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem7)
        self.btnSubmit = QtGui.QPushButton(self.gameframe)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.btnSubmit.setFont(font)
        self.btnSubmit.setObjectName("btnSubmit")
        self.verticalLayout_4.addWidget(self.btnSubmit)
        self.feedbackframe = QtGui.QFrame(self.centralWidget)
        self.feedbackframe.setGeometry(QtCore.QRect(650, 110, 411, 161))
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
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.lblFeedback = QtGui.QLabel(self.feedbackframe)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(36)
        self.lblFeedback.setFont(font)
        self.lblFeedback.setStyleSheet("#label{\n"
"    width:auto;\n"
"}")
        self.lblFeedback.setObjectName("lblFeedback")
        self.horizontalLayout_3.addWidget(self.lblFeedback)
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem9)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Task is ready", None, QtGui.QApplication.UnicodeUTF8))
        self.editParticipantID.setText(QtGui.QApplication.translate("MainWindow", "Participant ID", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDone.setText(QtGui.QApplication.translate("MainWindow", "DONE", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUp.setText(QtGui.QApplication.translate("MainWindow", "▲", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDown.setText(QtGui.QApplication.translate("MainWindow", "▼", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLabelUp.setText(QtGui.QApplication.translate("MainWindow", "Missions Discover Project", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLabelDown.setText(QtGui.QApplication.translate("MainWindow", "Mistypes Missions Disavows", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSubmit.setText(QtGui.QApplication.translate("MainWindow", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.lblFeedback.setText(QtGui.QApplication.translate("MainWindow", "Correct", None, QtGui.QApplication.UnicodeUTF8))

