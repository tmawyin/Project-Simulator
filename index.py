import sys

from PySide import QtCore, QtGui, QtOpenGL
from PySide.QtGui import QMainWindow, QPushButton, QApplication, QDesktopWidget
from mainwindow import Ui_MainWindow
from graph import Graph
# from OpenGL import *
import csv
import numpy as np
import pygame
from NetClient import *
from Receiver import *


class MainWindow(QMainWindow, Ui_MainWindow):	

	def __init__(self, parent = None):
		pygame.init()
		# Initializing the NetClient
		self.netclient = NetClient()
		self.netclient.glanceWarningSignal.connect(self.setGlanceWarning, QtCore.Qt.QueuedConnection)
		self.netclient.glanceDangerSignal.connect(self.setGlanceDanger, QtCore.Qt.QueuedConnection)
		self.netclient.glanceResetSignal.connect(self.resetGlance, QtCore.Qt.QueuedConnection)
		self.netclient.start()

		# Initializing the RECEIVER
		self.receiver = Receiver(self.netclient)
		self.receiver.start()

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

		# Show the application in fullscreen
		self.showFullScreen()
		
		# Setting the frames to be full screen
		desktop = QDesktopWidget()
		width = desktop.geometry().width()
		height = desktop.geometry().height()
		
		# Create the graph object
		##self.graph = Graph(width, height)
		##self.setCentralWidget(self.graph)
		# self.graph = Graph(width, height)		
		# self.graph.createGrid(8, 14)
		# self.graph.grid[7][0] = 3
		# self.graph.grid[6][0] = 2
		# self.graph.grid[5][0] = 2
		# self.graph.grid[4][0] = 2
		# self.graph.grid[3][0] = 1
		# self.graph.grid[7][1] = 3
		# self.graph.grid[6][1] = 3
		# self.graph.grid[5][1] = 1
		# self.graph.grid[4][1] = 1
		# self.graph.grid[7][2] = 3
		# self.graph.grid[6][2] = 3
		# self.graph.grid[5][2] = 2
		# self.graph.grid[4][2] = 2
		# self.graph.grid[3][2] = 2
		# self.graph.grid[2][2] = 1
		# self.graph.grid[7][3] = 3
		# self.graph.grid[6][3] = 3
		# self.graph.grid[5][3] = 3
		# self.graph.grid[4][3] = 3
		# self.graph.grid[7][4] = 3
		# self.graph.grid[6][4] = 3
		# self.graph.grid[5][4] = 2
		# self.graph.grid[4][4] = 1
		# self.graph.grid[7][5] = 3
		# self.graph.grid[6][5] = 3
		# self.graph.grid[5][5] = 2
		# self.graph.grid[4][5] = 2
		# self.graph.grid[3][5] = 1
		# self.graph.grid[7][6] = 3
		# self.graph.grid[6][6] = 2
		# self.graph.grid[5][6] = 2
		# self.graph.grid[4][6] = 1
		# self.graph.grid[7][7] = 2
		# self.graph.grid[6][7] = 1
		# self.graph.grid[5][7] = 1
		# self.graph.grid[4][7] = 1
		# self.graph.grid[7][8] = 3
		# self.graph.grid[6][8] = 2
		# self.graph.grid[5][8] = 1
		# self.graph.grid[7][9] = 3
		# self.graph.grid[6][9] = 1
		# self.graph.grid[7][10] = 2
		# self.graph.grid[6][10] = 2
		# self.graph.grid[5][10] = 1
		# self.graph.grid[7][11] = 1
		# self.graph.grid[6][11] = 1
		# self.graph.grid[5][11] = 1
		# self.graph.grid[7][12] = 2
		# self.graph.grid[6][12] = 1
		# self.graph.grid[7][13] = 1		
		# self.setCentralWidget(self.graph)

		# Hide all the frames except the initial
		self.introframe.show()
		self.readyframe.hide()
		self.feedbackframe.hide()
		self.gameframe.hide()	

		# Position and resize the frames.
		self.introframe.move(0,0)
		self.introframe.resize(width, height)
		self.readyframe.move(0,0)		
		self.readyframe.resize(width, height)
		self.feedbackframe.move(0,0)
		self.feedbackframe.resize(width, height)
		self.gameframe.move(0,0)
		self.gameframe.resize(width, height)
		
		#self.setGlanceWarning()
		#self.setGlanceDanger()

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
		#self.setCentralWidget(self.graph)

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
		self.resetGlance()

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
		
	def setGlanceWarning(self):
		# Change the style of the glance
		self.lblGlance.setStyleSheet("background-color:#f0ad4e; margin:0px 250px; padding-bottom:30px;")
		
	def setGlanceDanger(self):
		# Change the style of the glance
		self.lblGlance.setStyleSheet("background-color:#d9534f; margin:0px; padding-bottom:30px;")
		
	def resetGlance(self):
		# Change the style of the glance
		self.lblGlance.setStyleSheet("");
		
if __name__=='__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()
	app.exec_()
	
	
