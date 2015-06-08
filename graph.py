from PySide import QtCore, QtGui, QtOpenGL
import os
import numpy as np
import csv
import OpenGL.GL as gl
import math
from Printer import Printer
from Button import Button
from BadgeScreen import BadgeScreen

class Graph(QtOpenGL.QGLWidget):
	'''
	***********************************************************
	The options for the screen showing
	***********************************************************
	'''
	GRAPH_ONE = 0
	GRAPH_TWO = 1
	BADGE_SCREEN = 2

	def __init__(self, width, height):
		# Base constructor
		QtOpenGL.QGLWidget.__init__(self)		
		self.setMouseTracking(True)
		
		# Load the printer
		self.printer = Printer()
		
		# Load the other OpenGL screens
		'''
		***********************************************************
		New Class
		***********************************************************
		'''
		self.badgeScreen = BadgeScreen(width, height, self.printer)
		
		# Set the attributes
		self.showing = 2
		self.width = width
		self.height = height
		self.rectSize = 33.5
		# self.rectSize = 28.00
		self.gridCols = 0
		self.gridRows = 0
		self.grid = None
		
		# Create the buttons
		self.btnGraph1 = Button(u"\u25c4", 10, 15, 100, 50)
		self.btnGraph2 = Button(u"\u25ba", self.width - 110, 15, 100, 50)
		self.btnGraph3 = Button(u"\u25ba", self.width - 110, 15, 100, 50)
		self.btnGraph4 = Button(u"\u25c4", 10, 15, 100, 50)
		self.btnGraph1.disable()
		self.btnGraph3.disable()
		self.btnGraph4.disable()
		
		# The labels
		self.ube = 0
		self.ld = 0
		self.high = 0
		self.medium = 0
		self.low = 0
		self.timeEvent =[]
		
		# Calculate the proportions
		self.heightFivePercent = self.height * 0.05
		self.graphPadding = 5;
		self.rectPadding = 2;
		self.titleHeight = self.height * 0.1
		self.graphX = self.width * 0.02
		self.graphY = self.titleHeight * 2
		self.graphWidth = self.width * 0.60
		self.graphHeight = self.height * 0.7
		self.dsmX = self.width * 0.64
		self.dsmY = self.height * 0.5
		self.dsmWidth = self.width * 0.35
		self.dsmHeight = self.height * 0.4
		self.lowRiskX = self.dsmX
		self.lowRiskY = self.graphY
		self.mediumRiskX = self.dsmX
		self.mediumRiskY = self.graphY + self.rectSize + 30
		self.highRiskX = self.dsmX
		self.highRiskY = self.graphY + (self.rectSize * 2) + 60
		
		self.pastNumbers = [22, 16, 52]
		self.currentNumbers = [12, 18, 30]
		
		# self.pastNumbersSum = self.pastNumbers[0] + self.pastNumbers[1] + self.pastNumbers[2]
		# self.currentNumbersSum = self.currentNumbers[0] + self.currentNumbers[1] + self.currentNumbers[2]
		# self.glancesGridMaxNum = self.pastNumbersSum if self.pastNumbersSum > self.currentNumbersSum else self.currentNumbersSum
		# self.glancesGridMaxNum = self.glancesGridMaxNum + 10
		self.graph2HorPadding = 100
		self.glancesGridPadding = 50
		self.glancesGridTitleX = self.graph2HorPadding
		self.glancesGridTitleY = self.titleHeight + 10
		self.glancesGridTitleWidth = (self.width - (self.graph2HorPadding * 3)) * 0.5
		self.glancesGridTitleHeight = 70
		self.glancesGridX = self.graph2HorPadding + 30
		self.glancesGridY = self.glancesGridTitleY + self.glancesGridTitleHeight
		self.glancesGridWidth = self.glancesGridTitleWidth
		self.glancesGridHeight = (self.height - self.glancesGridY) - 70
		self.glancesGridBarPaddingTop = 20
		self.glancesGridBarWidth = (self.glancesGridWidth - (self.glancesGridPadding * 3)) / 2
		self.glancesGridBarHeight = self.glancesGridHeight - self.glancesGridBarPaddingTop
		self.tripsTitleX = (self.graph2HorPadding*2) + self.glancesGridWidth
		self.tripsTitleY = self.glancesGridTitleY
		self.tripsTitleWidth = self.glancesGridTitleWidth
		self.tripsTitleHeight = self.glancesGridTitleHeight
		self.glanceNumTitleX = self.tripsTitleX
		self.glanceNumTitleY = self.tripsTitleY + self.tripsTitleHeight + 10
		self.glanceNumTitleWidth = self.tripsTitleWidth
		self.glanceNumTitleHeight = self.tripsTitleHeight
		self.glanceNumPadding = 75 #53
		self.glanceNumRadius = 18
		self.glanceNumPaddingVer = 40
		self.highIconX = self.glanceNumTitleX + self.glanceNumRadius + 90
		self.highIconY = self.glanceNumTitleY + self.glanceNumTitleHeight + 50
		self.highPastTitleX = self.glanceNumTitleX + (self.glanceNumPadding * 4) + self.glanceNumRadius
		self.highPastTitleY = self.highIconY - self.glanceNumRadius
		self.highCurrentTitleX = self.glanceNumTitleX + (self.glanceNumPadding * 7) + self.glanceNumRadius
		self.highCurrentTitleY = self.highPastTitleY
		self.mediumIconX = self.highIconX
		self.mediumIconY = self.highIconY + self.glanceNumRadius + self.glanceNumPaddingVer
		self.mediumPastTitleX = self.highPastTitleX
		self.mediumPastTitleY = self.highPastTitleY + self.glanceNumRadius + self.glanceNumPaddingVer
		self.mediumCurrentTitleX = self.highCurrentTitleX
		self.mediumCurrentTitleY = self.mediumPastTitleY
		self.lowIconX = self.highIconX
		self.lowIconY = self.mediumIconY + self.glanceNumRadius + self.glanceNumPaddingVer
		self.lowPastTitleX = self.mediumPastTitleX
		self.lowPastTitleY = self.mediumPastTitleY + self.glanceNumRadius + self.glanceNumPaddingVer
		self.lowCurrentTitleX = self.highCurrentTitleX
		self.lowCurrentTitleY = self.lowPastTitleY
		self.totalTitleX = self.glanceNumTitleX + 70
		self.totalTitleY = self.lowIconY + 40
		self.totalPastTitleX = self.mediumPastTitleX
		self.totalPastTitleY = self.totalTitleY
		self.totalCurrentTitleX = self.mediumCurrentTitleX
		self.totalCurrentTitleY = self.totalTitleY
		self.safetyMetricsTitleX = self.glanceNumTitleX
		self.safetyMetricsTitleY = self.glanceNumTitleY + 450 #330
		self.safetyMetricsTitleWidth = self.glanceNumTitleWidth
		self.safetyMetricsTitleHeight = self.glanceNumTitleHeight
		self.safeEventTitleX = self.safetyMetricsTitleX + 30
		self.safeEventTitleY = self.safetyMetricsTitleY + self.safetyMetricsTitleHeight + 10
		self.safeEventPastNumTitleX = self.mediumPastTitleX
		self.safeEventPastNumTitleY = self.safeEventTitleY
		self.safeEventCurrentNumTitleX = self.mediumCurrentTitleX
		self.safeEventCurrentNumTitleY = self.safeEventTitleY
		self.unsafeEventTitleX = self.safeEventTitleX
		self.unsafeEventTitleY = self.safeEventTitleY + 50
		self.unsafeEventPastNumTitleX = self.mediumPastTitleX
		self.unsafeEventPastNumTitleY = self.unsafeEventTitleY
		self.unsafeEventCurrentNumTitleX = self.mediumCurrentTitleX
		self.unsafeEventCurrentNumTitleY = self.unsafeEventTitleY
		self.deviationsEventTitleX = self.safeEventTitleX
		self.deviationsEventTitleY = self.unsafeEventTitleY + 50
		self.deviationsEventPastNumTitleX = self.mediumPastTitleX
		self.deviationsEventPastNumTitleY = self.deviationsEventTitleY
		self.deviationsEventCurrentNumTitleX = self.mediumCurrentTitleX
		self.deviationsEventCurrentNumTitleY = self.deviationsEventTitleY
		
	def initializeGL(self):
		# Initialize the context
		gl.glClearColor(1.0, 1.0, 1.0, 1)
		gl.glEnable(gl.GL_LINE_STIPPLE)
		#glEnable (GL_BLEND);
		#glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
		
		'''
		***********************************************************
		Enable textures
		***********************************************************
		'''
		gl.glEnable(gl.GL_TEXTURE_2D)
		self.badgeScreen.init(self.parID,self.gender)
		
		# Use the fixed pipeline
		# Resize the window
		self.resizeGL(self.width, self.height)
		
	def resizeGL(self, width, height):
		# Update the attributes
		self.width = width
		self.height = height
		
		# Set up the viewport
		gl.glViewport(0, 0, width, height)
		
		# Set up an orthographic view
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glLoadIdentity()
		gl.glOrtho(0, self.width, self.height, 0, -1, 1)
		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()
		
	def mouseMoveEvent(self, event):
		self.btnGraph1.update(event.x(), event.y())
		self.btnGraph2.update(event.x(), event.y())
		self.btnGraph3.update(event.x(), event.y())
		self.btnGraph4.update(event.x(), event.y())

		self.repaint()
		
	def mousePressEvent(self, event):
		if self.btnGraph4.isMouseOver() == True:
			self.showing = self.GRAPH_ONE
			self.btnGraph1.enable()
			self.btnGraph2.disable()
			self.btnGraph3.enable()
			self.btnGraph4.disable()
			self.repaint()
	
		if self.btnGraph3.isMouseOver() == True:
			self.showing = self.GRAPH_TWO
			self.btnGraph1.disable()
			self.btnGraph2.disable()
			self.btnGraph3.disable()
			self.btnGraph4.enable()
			self.repaint()
	
		if self.btnGraph2.isMouseOver() == True:
			self.showing = self.GRAPH_ONE
			self.btnGraph1.enable()
			self.btnGraph2.disable()
			if self.enableButton == True:
				self.btnGraph3.enable()
			else:
				self.btnGraph3.disable()
			self.btnGraph4.disable()
			self.repaint()
		
		if self.btnGraph1.isMouseOver() == True:
			self.showing = self.BADGE_SCREEN
			self.btnGraph1.disable()
			self.btnGraph2.enable()
			self.btnGraph3.disable()
			self.btnGraph4.disable()
			self.repaint()
		
	def createGraph(self, parID, rows, cols):
		self.parID = parID.split("_")[0]+"_"+parID.split("_")[1]
		self.gridRows = rows
		self.gridCols = cols
		self.grid = [[0 for x in range(cols)] for x in range(rows)]
		self.ube = 0
		self.ld = 0
		self.high = 0
		self.medium = 0
		self.low = 0
		
		numRows = 900

		# Variables: Counters to keep track of values
		listValues = []
		gridValues = []
		lowCount = 0
		warnCount = 0
		dangerCount = 0
		unsafEvent = 0
		bbTime = 0			# <1.2s
		timeCollision = 0	# <1.5s
		laneDepart = 0		# <-5
		numCollision = 0	# >1
		accelCount = 0		# < -19.3 ft/s**2
		lineCount = 0
		timeUBE = []		# keeps track of where unsafe breaking events
		timeLOG = []		# keeps track of where log events happen
		logEvent = []		# keeps track of where log events and unsave event happen
		ldEvent = []
		isLaneDepart = False
		isAccel = False
		isCollisiton = False

		receiverData = np.genfromtxt('../../participantData/Gamification/%s_data.csv'%self.parID, delimiter=',')
		netclientData = np.genfromtxt('../../participantData/Gamification/%s_net.csv'%self.parID, delimiter=',')

		# Reading Receiver Data
		for i in range(len(receiverData)):
			# Counting for Number of Collisions
			if float(receiverData[i,2]) > 1:
				numCollision += 1
			# Counting for Lane Deviation
			if float(receiverData[i,4]) < -2.7 or float(receiverData[i,4]) > 5.0:
				isLaneDepart = True
			if isLaneDepart == True and (float(receiverData[i,4]) >= -2.7 and float(receiverData[i,4]) <= 5.0):
				isLaneDepart = False
				laneDepart += 1
				ldEvent.append(receiverData[i,0])

		# # Code to include the acceleration based on the LogStream
		for k in range(int(np.max(receiverData[:,1])+1)):
			a = receiverData[receiverData[:,1]==k]
			a = a[0:900,:]
			if k != 0:
				timeLOG.append(a[0,0]) 
			for l in range(len(a)):
				# Counting for Acceleration
				if float(a[l,10]) < -19.3 or (float(a[l,8]) <1.5 and float(a[l,8]) !=0):
					timeUBE.append(a[l,0])
					logEvent.append(int(a[l,1]))
					unsafEvent += 1
					break
		# timeLOG.append(receiverData[len(receiverData)-1,0])

		self.ube = unsafEvent
		self.ld += laneDepart

		# This will take when the log stream happens
		self.timeEvent = (timeLOG-receiverData[0,0])/(receiverData[len(receiverData)-1,0] - receiverData[0,0])
		self.logStreamEvent = logEvent
		self.deviationEvent = (ldEvent-receiverData[0,0])/(receiverData[len(receiverData)-1,0] - receiverData[0,0])

		# Reading Netclient Data
		for j in range(len(netclientData)):
			lineCount += 1
			# Counting for Warning, Danger, and Low Glances
			if float(netclientData[j,5]) == 1:
				warnCount += 1
			if float(netclientData[j,6]) == 1:
				dangerCount += 1
			if float(netclientData[j,8]) == 1:
				lowCount += 1

			if lineCount == numRows or j == range(len(netclientData))[-1]:
				column = [3 for x in range(dangerCount)] + [2 for x in range(warnCount)] + [1 for x in range(lowCount)]
				if len(column) > self.gridRows:
					column = column[0:self.gridRows]
				elif len(column) < self.gridRows:
					column = column + [0 for x in range(self.gridRows-len(column))]
				gridValues.append(column)

				self.high += dangerCount
				self.medium += warnCount
				self.low += lowCount
				
				# Reset all variables
				lineCount = 0
				lowCount = 0
				warnCount = 0 
				dangerCount = 0
		
		self.grid = np.zeros((self.gridRows, self.gridCols))
		minLength = len(gridValues) if self.gridCols > len(gridValues) else self.gridCols
		for i in range(minLength):
			gridValues[i].reverse()
			self.grid[:,i] = np.array(gridValues[i])

		# Saving drives to a file
		driver = parID.split("_")
		if os.path.exists('../../participantData/Gamification/%s_drives.csv'%driver[0]):
			driverData = np.genfromtxt('../../participantData/Gamification/%s_drives.csv'%driver[0], delimiter=',')
			if len(driverData.shape) == 1:
				if str(driver[2]) == "m" or str(driver[2]) == "M":
					self.gender = 0
				else:
					self.gender = 1
			# 
			else:
				self.gender = driverData[1,-1]
		
		with open('../../participantData/Gamification/%s_drives.csv'%driver[0],'ab') as csvfile:
			toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
			toFile.writerow(['%d'%self.high,'%d'%self.medium,'%d'%self.low,'%d'%self.ld,'%s'%self.ube,'%d'%(8-self.ube),'%d'%self.gender])

		# Using file to determine comparison screen
		driverData = np.genfromtxt('../../participantData/Gamification/%s_drives.csv'%driver[0], delimiter=',')
		if len(driverData.shape) == 1:
			self.enableButton = False
			driverData = np.array([driverData])
		else:
			self.enableButton = True
			self.pastNumbers = map(int,driverData[-2,0:3].tolist())
			self.currentNumbers = map(int,driverData[-1,0:3].tolist())
			self.compLane = map(int,driverData[-2:,3].tolist())
			self.compUnsafe = map(int,driverData[-2:,4].tolist())
			self.compSafe = map(int,driverData[-2:,5].tolist())
			self.pastNumbersSum = self.pastNumbers[0] + self.pastNumbers[1] + self.pastNumbers[2]
			self.currentNumbersSum = self.currentNumbers[0] + self.currentNumbers[1] + self.currentNumbers[2]
			self.glancesGridMaxNum = self.pastNumbersSum if self.pastNumbersSum > self.currentNumbersSum else self.currentNumbersSum
			self.glancesGridMaxNum = int(math.ceil(self.glancesGridMaxNum/10.0) * 10)
	
	def paintLine(self, x1, y1, x2, y2, width, red = 0, green = 0, blue = 0):
		gl.glColor3f(red, green, blue)	
		gl.glBegin(gl.GL_QUADS)
		gl.glVertex2f(x1, y1)#+70
		gl.glVertex2f(x1 + width+2, y1)
		gl.glVertex2f(x2 + width+2, y2-10)
		gl.glVertex2f(x2, y2-10)
		gl.glEnd()
		
	'''
	***********************************************************
	New Function
	***********************************************************
	'''
	def paintLineHorizontal(self, x1, y1, x2, y2, width = 1, red = 0, green = 0, blue = 0):
		top = math.ceil(width/2.0)
		bottom = math.floor(width/2.0)
		
		gl.glColor3f(red, green, blue)
		gl.glBegin(gl.GL_QUADS)
		gl.glVertex2f(x1, y1 - top)
		gl.glVertex2f(x2, y2 - top)
		gl.glVertex2f(x2, y2 + bottom)
		gl.glVertex2f(x1, y1 + bottom)
		gl.glEnd();
	
	def paintRect(self, x, y, red, green, blue):
		# Draw the background of the rectangle
		gl.glColor3f(red, green, blue)
		gl.glBegin(gl.GL_QUADS)
		gl.glVertex2f(x, y)
		gl.glVertex2f(x + self.rectSize, y)
		gl.glVertex2f(x + self.rectSize, y + self.rectSize)
		gl.glVertex2f(x, y + self.rectSize)
		gl.glEnd()
		
		# Revert the drawing mode
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
		
	def paintGrid(self):
		# Draw the border of the grid
		gl.glColor3f(0.9, 0.9, 0.9)
		gl.glLineWidth(2.0)
		# gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
		gl.glBegin(gl.GL_QUADS);
		gl.glVertex2f(self.graphX, self.graphY)
		gl.glVertex2f(self.graphX + self.graphWidth, self.graphY)
		gl.glVertex2f(self.graphX + self.graphWidth, self.graphY + self.graphHeight)
		gl.glVertex2f(self.graphX, self.graphY + self.graphHeight)
		gl.glEnd()
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
		
		moveX = self.graphWidth - (self.graphPadding * 2) - ((self.gridCols * self.rectSize) + (self.rectPadding * (self.gridCols)))
		moveY = self.graphHeight - (self.graphPadding * 2) - ((self.gridRows * self.rectSize) + (self.rectPadding * (self.gridRows)))
		
		# Draw the background lines
		numLines = int(self.gridRows/5)
		gl.glBegin(gl.GL_LINES)
		baseY = ((self.graphY + self.graphHeight) - self.graphPadding)
		fiveRects = (5 * self.rectSize) + (5 * self.rectPadding)
		for i in range(numLines):
			gl.glVertex2f(self.graphX, baseY - ((i+1) * fiveRects) - 1)
			gl.glVertex2f(self.graphX + self.graphWidth, baseY - ((i+1) * fiveRects) - 1)
		gl.glEnd()

		# Draw the event lines
		for i in range(len(self.timeEvent)):
			xposition = self.graphX + (self.timeEvent[i] * (((self.gridCols * self.rectSize) + (2 * self.graphPadding)) - ((self.gridCols + 1) * self.rectPadding)))
			if xposition < (self.graphX + self.graphWidth):
				if int(i+1) in self.logStreamEvent:
					self.paintLine(xposition, self.graphY, xposition, self.graphY + self.graphHeight, 2, 1.0, 0.0, 0.0) # Red
				else:
					self.paintLine(xposition, self.graphY, xposition, self.graphY + self.graphHeight, 2, 0.16, 0.76, 0.13) # Green

		# Drawing lane deviation lines
		for i in range(len(self.deviationEvent)):
			xposition = self.graphX + (self.deviationEvent[i] * (((self.gridCols * self.rectSize) + (2 * self.graphPadding)) - ((self.gridCols + 1) * self.rectPadding)))
			if xposition < (self.graphX + self.graphWidth):
				# self.paintLine(xposition, self.graphY, xposition, self.graphY + self.graphHeight, 2, 1.0, 0.6, 1.0)
				self.paintLine(xposition, self.graphY, xposition, self.graphY + self.graphHeight, 2, 0.0, 0.0, 0.0)  
		
		# Fill the grid
		gl.glLineWidth(2.0)
		for r, i in enumerate(self.grid):
			for c, v in enumerate(i):
				if v > 0:
					rectx = self.graphX + self.graphPadding + (self.rectPadding * c) + (c * self.rectSize)
					recty = self.graphY + self.graphPadding + moveY + (self.rectPadding * r) + (r * self.rectSize)
					if v == 1:
						self.paintRect(rectx, recty, 0.7, 0.7, 0.7)
					elif v == 2:
						self.paintRect(rectx, recty, 0.9412, 0.6784, 0.3059)
					elif v == 3:
						self.paintRect(rectx, recty, 0.851, 0.3255, 0.3099)

	def paintDSM(self):
		# Draw the border
		gl.glColor3f(0.9, 0.9, 0.9)
		gl.glLineWidth(2.0)
		# gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
		gl.glBegin(gl.GL_QUADS);
		gl.glVertex2f(self.dsmX, self.dsmY)
		gl.glVertex2f(self.dsmX + self.dsmWidth, self.dsmY)
		gl.glVertex2f(self.dsmX + self.dsmWidth, self.dsmY + self.dsmHeight)
		gl.glVertex2f(self.dsmX, self.dsmY + self.dsmHeight)
		gl.glEnd()
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

		# Adding legend
		self.paintLineHorizontal(self.dsmX + 5, self.dsmY + 100, self.dsmX + 50, self.dsmY + 100, 10, 0.16, 0.76, 0.13)
		self.paintLineHorizontal(self.dsmX + 5, self.dsmY + 230, self.dsmX + 50, self.dsmY + 230, 10, 1.00, 0.00, 0.00)
		self.paintLineHorizontal(self.dsmX + 5, self.dsmY + 350, self.dsmX + 50, self.dsmY + 350, 10, 0.00, 0.00, 0.00)
		
	def paintCircle(self, x, y, radius, red = 0, green = 0, blue = 0):
		gl.glColor3f(red, green, blue)
		gl.glBegin(gl.GL_POLYGON)
		for i in range(360):
			gl.glVertex2f(x + (radius * math.sin(math.radians(i))), y + (radius * math.cos(math.radians(i))))
		gl.glEnd()
		
	def paintEvent(self, event):
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		gl.glLoadIdentity();
		
		# Initialize the painter
		painter = QtGui.QPainter()
		painter.begin(self)
		
		'''
		***********************************************************
		Changed the if statement
		Bind the texture to nothing
		***********************************************************
		'''
		gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
		if self.showing == self.GRAPH_ONE:
			# Get the bounding rectangles
			tripEndBR = self.printer.getTextBox(painter, "Trip End", self.printer.fontNormal)
			
			# Draw OpenGL stuff
			self.paintGrid()
			self.paintDSM()
			
			self.paintRect(self.highRiskX, self.highRiskY, 0.851, 0.3255, 0.3099)
			self.paintRect(self.mediumRiskX, self.mediumRiskY, 0.9412, 0.6784, 0.3059)
			self.paintRect(self.lowRiskX, self.lowRiskY, 0.7, 0.7, 0.7)
			
			self.btnGraph1.drawBackground()
			self.btnGraph3.drawBackground()
			
			# Draw painter stuff
			self.printer.printCentered(painter, "Trip Summary", self.printer.fontXLarge, 0, 0, self.width, self.titleHeight, 50, 50, 50)
			self.printer.printCentered(painter, "Glance Patterns to the Display", self.printer.fontLarge, self.graphX, self.graphY - 60, self.graphWidth, self.heightFivePercent, 50, 50, 50)
			self.printer.printText(painter, "Trip Start", self.printer.fontNormal, self.graphX, self.graphY + self.graphHeight, self.width, self.height, 50, 50, 50)
			self.printer.printText(painter, "Trip End", self.printer.fontNormal, self.graphX + self.graphWidth - tripEndBR.right(), self.graphY + self.graphHeight, self.width, self.height, 50, 50, 50)
			self.printer.printCentered(painter, "Driving Safety Metrics", self.printer.fontLarge, self.dsmX, self.dsmY, self.dsmWidth, self.heightFivePercent, 50, 50, 50)
			
			# self.printer.printTextWrap(painter, u"\u2022", self.printer.fontSmall, self.dsmX + 10, self.dsmY + 70, self.dsmWidth - 60, self.dsmHeight, 50, 50, 50)
			self.printer.printTextWrap(painter, " %i"%(8-self.ube), self.printer.fontNormal, self.dsmX + 50, self.dsmY + 70, self.dsmWidth - 30, self.dsmHeight, 40, 193, 34)
			self.printer.printTextWrap(painter, "      out of 8 safe responses to lead    vehicle braking", self.printer.fontNormal, self.dsmX + 50, self.dsmY + 70, self.dsmWidth - 30, self.dsmHeight, 50, 50, 50)
			
			# self.printer.printTextWrap(painter, u"\u2022", self.printer.fontSmall, self.dsmX + 10, self.dsmY + 200, self.dsmWidth - 30, self.dsmHeight, 50, 50, 50)
			self.printer.printTextWrap(painter, " %i"%self.ube, self.printer.fontNormal, self.dsmX + 50, self.dsmY + 200, self.dsmWidth - 30, self.dsmHeight, 255, 0, 0)
			self.printer.printTextWrap(painter, "      out of 8 unsafe responses to    lead vehicle braking", self.printer.fontNormal, self.dsmX + 50, self.dsmY + 200, self.dsmWidth - 30, self.dsmHeight, 50, 50, 50)
			
			# self.printer.printTextWrap(painter, u"\u2022", self.printer.fontSmall, self.dsmX + 10, self.dsmY + 330, self.dsmWidth - 30, self.dsmHeight, 50, 50, 50)
			self.printer.printTextWrap(painter, " %i"%self.ld, self.printer.fontNormal, self.dsmX + 50, self.dsmY + 330, self.dsmWidth - 30, self.dsmHeight, 255, 0, 0)#255, 153, 255)
			self.printer.printTextWrap(painter, "      lane departures", self.printer.fontNormal, self.dsmX + 50, self.dsmY + 330, self.dsmWidth - 30, self.dsmHeight, 50, 50, 50)

			self.printer.printText(painter, str(int(self.low)), self.printer.fontNormal, self.lowRiskX + self.rectSize + 16, self.lowRiskY, self.width, self.height)
			self.printer.printText(painter, str(int(self.medium)), self.printer.fontNormal, self.mediumRiskX + self.rectSize + 16, self.mediumRiskY, self.width, self.height)
			self.printer.printText(painter, str(int(self.high)), self.printer.fontNormal, self.highRiskX + self.rectSize + 16, self.highRiskY, self.width, self.height)
			self.printer.printText(painter, "Low Risk Glances", self.printer.fontNormal, self.lowRiskX + self.rectSize + 150, self.lowRiskY, self.width, self.height)
			self.printer.printText(painter, "Medium Risk Glances", self.printer.fontNormal, self.mediumRiskX + self.rectSize + 150, self.mediumRiskY, self.width, self.height)
			self.printer.printText(painter, "High Risk Glances", self.printer.fontNormal, self.highRiskX + self.rectSize + 150, self.highRiskY, self.width, self.height)
			
			self.btnGraph1.drawText(painter, self.printer, self.printer.fontLarge)
			self.btnGraph3.drawText(painter, self.printer, self.printer.fontLarge)

		elif self.showing == self.GRAPH_TWO:
			self.paintCircle(self.lowIconX, self.lowIconY, self.glanceNumRadius, 0.851, 0.325, 0.31)
			self.paintCircle(self.mediumIconX, self.mediumIconY, self.glanceNumRadius, 0.941, 0.678, 0.305)
			self.paintCircle(self.highIconX, self.highIconY, self.glanceNumRadius, 0.5, 0.5, 0.5)
			
			self.btnGraph4.drawBackground()
			
			'''
			***********************************************************
			Removed the gl.GL_LINES block
			Added the paintLineHorizontal functions
			***********************************************************
			'''
			self.paintLineHorizontal(self.glancesGridX, self.glancesGridY + self.glancesGridBarPaddingTop, self.glancesGridX + self.glancesGridWidth, self.glancesGridY + self.glancesGridBarPaddingTop, 2, 0.3, 0.3, 0.3)
			self.paintLineHorizontal(self.glancesGridX, self.glancesGridY + self.glancesGridBarPaddingTop + (self.glancesGridBarHeight/2.0), self.glancesGridX + self.glancesGridWidth, self.glancesGridY + self.glancesGridBarPaddingTop + (self.glancesGridBarHeight/2.0), 2, 0.3, 0.3, 0.3)
			self.paintLineHorizontal(self.glancesGridX, self.glancesGridY + self.glancesGridHeight, self.glancesGridX + self.glancesGridWidth, self.glancesGridY + self.glancesGridHeight, 2, 0.3, 0.3, 0.3)
			
			gl.glBegin(gl.GL_QUADS)
			gl.glColor3f(0.5, 0.5, 0.5)
			gl.glVertex2f(self.glancesGridX, self.glancesGridTitleY)
			gl.glVertex2f(self.glancesGridX + self.glancesGridWidth, self.glancesGridTitleY)
			gl.glVertex2f(self.glancesGridX + self.glancesGridWidth, self.glancesGridTitleY + self.glancesGridTitleHeight)
			gl.glVertex2f(self.glancesGridX, self.glancesGridTitleY + self.glancesGridTitleHeight)
			gl.glVertex2f(self.tripsTitleX, self.tripsTitleY)
			gl.glVertex2f(self.tripsTitleX + self.tripsTitleWidth, self.tripsTitleY)
			gl.glVertex2f(self.tripsTitleX + self.tripsTitleWidth, self.tripsTitleY + self.tripsTitleHeight)
			gl.glVertex2f(self.tripsTitleX, self.tripsTitleY + self.tripsTitleHeight)

			# Safety metric text block
			gl.glVertex2f(self.safetyMetricsTitleX, self.safetyMetricsTitleY-60)
			gl.glVertex2f(self.safetyMetricsTitleX + self.safetyMetricsTitleWidth, self.safetyMetricsTitleY-60)
			gl.glVertex2f(self.safetyMetricsTitleX + self.safetyMetricsTitleWidth, self.safetyMetricsTitleY + self.safetyMetricsTitleHeight-60)
			gl.glVertex2f(self.safetyMetricsTitleX, self.safetyMetricsTitleY + self.safetyMetricsTitleHeight-60)
			
			# Comparison Bars -- COLOR
			# gl.glColor3f(0.67, 0.78, 0.82)
			gl.glColor3f(0.576, 0.72, 0.85)
			barOffset = self.glancesGridBarHeight - ((float(self.pastNumbersSum) / float(self.glancesGridMaxNum)) * self.glancesGridBarHeight)
			gl.glVertex2f(self.glancesGridX + self.glancesGridPadding, self.glancesGridY + barOffset + self.glancesGridBarPaddingTop)
			gl.glVertex2f(self.glancesGridX + self.glancesGridPadding + self.glancesGridBarWidth, self.glancesGridY + barOffset + self.glancesGridBarPaddingTop)
			gl.glVertex2f(self.glancesGridX + self.glancesGridPadding + self.glancesGridBarWidth, self.glancesGridY + self.glancesGridHeight)
			gl.glVertex2f(self.glancesGridX + self.glancesGridPadding, self.glancesGridY + self.glancesGridHeight)
			# gl.glColor3f(0.576, 0.65, 0.9)
			barOffset = self.glancesGridBarHeight - ((float(self.currentNumbersSum) / float(self.glancesGridMaxNum)) * self.glancesGridBarHeight)
			gl.glVertex2f(self.glancesGridX + (self.glancesGridPadding*2) + self.glancesGridBarWidth, self.glancesGridY + barOffset + self.glancesGridBarPaddingTop)
			gl.glVertex2f(self.glancesGridX + (self.glancesGridPadding*2) + (self.glancesGridBarWidth*2), self.glancesGridY + barOffset + self.glancesGridBarPaddingTop)
			gl.glVertex2f(self.glancesGridX + (self.glancesGridPadding*2) + (self.glancesGridBarWidth*2), self.glancesGridY + self.glancesGridHeight)
			gl.glVertex2f(self.glancesGridX + (self.glancesGridPadding*2) + self.glancesGridBarWidth, self.glancesGridY + self.glancesGridHeight)
			
			gl.glColor3f(0.7, 0.7, 0.7)
			gl.glVertex2f(self.glanceNumTitleX, self.glanceNumTitleY)
			gl.glVertex2f(self.glanceNumTitleX + self.glanceNumTitleWidth, self.glanceNumTitleY)
			gl.glVertex2f(self.glanceNumTitleX + self.glanceNumTitleWidth, self.glanceNumTitleY + self.glanceNumTitleHeight)
			gl.glVertex2f(self.glanceNumTitleX, self.glanceNumTitleY + self.glanceNumTitleHeight)
			
			gl.glVertex2f(self.safetyMetricsTitleX, self.safetyMetricsTitleY+20)
			gl.glVertex2f(self.safetyMetricsTitleX + self.safetyMetricsTitleWidth, self.safetyMetricsTitleY+20)
			gl.glVertex2f(self.safetyMetricsTitleX + self.safetyMetricsTitleWidth, self.safetyMetricsTitleY + self.safetyMetricsTitleHeight+20)
			gl.glVertex2f(self.safetyMetricsTitleX, self.safetyMetricsTitleY + self.safetyMetricsTitleHeight+20)
			gl.glEnd()
			
			bottomBar = self.glancesGridY + self.glancesGridHeight
			self.paintCircle(self.glancesGridX + self.glancesGridPadding + (self.glancesGridBarWidth/2.0), bottomBar - ((self.pastNumbers[2]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 18, 0.5, 0.5, 0.5)
			self.paintCircle(self.glancesGridX + self.glancesGridPadding + (self.glancesGridBarWidth/2.0), bottomBar - ((self.pastNumbers[1]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 18, 0.941, 0.678, 0.305)
			self.paintCircle(self.glancesGridX + self.glancesGridPadding + (self.glancesGridBarWidth/2.0), bottomBar - ((self.pastNumbers[0]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 18, 0.851, 0.325, 0.31)
			self.paintCircle(self.glancesGridX + self.glancesGridBarWidth + (self.glancesGridPadding*2) + (self.glancesGridBarWidth/2.0), bottomBar - ((self.currentNumbers[2]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 18, 0.5, 0.5, 0.5)
			self.paintCircle(self.glancesGridX + self.glancesGridBarWidth + (self.glancesGridPadding*2) + (self.glancesGridBarWidth/2.0), bottomBar - ((self.currentNumbers[1]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 18, 0.941, 0.678, 0.305)
			self.paintCircle(self.glancesGridX + self.glancesGridBarWidth + (self.glancesGridPadding*2) + (self.glancesGridBarWidth/2.0), bottomBar - ((self.currentNumbers[0]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 18, 0.851, 0.325, 0.31)
			
			self.paintLineHorizontal(self.glancesGridX + self.glancesGridPadding + (self.glancesGridBarWidth/2.0), bottomBar - ((self.pastNumbers[2]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), self.glancesGridX + self.glancesGridBarWidth + (self.glancesGridPadding*2) + (self.glancesGridBarWidth/2.0), bottomBar - ((self.currentNumbers[2]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 10, 0.5, 0.5, 0.5)
			self.paintLineHorizontal(self.glancesGridX + self.glancesGridPadding + (self.glancesGridBarWidth/2.0), bottomBar - ((self.pastNumbers[1]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), self.glancesGridX + self.glancesGridBarWidth + (self.glancesGridPadding*2) + (self.glancesGridBarWidth/2.0), bottomBar - ((self.currentNumbers[1]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 10, 0.941, 0.678, 0.305)
			self.paintLineHorizontal(self.glancesGridX + self.glancesGridPadding + (self.glancesGridBarWidth/2.0), bottomBar - ((self.pastNumbers[0]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), self.glancesGridX + self.glancesGridBarWidth + (self.glancesGridPadding*2) + (self.glancesGridBarWidth/2.0), bottomBar - ((self.currentNumbers[0]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 10, 0.851, 0.325, 0.31)
			
			self.paintCircle(self.glancesGridX + self.glancesGridPadding + (self.glancesGridBarWidth/2.0), bottomBar - ((self.pastNumbers[2]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 8, 1.0, 1.0, 1.0)
			self.paintCircle(self.glancesGridX + self.glancesGridPadding + (self.glancesGridBarWidth/2.0), bottomBar - ((self.pastNumbers[1]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 8, 1.0, 1.0, 1.0)
			self.paintCircle(self.glancesGridX + self.glancesGridPadding + (self.glancesGridBarWidth/2.0), bottomBar - ((self.pastNumbers[0]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 8, 1.0, 1.0, 1.0)
			self.paintCircle(self.glancesGridX + self.glancesGridBarWidth + (self.glancesGridPadding*2) + (self.glancesGridBarWidth/2.0), bottomBar - ((self.currentNumbers[2]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 8, 1.0, 1.0, 1.0)
			self.paintCircle(self.glancesGridX + self.glancesGridBarWidth + (self.glancesGridPadding*2) + (self.glancesGridBarWidth/2.0), bottomBar - ((self.currentNumbers[1]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 8, 1.0, 1.0, 1.0)
			self.paintCircle(self.glancesGridX + self.glancesGridBarWidth + (self.glancesGridPadding*2) + (self.glancesGridBarWidth/2.0), bottomBar - ((self.currentNumbers[0]/float(self.glancesGridMaxNum))*self.glancesGridBarHeight), 8, 1.0, 1.0, 1.0)
			
			self.printer.printCentered(painter, "Compare Recent Trips", self.printer.fontXLarge, 0, 0, self.width, self.titleHeight, 50, 50, 50)
			self.printer.printCentered(painter, "Glances to Display", self.printer.fontLarge, self.glancesGridTitleX, self.glancesGridTitleY, self.glancesGridTitleWidth, self.glancesGridTitleHeight, 240, 240, 240)
			self.printer.printCentered(painter, "Number of Glances", self.printer.fontLarge, self.tripsTitleX, self.tripsTitleY, self.tripsTitleWidth, self.tripsTitleHeight, 240, 240, 240)
			self.printer.printCentered(painter, "Trips:\t\t\t\tPrevious\t\t\t\tCurrent", self.printer.fontLarge, self.glanceNumTitleX, self.glanceNumTitleY, self.glanceNumTitleWidth, self.glanceNumTitleHeight, 240, 240, 240)
			self.printer.printCentered(painter, "Safety Metrics", self.printer.fontLarge, self.safetyMetricsTitleX, self.safetyMetricsTitleY-60, self.glanceNumTitleWidth, self.glanceNumTitleHeight, 240, 240, 240)
			self.printer.printCentered(painter, "Trips:\t\t\t\tPrevious\t\t\t\tCurrent", self.printer.fontLarge, self.safetyMetricsTitleX, self.safetyMetricsTitleY+20, self.glanceNumTitleWidth, self.glanceNumTitleHeight, 240, 240, 240)
			self.printer.printCenteredHor(painter, str(self.glancesGridMaxNum), self.printer.fontNormal, 0, self.glancesGridY + 3, self.glancesGridX, 100, 40, 40, 40)
			self.printer.printCenteredHor(painter, str(int(self.glancesGridMaxNum/2.0)), self.printer.fontNormal, 0, self.glancesGridY + 3 + (self.glancesGridBarHeight/2.0), self.glancesGridX, 100, 40, 40, 40)
			self.printer.printCenteredHor(painter, "0", self.printer.fontNormal, 0, self.glancesGridY + self.glancesGridHeight - 20, self.glancesGridX, 100, 40, 40, 40)
			self.printer.printCenteredHor(painter, "Previous", self.printer.fontNormal, self.glancesGridX + self.glancesGridPadding, self.glancesGridY + self.glancesGridHeight, self.glancesGridBarWidth, 100, 40, 40, 40)
			self.printer.printCenteredHor(painter, "Current", self.printer.fontNormal, self.glancesGridX + (self.glancesGridPadding*2) + self.glancesGridBarWidth, self.glancesGridY + self.glancesGridHeight, self.glancesGridBarWidth, 100, 40, 40, 40)
			self.printer.printText(painter, str(self.pastNumbers[2]), self.printer.fontNormal, self.highPastTitleX+40, self.highPastTitleY, self.width, self.height)
			self.printer.printText(painter, str(self.currentNumbers[2]), self.printer.fontNormal, self.highCurrentTitleX+45, self.highCurrentTitleY, self.width, self.height)
			self.printer.printText(painter, str(self.pastNumbers[1]), self.printer.fontNormal, self.mediumPastTitleX+40, self.mediumPastTitleY, self.width, self.height)
			self.printer.printText(painter, str(self.currentNumbers[1]), self.printer.fontNormal, self.mediumCurrentTitleX+45, self.mediumCurrentTitleY, self.width, self.height)
			self.printer.printText(painter, str(self.pastNumbers[0]), self.printer.fontNormal, self.lowPastTitleX+40, self.lowPastTitleY, self.width, self.height)
			self.printer.printText(painter, str(self.currentNumbers[0]), self.printer.fontNormal, self.lowCurrentTitleX+45, self.lowCurrentTitleY, self.width, self.height)
			self.printer.printText(painter, "Total", self.printer.fontNormal, self.totalTitleX, self.totalTitleY+20, self.width, self.height)
			self.printer.printText(painter, str(self.pastNumbersSum), self.printer.fontNormal, self.totalPastTitleX+40, self.totalPastTitleY+20, self.width, self.height)
			self.printer.printText(painter, str(self.currentNumbersSum), self.printer.fontNormal, self.totalCurrentTitleX+45, self.totalCurrentTitleY+20, self.width, self.height)
			self.printer.printText(painter, "Safe Braking", self.printer.fontNormal, self.safeEventTitleX, self.safeEventTitleY+40, self.width, self.height, 40, 193, 34)
			self.printer.printText(painter, "%s"%str(self.compSafe[0]), self.printer.fontNormal, self.safeEventPastNumTitleX+40, self.safeEventPastNumTitleY+40, self.width, self.height)
			self.printer.printText(painter, "%s"%str(self.compSafe[1]), self.printer.fontNormal, self.safeEventCurrentNumTitleX+45, self.safeEventCurrentNumTitleY+40, self.width, self.height)
			self.printer.printText(painter, "Unsafe Braking", self.printer.fontNormal, self.unsafeEventTitleX, self.unsafeEventTitleY+55, self.width, self.height, 217, 83, 79)
			self.printer.printText(painter, "%s"%str(self.compUnsafe[0]), self.printer.fontNormal, self.unsafeEventPastNumTitleX+40, self.unsafeEventPastNumTitleY+55, self.width, self.height)
			self.printer.printText(painter, "%s"%str(self.compUnsafe[1]), self.printer.fontNormal, self.unsafeEventCurrentNumTitleX+45, self.unsafeEventCurrentNumTitleY+55, self.width, self.height)
			self.printer.printText(painter, "Lane Departures", self.printer.fontNormal, self.deviationsEventTitleX, self.deviationsEventTitleY+70, self.width, self.height, 217, 83, 79)
			self.printer.printText(painter, "%s"%str(self.compLane[0]), self.printer.fontNormal, self.deviationsEventPastNumTitleX+40, self.deviationsEventPastNumTitleY+70, self.width, self.height)
			self.printer.printText(painter, "%s"%str(self.compLane[1]), self.printer.fontNormal, self.deviationsEventCurrentNumTitleX+45, self.deviationsEventCurrentNumTitleY+70, self.width, self.height)
			
			self.btnGraph4.drawText(painter, self.printer, self.printer.fontLarge)
			
		elif self.showing == self.BADGE_SCREEN:
			self.btnGraph2.drawBackground()
			
			self.badgeScreen.draw(painter)
			
			self.btnGraph2.drawText(painter, self.printer, self.printer.fontLarge)
			
		# End the painter
		painter.end()