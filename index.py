import sys

from PySide import QtCore, QtGui
from PySide.QtGui import QMainWindow, QPushButton, QApplication, QDesktopWidget
from mainwindow import Ui_MainWindow
import numpy as np

class MainWindow(QMainWindow, Ui_MainWindow):	
	def __init__(self, parent = None):
		# Define variables
		self.txtList = np.genfromtxt('largeSet.txt',dtype='str',delimiter='\n')
		self.ansSheet = np.genfromtxt('largeAnsSet.txt',dtype='int',delimiter='\n')
		self.counter = 0
		self.response = -1

		# Set up the GUI
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		
		# Hide all the frames except the initial
		self.readyframe.hide()
		self.feedbackframe.hide()
		self.gameframe.hide()	
		self.showFullScreen()
		
		# Setting the frames to be full screen
		desktop = QDesktopWidget()
		width = desktop.geometry().width()
		height = desktop.geometry().height()

		self.introframe.move(0,0)
		self.introframe.resize(width, height)
		self.readyframe.move(0,0)		
		self.readyframe.resize(width, height)
		self.feedbackframe.move(0,0)
		self.feedbackframe.resize(width, height)
		self.gameframe.move(0,0)
		self.gameframe.resize(width, height)

		''' BUTTONS '''
		# Button "DONE" on click
		QtCore.QObject.connect(self.btnDone, QtCore.SIGNAL("clicked()"), self.showReadyFrame)
		# Moving UP/DOWN buttons
		QtCore.QObject.connect(self.btnUp, QtCore.SIGNAL("clicked()"), self.moveUp)
		QtCore.QObject.connect(self.btnDown, QtCore.SIGNAL("clicked()"), self.moveDown)
		# Selecting buttons
		QtCore.QObject.connect(self.btnLabelUp, QtCore.SIGNAL("clicked()"), self.Uphighlight)
		QtCore.QObject.connect(self.btnLabelDown, QtCore.SIGNAL("clicked()"), self.Downhighlight)
		# Button "SUBMIT" on click
		QtCore.QObject.connect(self.btnSubmit, QtCore.SIGNAL("clicked()"), self.submitFun)

	''' HIGHLIGHTING BUTTONS '''
	# This modifies the highligh sequence of the labels
	def Uphighlight(self):
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:white;background-color:blue;}")
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;}")
		self.response = self.counter
	def Downhighlight(self):
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:white;background-color:blue;}")
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;}")
		tmp = self.counter
		self.response = tmp+1

	''' UP/DOWN BUTTONS '''
	# Functions for moving up or down in the text file
	def moveUp(self):
		if self.counter == 0:
			self.counter = 0
		else:
			self.counter = self.counter - 1
		# Modifying labels from buttons
		self.response = -1
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;}")
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;}")
		# Setting up labels
		counter = self.counter
		self.btnLabelUp.setText(QtGui.QApplication.translate("MainWindow",self.txtList[counter] , None, QtGui.QApplication.UnicodeUTF8))
		self.btnLabelDown.setText(QtGui.QApplication.translate("MainWindow",self.txtList[counter+1] , None, QtGui.QApplication.UnicodeUTF8))

	def moveDown(self):
		if self.counter == len(self.txtList)-2:
			self.counter = len(self.txtList)-2
		else:
			self.counter = self.counter + 1
		# Modifying labels from buttons
		self.response = -1
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;}")
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;}")
		# Setting up labels
		counter = self.counter
		self.btnLabelUp.setText(QtGui.QApplication.translate("MainWindow",self.txtList[counter] , None, QtGui.QApplication.UnicodeUTF8))
		self.btnLabelDown.setText(QtGui.QApplication.translate("MainWindow",self.txtList[counter+1] , None, QtGui.QApplication.UnicodeUTF8))

	''' SHOW/HIDE FRAMES '''
	# Showing all required frames
	def showReadyFrame(self):
		self.introframe.hide()
		self.readyframe.show()
		# Wait for 2 seconds before calling the game screen
		timer = QtCore.QTimer()
		timer.singleShot(2000, self.showGameFrame)

	def showGameFrame(self):
		self.response = -1
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;}")
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;}")
		self.readyframe.hide()
		self.feedbackframe.hide()
		self.gameframe.show()

	def submitFun(self):
		if self.ansSheet[self.response] == 0:
			self.lblFeedback.setText(QtGui.QApplication.translate("MainWindow", "Incorrect", None, QtGui.QApplication.UnicodeUTF8))
		if self.ansSheet[self.response] == 1:
			self.lblFeedback.setText(QtGui.QApplication.translate("MainWindow", "Correct", None, QtGui.QApplication.UnicodeUTF8))
		self.gameframe.hide()
		self.feedbackframe.show()
		timer = QtCore.QTimer()
		timer.singleShot(1000, self.showGameFrame)

		
if __name__=='__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()
	app.exec_()
