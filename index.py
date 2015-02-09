import sys

from PySide import QtCore, QtGui
from PySide.QtGui import QMainWindow, QPushButton, QApplication, QDesktopWidget
from mainwindow import Ui_MainWindow
import csv
import numpy as np
import pygame

class MainWindow(QMainWindow, Ui_MainWindow):	
	def __init__(self, parent = None):
		pygame.init()
		# Define variables
		txtList = np.genfromtxt('largeSet.txt',dtype='str',delimiter='\n')
		ansList = np.genfromtxt('largeAnsSet.txt',dtype='int',delimiter='\n')
		# Creates the list of words with corresponding answer keys
		self.allList = np.vstack((txtList,ansList)).T
		np.random.shuffle(self.allList)
		self.counter = 0 # Defines the counter to go over list of phrases and answers
		self.response = np.nan # Keeps track of the response
		self.trialNum = 0 # Keeps track of the trial number
		self.interact = 0 # Keeps track of the number of interactions

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
		# Button "START" on click
		QtCore.QObject.connect(self.btnStart, QtCore.SIGNAL("clicked()"), self.showGameFrame)

	''' HIGHLIGHTING BUTTONS '''
	# This modifies the highligh sequence of the labels
	def Uphighlight(self):
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:white;background-color:blue;text-align:left;}")
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		self.response = self.counter
		# Increase counter for interactions with screen
		self.interact += 1
	def Downhighlight(self):
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:white;background-color:blue;text-align:left;}")
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		tmp = self.counter
		self.response = tmp+1
		# Increase counter for interactions with screen
		self.interact += 1

	''' UP/DOWN BUTTONS '''
	# Functions for moving up or down in the text file
	def moveUp(self):
		if self.counter == 0:
			self.counter = 0
		else:
			self.counter = self.counter - 1
		# Modifying labels from buttons
		self.response = np.nan
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		# Setting up labels
		counter = self.counter
		self.btnLabelUp.setText(QtGui.QApplication.translate("MainWindow",self.allList[counter,0] , None, QtGui.QApplication.UnicodeUTF8))
		self.btnLabelDown.setText(QtGui.QApplication.translate("MainWindow",self.allList[counter+1,0] , None, QtGui.QApplication.UnicodeUTF8))
		# Increase counter for interactions with screen
		self.interact += 1

	def moveDown(self):
		if self.counter == len(self.allList)-2:
			self.counter = len(self.allList)-2
		else:
			self.counter = self.counter + 1
		# Modifying labels from buttons
		self.response = np.nan
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		# Setting up labels
		counter = self.counter
		self.btnLabelUp.setText(QtGui.QApplication.translate("MainWindow",self.allList[counter,0] , None, QtGui.QApplication.UnicodeUTF8))
		self.btnLabelDown.setText(QtGui.QApplication.translate("MainWindow",self.allList[counter+1,0] , None, QtGui.QApplication.UnicodeUTF8))
		# Increase counter for interactions with screen
		self.interact += 1

	''' SHOW/HIDE FRAMES '''
	# Showing all required frames
	def showReadyFrame(self):
		self.parID = self.editParticipantID.text()
		with open('%s.csv'%self.parID,'wb') as csvfile:
			toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
			toFile.writerow(['Trial#','Phrase Selected','isCorrect','Interactions'])
		self.introframe.hide()
		self.feedbackframe.hide()
		self.gameframe.hide()
		self.readyframe.show()
		# Wait for 2 seconds before calling the game screen
		#timer = QtCore.QTimer()
		#timer.singleShot(2000, self.showGameFrame)

	def showGameFrame(self):
		# Set up the initial words
		counter = self.counter
		self.btnLabelUp.setText(QtGui.QApplication.translate("MainWindow",self.allList[counter,0] , None, QtGui.QApplication.UnicodeUTF8))
		self.btnLabelDown.setText(QtGui.QApplication.translate("MainWindow",self.allList[counter+1,0] , None, QtGui.QApplication.UnicodeUTF8))
		self.response = np.nan
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		self.introframe.hide()
		self.readyframe.hide()
		self.feedbackframe.hide()
		self.gameframe.show()
		self.trialNum += 1

	def submitFun(self):
		if np.isnan(self.response):
			self.interact += 1 # Increase counter for interactions with screen
		if not np.isnan(self.response):
			# Incorrect response - Keeps on playing the game
			if int(self.allList[self.response,1]) == 0:
				pygame.mixer.Sound('boo.wav').play()
				self.lblFeedback.setText(QtGui.QApplication.translate("MainWindow", "Incorrect", None, QtGui.QApplication.UnicodeUTF8))
				self.gameframe.hide()
				self.feedbackframe.show()
				self.interact += 1 # Increase counter for interactions with screen
				timer = QtCore.QTimer()
				timer.singleShot(1000, self.showGameFrame)
				
			# Correct response - Goes back to "Task Is Ready" Screen
			if int(self.allList[self.response,1]) == 1:
				pygame.mixer.Sound('cheer.wav').play()
				self.lblFeedback.setText(QtGui.QApplication.translate("MainWindow", "Correct", None, QtGui.QApplication.UnicodeUTF8))
				self.gameframe.hide()
				self.feedbackframe.show()
				self.interact += 1 # Increase counter for interactions with screen
				timer = QtCore.QTimer()
				timer.singleShot(1000, self.showReadyFrame)

			# Writing results to file
			with open('%s.csv'%self.parID,'ab') as csvfile:
				toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
				toFile.writerow(['%d'%self.trialNum,'%s'%self.allList[self.response,0],'%s'%self.allList[self.response,1],'%d'%self.interact])

		# Randomizing next trial
		np.random.shuffle(self.allList)
		self.counter = 0 # Resets counter for answers
		self.interact = 0 # Resets counter for interactions with screen


		
if __name__=='__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()
	app.exec_()
