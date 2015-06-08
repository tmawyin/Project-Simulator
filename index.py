import sys
import os
from PySide import QtCore, QtGui, QtOpenGL
from PySide.QtGui import QMainWindow, QPushButton, QApplication, QDesktopWidget
from mainwindow import Ui_MainWindow
from graph import Graph
import csv
import numpy as np
''' SIMULATOR '''
from NetClient import *
from Receiver import *


class MainWindow(QMainWindow, Ui_MainWindow):	
	parID_signal = QtCore.Signal(str)
	quitNetclient = QtCore.Signal()

	def __init__(self, parent = None):
		# Initialize the constructor
		super(MainWindow, self).__init__(parent)

		# Removes glances file - not needed
		if os.path.exists('GlancesNetclient.csv'):
			os.remove("GlancesNetclient.csv")

		# Define variables
		# Change to True to recreate post-drive screen
		self.summary = False

		self.initAll = False
		self.endDrive = False
		txtList = np.genfromtxt('largeSet.txt',dtype='str',delimiter='\n')
		ansList = np.genfromtxt('largeAnsSet.txt',dtype='int',delimiter='\n')
		# Creates the list of words with corresponding answer keys
		self.responseList = np.vstack((txtList,ansList)).T
		rnd = np.random.randint(0,self.responseList.shape[0]/10)
		self.allList = self.responseList[rnd*10:rnd*10+10,:]
		
		self.counter = 0 # Defines the counter to go over list of phrases and answers
		self.response = np.nan # Keeps track of the response
		self.trialNum = 0 # Keeps track of the trial number
		self.interact = 0 # Keeps track of the number of interactions

		# Set up the GUI
		self.setupUi(self)

		# Show the application in fullscreen
		self.showFullScreen()
		
		# Setting the frames to be full screen
		desktop = QDesktopWidget()
		width = desktop.geometry().width()
		height = desktop.geometry().height()

		# Create the graph object
		self.graph = Graph(width, height)

		# Hide all the frames except the initial
		self.introframe.show()
		self.readyframe.hide()
		self.feedbackframe.hide()
		self.gameframe.hide()
		self.endframe.hide()

		# Position and resize the frames.
		self.introframe.move(0,0)
		self.introframe.resize(width, height)
		self.readyframe.move(0,0)		
		self.readyframe.resize(width, height)
		self.feedbackframe.move(0,0)
		self.feedbackframe.resize(width, height)
		self.gameframe.move(0,0)
		self.gameframe.resize(width, height)
		self.endframe.move(0,0)
		self.endframe.resize(width, height)

		''' BUTTONS '''
		# Button "DONE" on click
		QtCore.QObject.connect(self.btnDone, QtCore.SIGNAL("clicked()"), self.showReadyFrame)
		# Moving UP/DOWN buttons
		QtCore.QObject.connect(self.btnUp, QtCore.SIGNAL("clicked()"), self.moveUp)
		QtCore.QObject.connect(self.btnDown, QtCore.SIGNAL("clicked()"), self.moveDown)
		self.btnUp.setEnabled(False)
		self.btnUp.setStyleSheet("QPushButton{background-color:#B0B0B0;}")
		# Selecting buttons
		QtCore.QObject.connect(self.btnLabelUp, QtCore.SIGNAL("clicked()"), self.Uphighlight)
		QtCore.QObject.connect(self.btnLabelDown, QtCore.SIGNAL("clicked()"), self.Downhighlight)
		# Button "SUBMIT" on click
		QtCore.QObject.connect(self.btnSubmit, QtCore.SIGNAL("clicked()"), self.submitFun)
		# Button "START" on click
		QtCore.QObject.connect(self.btnStart, QtCore.SIGNAL("clicked()"), self.showGameFrame)
		# Button "END" on click
		QtCore.QObject.connect(self.goButton, QtCore.SIGNAL("clicked()"), self.showPostDrive)

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
			self.counter = self.counter - 2
			if self.counter == 0:
				self.btnUp.setEnabled(False)
				self.btnUp.setStyleSheet("QPushButton{background-color:#B0B0B0;}")
		self.btnDown.setEnabled(True)
		self.btnDown.setStyleSheet("QPushButton{background-color:"";}")
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
			self.counter = self.counter + 2
			if self.counter == len(self.allList)-2:
				self.btnDown.setEnabled(False)
				self.btnDown.setStyleSheet("QPushButton{background-color:#B0B0B0;}")
		self.btnUp.setEnabled(True)
		self.btnUp.setStyleSheet("QPushButton{background-color:"";}")
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
		self.fileName= self.parID.split("_")[0]+"_"+self.parID.split("_")[1]
		''' SIMULATOR '''
		if self.initAll == False and self.summary == False:
			# Initializing the NetClient
			self.netclient = NetClient(self.quitNetclient)
			self.netclient.glanceWarningSignal.connect(self.setGlanceWarning, QtCore.Qt.QueuedConnection)
			self.netclient.glanceDangerSignal.connect(self.setGlanceDanger, QtCore.Qt.QueuedConnection)
			self.netclient.glanceResetSignal.connect(self.resetGlance, QtCore.Qt.QueuedConnection)
			self.netclient.start()
			# Initializing the RECEIVER
			self.receiver = Receiver(self.netclient,self.parID_signal)
			self.receiver.terminateScreen.connect(self.showEndDrive, QtCore.Qt.QueuedConnection)
			self.receiver.start()
			self.parID_signal.emit(self.fileName)
			self.initAll = True
		
		# GUI part
		self.introframe.hide()
		self.feedbackframe.hide()
		self.gameframe.hide()
		self.endframe.hide()
		self.readyframe.show()
		self.resetGlance()
		
		# Only create the file if it does not exist
		if not os.path.exists('../../participantData/Gamification/%s.csv'%self.fileName):
			with open('../../participantData/Gamification/%s.csv'%self.fileName,'wb') as csvfile:
				toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
				toFile.writerow(['Trial#','Phrase Selected','isCorrect','Interactions'])


	def showGameFrame(self):
		self.btnUp.setStyleSheet("QPushButton{background-color:#B0B0B0;}")
		self.btnDown.setStyleSheet("QPushButton{background-color:"";}")
		self.btnUp.setEnabled(False)
		self.btnDown.setEnabled(True)
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
		self.endframe.hide()
		self.gameframe.show()
		self.trialNum += 1
		self.interact += 1
		self.resetGlance()

	def submitFun(self):
		if self.endDrive == True:
			self.showEndDrive()
		else:
			if np.isnan(self.response):
				self.interact += 1 # Increase counter for interactions with screen
			if not np.isnan(self.response):
				# Incorrect response - Keeps on playing the game
				if int(self.allList[self.response,1]) == 0:
					self.lblFeedback.setText(QtGui.QApplication.translate("MainWindow", "Incorrect", None, QtGui.QApplication.UnicodeUTF8))
					self.gameframe.hide()
					self.feedbackframe.show()
					self.interact += 1 # Increase counter for interactions with screen
					timer = QtCore.QTimer()
					correctVal = False
					if self.summary == False:
						timer.singleShot(1000, self.showGameFrame)
					else:
						timer.singleShot(1000, self.showEndDrive)
					
				# Correct response - Goes back to "Task Is Ready" Screen
				if int(self.allList[self.response,1]) == 1:
					self.lblFeedback.setText(QtGui.QApplication.translate("MainWindow", "Correct", None, QtGui.QApplication.UnicodeUTF8))
					self.gameframe.hide()
					self.feedbackframe.show()
					self.interact += 1 # Increase counter for interactions with screen
					timer = QtCore.QTimer()
					correctVal = True
					timer.singleShot(1000, self.showReadyFrame)

				# Writing results to file
				with open('../../participantData/Gamification/%s.csv'%self.fileName,'ab') as csvfile:
					toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
					toFile.writerow(['%d'%self.trialNum,'%s'%self.allList[self.response,0],'%s'%self.allList[self.response,1],'%d'%self.interact])

				# Randomizing the next trial if correct
				if correctVal == True:
					rnd = np.random.randint(0,self.responseList.shape[0]/10)
					self.allList = self.responseList[rnd*10:rnd*10+10,:]
					correctVal = False

			self.counter = 0 # Resets counter for answers
			self.interact = 0 # Resets counter for interactions with screen
		
	def showEndDrive(self):
		self.label_loading.setStyleSheet("QLabel{background-color:white; color:white;}")
		self.endDrive = True
		self.introframe.hide()
		self.readyframe.hide()
		self.feedbackframe.hide()
		self.gameframe.hide()
		self.endframe.show()
		with open('../../participantData/Gamification/%s.csv'%self.fileName,'ab') as csvfile:
			toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
			toFile.writerow(['%d'%self.interact])
		''' SIMULATOR '''
		if self.summary == False:
			self.quitNetclient.emit()
			self.netclient.glanceWarningSignal.disconnect(self.setGlanceWarning)
			self.netclient.glanceDangerSignal.disconnect(self.setGlanceDanger)
			self.netclient.glanceResetSignal.disconnect(self.resetGlance)
			self.netclient.exit(0)
			self.receiver.exit(0)

	def setGlanceWarning(self):
		# Change the style of the glance
		self.lblGlance.setStyleSheet("background-color:#f0ad4e; margin:0px 250px; padding-bottom:30px;")
		self.lblGlance_2.setStyleSheet("background-color:#f0ad4e; margin:0px 250px; padding-bottom:30px;")
		# self.lblGlance_2.setStyleSheet("background-color:#f0ad4e; margin:0px 350px; padding-bottom:30px; max-height: 64px;")
		
	def setGlanceDanger(self):
		# Change the style of the glance
		self.lblGlance.setStyleSheet("background-color:#d9534f; margin:0px; padding-bottom:30px;")
		self.lblGlance_2.setStyleSheet("background-color:#d9534f; margin:0px; padding-bottom:30px;")
		# self.lblGlance_2.setStyleSheet("background-color:#d9534f; margin:0px 100px; padding-bottom:30px; max-height: 64px;")
		
	def resetGlance(self):
		# Change the style of the glance
		self.lblGlance.setStyleSheet("background-color:white; margin:0px; padding-bottom:30px;");
		self.lblGlance_2.setStyleSheet("background-color:white; margin:0px; padding-bottom:30px;");

	def showPostDrive(self):
		self.goButton.setEnabled(False)
		self.label_loading.setStyleSheet("QLabel{background-color:""; color:"";}")
		timer = QtCore.QTimer()
		timer.singleShot(50,self.endGraph)

	def endGraph(self):
		self.graph.createGraph(self.parID,18,32)
		self.setCentralWidget(self.graph)
		
				
if __name__=='__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()
	app.exec_()
	
	
