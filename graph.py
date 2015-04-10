from PySide import QtCore, QtGui, QtOpenGL
import numpy as np
import csv
import OpenGL.GL as gl

class Graph(QtOpenGL.QGLWidget):
	def __init__(self, width, height):
		# Base constructor
		QtOpenGL.QGLWidget.__init__(self)
		
		# Set the attributes
		self.width = width
		self.height = height
		self.rectSize = 45.0
		self.gridCols = 0
		self.gridRows = 0
		self.grid = None
		
		# Load the fonts
		self.fontXLarge = QtGui.QFont("Verdana", 32, QtGui.QFont.Bold, False)
		self.fontLarge = QtGui.QFont("Verdana", 24, QtGui.QFont.Bold, False)
		self.fontNormal = QtGui.QFont("Verdana", 20, 1, False)
		self.fontSmall  = QtGui.QFont("Verdana", 16, 1, False)
		
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
		self.highRiskX = self.dsmX
		self.highRiskY = self.graphY
		self.mediumRiskX = self.dsmX
		self.mediumRiskY = self.graphY + self.rectSize + 30
		self.lowRiskX = self.dsmX
		self.lowRiskY = self.graphY + (self.rectSize * 2) + 60
		
		
	def initializeGL(self):
		# Initialize the context
		gl.glClearColor(1.0, 1.0, 1.0, 1)
		gl.glEnable(gl.GL_LINE_STIPPLE)
		
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
		
	def createGraph(self, parID, rows, cols):
		self.gridRows = rows
		self.gridCols = cols
		self.grid = [[0 for x in range(cols)] for x in range(rows)]
		self.ube = 0
		self.ld = 0
		self.high = 0
		self.medium = 0
		self.low = 0
		
		# Calculate the size of the rectangles
		'''self.rectSize = self.graphWidth if self.graphHeight > self.graphWidth else self.graphHeight
		#self.rectSize = self.graphWidth
		self.rectSize = self.rectSize - (self.graphPadding * 2)
		self.rectSize = self.rectSize - (self.rectPadding * (self.gridCols - 1))
		self.rectSize = self.rectSize/self.gridCols
		print(self.rectSize)'''
		
		numRows = 900

		# Variables: Counters to keep track of values
		listValues = []
		gridValues = []
		lowCount = 0
		warnCount = 0
		dangerCount = 0
		bbTime = 0			# <1.2s
		timeCollision = 0	# <1.5s
		laneDepart = 0		# <-5
		numCollision = 0	# >1
		accelCount = 0		# < -19.3 ft/s**2
		lineCount = 0
		timeUBE = []		# keeps track of where unsafe breaking events
		isLaneDepart = False
		isAccel = False
		isCollisiton = False

		receiverData = np.genfromtxt('%s_data.csv'%parID, delimiter=',')
		netclientData = np.genfromtxt('%s_net.csv'%parID, delimiter=',')

		# Reading Receiver Data
		for i in range(len(receiverData)):
			# Counting for Number of Collisions
			if float(receiverData[i,2]) > 1:
				numCollision += 1
			# Counting for Lane Deviation
			if float(receiverData[i,4]) < -3:
				isLaneDepart = True
			if isLaneDepart == True and float(receiverData[i,4]) >= -3:
				isLaneDepart = False
				laneDepart += 1
			# Counting for Bumper to Bumper Time
			if float(receiverData[i,6]) < 1.2:
				bbTime += 0
			# Counting for Time to Collision
			if float(receiverData[i,8]) <1.5 and float(receiverData[i,8]) !=0:
				isCollisiton = True
			if isCollisiton == True and float(receiverData[i,8]) >= 1.5:
				isCollisiton = False
				timeCollision += 0
			# Counting for Acceleration
			if float(receiverData[i,10]) < -19.3:
				isAccel = True
			if isAccel == True and float(receiverData[i,10]) >= -19.3:
				isAccel = False
				accelCount += 1
				timeUBE.append(receiverData[i,0])

		self.ube += bbTime + timeCollision + accelCount
		self.ld += laneDepart
		self.timeEvent = (timeUBE-receiverData[0,0])/(receiverData[len(receiverData)-1,0] - receiverData[0,0])

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

			if lineCount == numRows:
				#listValues.append([lowCount,warnCount,dangerCount,numCollision,laneDepart,bbTime,timeCollision,accelCount])
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

		# Add percentage as labels:
		# total = self.high + self.medium + self.low
		# if total == 0:
		# 	total = 1.0
		# self.high = round((self.high/float(total)) * 100)
		# self.medium = round((self.medium/float(total)) * 100)
		# self.low = round((self.low/float(total)) * 100)
		
		self.grid = np.zeros((self.gridRows, self.gridCols))
		minLength = len(gridValues) if self.gridCols > len(gridValues) else self.gridCols
		for i in range(minLength):
			gridValues[i].reverse()
			self.grid[:,i] = np.array(gridValues[i])
	
	def paintLine(self, x1, y1, x2, y2, width, red = 0, green = 0, blue = 0):
		gl.glColor3f(red, green, blue)
		gl.glBegin(gl.GL_QUADS)
		gl.glVertex2f(x1, y1+70)
		gl.glVertex2f(x1 + width, y1+70)
		gl.glVertex2f(x2 + width, y2-10)
		gl.glVertex2f(x2, y2-10)
		gl.glEnd()	
	
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
		
	def printCentered(self, painter, str, font, x, y, width, height, red = 0, green = 0, blue = 0):
		painter.setPen(QtGui.QColor(red, green, blue))
		painter.setFont(font)
		painter.drawText(x, y, width, height, QtCore.Qt.AlignCenter, str)
		
	def printCenteredHor(self, painter, str, font, y = 0):
		painter.setFont(font)
		painter.drawText(0, y, self.width, self.height, QtCore.Qt.AlignHCenter, str)
		
	def printText(self, painter, str, font, x, y, red = 0, green = 0, blue = 0):
		painter.setPen(QtGui.QColor(red, green, blue))
		painter.setFont(font)
		painter.drawText(x, y, self.width, self.height, QtCore.Qt.AlignLeft, str)
		
	def printTextBox(self, painter, str, font, x, y, width, height, red = 0, green = 0, blue = 0):
		painter.setPen(QtGui.QColor(red, green, blue))
		painter.setFont(font)
		painter.drawText(x, y, width, height, QtCore.Qt.TextWordWrap, str)
		
	def getTextBox(self, painter, str, font):
		painter.setFont(font)
		return painter.boundingRect(0, 0, 0, 0, QtCore.Qt.AlignLeft, str)
		
	def getTextCenteredBox(self, painter, str, font, x, y, width, height):
		painter.setFont(font)
		rect = painter.boundingRect(x, y, width, height, QtCore.Qt.AlignCenter, str)
		return rect
		
	def getTextCenteredHorBox(self, painter, str, font, y = 0):
		painter.setFont(font)
		rect = painter.boundingRect(0, y, self.width, self.height, QtCore.Qt.AlignHCenter, str)
		return rect
		
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
		# for i in range(len(self.timeEvent)):
		# 	xposition = self.graphX + (self.timeEvent[i] * self.graphWidth)
		# 	self.paintLine(xposition, self.graphY, xposition, self.graphY + self.graphHeight, 2, 1.0, 0.0, 0.0)
		for i in range(len(self.timeEvent)):
			xposition = self.graphX + (self.timeEvent[i] * (((self.gridCols * self.rectSize) + (2 * self.graphPadding)) - ((self.gridCols + 1) * self.rectPadding)))
			if xposition < (self.graphX + self.graphWidth):
				self.paintLine(xposition, self.graphY, xposition, self.graphY + self.graphHeight, 2, 1.0, 0.0, 0.0)
		
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
		
	def paintEvent(self, event):
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		gl.glLoadIdentity();
		
		# Initialize the painter
		painter = QtGui.QPainter()
		painter.begin(self)
		
		# Get the bounding rectangles
		tripEndBR = self.getTextBox(painter, "Trip End", self.fontNormal)
		#rattdBR = self.getTextCenteredBox(painter, "represents a glance to the display", self.fontNormal, 0, self.legendY, self.width, self.legendHeight)
		#startBR = self.getTextBox(painter, "START", self.fontNormal)
		#endBR = self.getTextCenteredHorBox(painter, "END", self.fontNormal, 0)
		
		# Draw OpenGL stuff
		self.paintGrid()
		self.paintDSM()
		
		#self.paintRect(rattdBR.left() - self.rectSize - 10, rattdBR.top(), 1.0, 1.0, 1.0)
		#gridRect = self.paintGrid()
		
		self.paintRect(self.highRiskX, self.highRiskY, 0.851, 0.3255, 0.3099)
		self.paintRect(self.mediumRiskX, self.mediumRiskY, 0.9412, 0.6784, 0.3059)
		self.paintRect(self.lowRiskX, self.lowRiskY, 0.7, 0.7, 0.7)
		
		'''gl.glLineWidth(20.0)
		gl.glBegin(gl.GL_LINES)
		gl.glColor3f(0.3255, 0.851, 0.3099)
		gl.glVertex2f(self.sbeX, self.eventsY + (self.eventsHeight * 0.7))
		gl.glVertex2f(self.sbeX + self.eventsWidth, self.eventsY + (self.eventsHeight * 0.7))
		
		gl.glColor3f(0.851, 0.3255, 0.3099)
		gl.glVertex2f(self.ubeX, self.eventsY + (self.eventsHeight * 0.7))
		gl.glVertex2f(self.ubeX + self.eventsWidth, self.eventsY + (self.eventsHeight * 0.7))
		gl.glEnd()
		
		#gl.glLineStipple(1, 0xFC3F)
		gl.glLineStipple(1, 0xF00F)
		gl.glBegin(gl.GL_LINES)
		gl.glVertex2f(self.ldX, self.eventsY + (self.eventsHeight * 0.7))
		gl.glVertex2f(self.ldX + (self.eventsWidth * 0.5), self.eventsY + (self.eventsHeight * 0.7))
		gl.glEnd()
		
		# Reset the line attributes
		gl.glLineStipple(1, 0xFFFF)		
		gl.glLineWidth(1.0)
		gl.glColor3f(0.0, 0.0, 0.0)
		
		gl.glBegin(gl.GL_LINES)
		# Draw the graph border for the safe braking events
		gl.glVertex2f(self.sbeX, self.eventsY)
		gl.glVertex2f(self.sbeX, self.eventsY + self.eventsHeight)
		gl.glVertex2f(self.sbeX, self.eventsY + self.eventsHeight)
		gl.glVertex2f(self.sbeX + self.eventsWidth, self.eventsY + self.eventsHeight)
		
		# Draw the graph border for the unsafe braking events
		gl.glVertex2f(self.ubeX, self.eventsY)
		gl.glVertex2f(self.ubeX, self.eventsY + self.eventsHeight)
		gl.glVertex2f(self.ubeX, self.eventsY + self.eventsHeight)
		gl.glVertex2f(self.ubeX + self.eventsWidth, self.eventsY + self.eventsHeight)
		
		# Draw the graph border for the lane deviations
		gl.glVertex2f(self.ldX, self.eventsY)
		gl.glVertex2f(self.ldX, self.eventsY + self.eventsHeight)
		gl.glVertex2f(self.ldX, self.eventsY + self.eventsHeight)
		gl.glVertex2f(self.ldX + self.eventsWidth, self.eventsY + self.eventsHeight)
		gl.glEnd()'''
		
		# Draw painter stuff
		self.printCentered(painter, "Trip Summary", self.fontXLarge, 0, 0, self.width, self.titleHeight, 50, 50, 50)
		self.printCentered(painter, "Glance Patterns to the Display", self.fontLarge, self.graphX, self.graphY + 10, self.graphWidth, self.heightFivePercent, 50, 50, 50)
		self.printText(painter, "Trip Start", self.fontNormal, self.graphX, self.graphY + self.graphHeight, 50, 50, 50)
		self.printText(painter, "Trip End", self.fontNormal, self.graphX + self.graphWidth - tripEndBR.right(), self.graphY + self.graphHeight, 50, 50, 50)
		self.printCentered(painter, "Driving Safety Metrics", self.fontLarge, self.dsmX, self.dsmY, self.dsmWidth, self.heightFivePercent, 50, 50, 50)
		
		self.printTextBox(painter, u"\u2022", self.fontSmall, self.dsmX + 10, self.dsmY + 70, self.dsmWidth - 60, self.dsmHeight, 50, 50, 50)
		self.printTextBox(painter, "%i"%(8-self.ube), self.fontNormal, self.dsmX + 50, self.dsmY + 70, self.dsmWidth - 30, self.dsmHeight, 40, 193, 34)
		self.printTextBox(painter, "   out of 8 safe responses to lead vehicle braking", self.fontNormal, self.dsmX + 50, self.dsmY + 70, self.dsmWidth - 30, self.dsmHeight, 50, 50, 50)
		
		self.printTextBox(painter, u"\u2022", self.fontSmall, self.dsmX + 10, self.dsmY + 200, self.dsmWidth - 30, self.dsmHeight, 50, 50, 50)
		self.printTextBox(painter, "%i"%self.ube, self.fontNormal, self.dsmX + 50, self.dsmY + 200, self.dsmWidth - 30, self.dsmHeight, 255, 0, 0)
		self.printTextBox(painter, "   out of 8 unsafe responses to lead vehicle braking", self.fontNormal, self.dsmX + 50, self.dsmY + 200, self.dsmWidth - 30, self.dsmHeight, 50, 50, 50)
		
		self.printTextBox(painter, u"\u2022", self.fontSmall, self.dsmX + 10, self.dsmY + 330, self.dsmWidth - 30, self.dsmHeight, 50, 50, 50)
		self.printTextBox(painter, "%i"%self.ld, self.fontNormal, self.dsmX + 50, self.dsmY + 330, self.dsmWidth - 30, self.dsmHeight, 255, 0, 0)
		self.printTextBox(painter, "   lane deviations", self.fontNormal, self.dsmX + 50, self.dsmY + 330, self.dsmWidth - 30, self.dsmHeight, 50, 50, 50)

		self.printText(painter, str(int(self.high)), self.fontNormal, self.highRiskX + self.rectSize + 16, self.highRiskY)
		self.printText(painter, str(int(self.medium)), self.fontNormal, self.mediumRiskX + self.rectSize + 16, self.mediumRiskY)
		self.printText(painter, str(int(self.low)), self.fontNormal, self.lowRiskX + self.rectSize + 16, self.lowRiskY)
		self.printText(painter, "High Risk Glances", self.fontNormal, self.highRiskX + self.rectSize + 150, self.highRiskY)
		self.printText(painter, "Medium Risk Glances", self.fontNormal, self.mediumRiskX + self.rectSize + 150, self.mediumRiskY)
		self.printText(painter, "Low Risk Glances", self.fontNormal, self.lowRiskX + self.rectSize + 150, self.lowRiskY)
		# print(colored("Hello world in red style!", 'red'))

		'''self.printCentered(painter, "Summary of Your Drive", self.fontXLarge, 0, 0, self.width, self.legendHeight)
		self.printCentered(painter, "represents a glance to the display", self.fontNormal, 0, self.legendY, self.width, self.legendHeight)
		self.printText(painter, "START", self.fontNormal, gridRect[0] - (startBR.right()/2), gridRect[1] + gridRect[3] + 10)
		self.printText(painter, "END", self.fontNormal, (gridRect[0] + gridRect[2]) - (startBR.right()/2), gridRect[1] + gridRect[3] + 10)
		self.printText(painter, "Distraction Level:", self.fontNormal, self.dlX, self.dlY)
		self.printText(painter, "High", self.fontNormal, self.highX, self.dlY)
		self.printText(painter, "Medium", self.fontNormal, self.mediumX, self.dlY)
		self.printText(painter, "Low", self.fontNormal, self.lowX, self.dlY)
		self.printText(painter, str(int(self.high)) + "%", self.fontNormal, self.highX + self.rectSize + 8, self.dlY + 43)
		self.printText(painter, str(int(self.medium)) + "%", self.fontNormal, self.mediumX + self.rectSize + 8, self.dlY + 43)
		self.printText(painter, str(int(self.low)) + "%", self.fontNormal, self.lowX + self.rectSize + 8, self.dlY + 43)
		self.printCenteredHor(painter, "Driving Performance", self.fontLarge, self.dpY)
		self.printText(painter, "Safety Indicator:", self.fontNormal, self.siX, self.siY)
		self.printText(painter, "Safe", self.fontNormal, self.safeX, self.siY, 92, 184, 92)
		self.printText(painter, "Unsafe", self.fontNormal, self.unsafeX, self.siY, 217, 83, 79)
		self.printText(painter, "4 safe braking events", self.fontNormal, self.sbeX + 10, self.eventsY + (self.eventsHeight*0.15))
		self.printText(painter, "%i unsafe braking events"%self.ube, self.fontNormal, self.ubeX + 10, self.eventsY + (self.eventsHeight*0.15))
		self.printText(painter, "%i lane deviations"%self.ld, self.fontNormal, self.ldX + 10, self.eventsY + (self.eventsHeight*0.15))'''
		
		# End the painter
		painter.end()