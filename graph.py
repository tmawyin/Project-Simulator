from PySide import QtCore, QtGui, QtOpenGL

import OpenGL.GL as gl

class Graph(QtOpenGL.QGLWidget):
	def __init__(self, width, height):
		# Base constructor
		QtOpenGL.QGLWidget.__init__(self)
		
		# Set the attributes
		self.width = width
		self.height = height
		self.rectSize = 32.0
		self.gridCols = 0
		self.gridRows = 0
		self.grid = None
		
		# Load the fonts
		self.fontLarge = QtGui.QFont("Verdana", 25, 1, False)
		self.fontNormal = QtGui.QFont("Verdana", 15, 1, False)
		
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
		
	def createGrid(self, rows, cols):
		self.gridRows = rows
		self.gridCols = cols
		self.grid = [[0 for x in range(cols)] for x in range(rows)]
		
	def paintRect(self, x, y, red, green, blue):
		# Draw the background of the rectangle
		gl.glColor3f(red, green, blue)
		gl.glBegin(gl.GL_QUADS)
		gl.glVertex2f(x, y)
		gl.glVertex2f(x + self.rectSize, y)
		gl.glVertex2f(x + self.rectSize, y + self.rectSize)
		gl.glVertex2f(x, y + self.rectSize)
		gl.glEnd()
		
		# Draw the frame of the rectangle
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
		gl.glColor3f(0.3, 0.3, 0.3)
		gl.glBegin(gl.GL_QUADS)
		gl.glVertex2f(x, y)
		gl.glVertex2f(x + self.rectSize, y)
		gl.glVertex2f(x + self.rectSize, y + self.rectSize)
		gl.glVertex2f(x, y + self.rectSize)
		gl.glVertex2f(x + 3, y + 3)
		gl.glVertex2f(x + self.rectSize - 3, y + 3)
		gl.glVertex2f(x + self.rectSize - 3, y + self.rectSize - 3)
		gl.glVertex2f(x + 3, y + self.rectSize - 3)
		gl.glEnd()
		
		# Revert the drawing mode
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
		
	def printCenteredHor(self, painter, str, font, y = 0):
		painter.setFont(font)
		painter.drawText(0, y, self.width, self.height, QtCore.Qt.AlignHCenter, str)
		
	def printText(self, painter, str, font, x, y, red = 0, green = 0, blue = 0):
		painter.setPen(QtGui.QColor(red, green, blue))
		painter.setFont(font)
		painter.drawText(x, y, self.width, self.height, QtCore.Qt.AlignLeft, str)
		
	def getTextCenteredHorBox(self, painter, str, font, y = 0):
		painter.setFont(font)
		rect = painter.boundingRect(0, y, self.width, self.height, QtCore.Qt.AlignHCenter, str)
		return rect
		
	def paintGrid(self):
		# Calculate the dimensions of the grid
		gridPadding = 10
		gridWidth = (self.gridCols * self.rectSize) + (self.gridCols * 4) + gridPadding
		gridHeight = (self.gridRows * self.rectSize) + (self.gridRows * 4) + gridPadding
		gridX = (self.width/2) - (gridWidth/2) - (gridPadding/2)
		gridY = 100
		
		# Draw the border of the grid
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
		gl.glBegin(gl.GL_QUADS);
		gl.glVertex2f(gridX - 10, gridY)
		gl.glVertex2f(gridX + gridWidth + 10, gridY)
		gl.glVertex2f(gridX + gridWidth + 10, gridY + gridHeight)
		gl.glVertex2f(gridX - 10, gridY + gridHeight)
		gl.glEnd()
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
		
		# Fill the grid
		for r, g in enumerate(self.grid):
			for c, v in enumerate(g):
				if v > 0:
					rectx = (gridX + gridPadding/2) + (c * self.rectSize) + (c * 4)
					recty = (gridY + gridPadding/2) + (r * self.rectSize) + (r * 4)
					if v == 1:
						self.paintRect(rectx, recty, 0.7, 0.7, 0.7)
					elif v == 2:
						self.paintRect(rectx, recty, 0.9412, 0.6784, 0.3059)
					elif v == 3:
						self.paintRect(rectx, recty, 0.851, 0.3255, 0.3099)
		return (gridX, gridY, gridWidth, gridHeight)
		
	def paintEvent(self, event):
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		gl.glLoadIdentity();
		
		# Initialize the painter
		painter = QtGui.QPainter()
		painter.begin(self)
		
		# Get the bounding rectangles
		rattdBR = self.getTextCenteredHorBox(painter, "represents a glance to the display", self.fontNormal, 55)
		endBR = self.getTextCenteredHorBox(painter, "END", self.fontNormal, 0)
		
		# Draw OpenGL stuff
		self.paintRect(rattdBR.left() - self.rectSize - 10, rattdBR.top(), 1.0, 1.0, 1.0)
		gridRect = self.paintGrid()
		self.paintRect(570, gridRect[1] + gridRect[3] + 80, 0.851, 0.3255, 0.3099)
		self.paintRect(720, gridRect[1] + gridRect[3] + 80, 0.9412, 0.6784, 0.3059)
		self.paintRect(900, gridRect[1] + gridRect[3] + 80, 0.7, 0.7, 0.7)
		
		gl.glBegin(gl.GL_LINES)
		gl.glVertex2f(140.0, gridRect[1] + gridRect[3] + 210)
		gl.glVertex2f(140.0, gridRect[1] + gridRect[3] + 300)
		gl.glVertex2f(140.0, gridRect[1] + gridRect[3] + 300)
		gl.glVertex2f(400.0, gridRect[1] + gridRect[3] + 300)
		
		gl.glVertex2f(560.0, gridRect[1] + gridRect[3] + 210)
		gl.glVertex2f(560.0, gridRect[1] + gridRect[3] + 300)
		gl.glVertex2f(560.0, gridRect[1] + gridRect[3] + 300)
		gl.glVertex2f(820.0, gridRect[1] + gridRect[3] + 300)
		
		gl.glVertex2f(980.0, gridRect[1] + gridRect[3] + 210)
		gl.glVertex2f(980.0, gridRect[1] + gridRect[3] + 300)
		gl.glVertex2f(980.0, gridRect[1] + gridRect[3] + 300)
		gl.glVertex2f(1240.0, gridRect[1] + gridRect[3] + 300)
		gl.glEnd()
		
		gl.glLineWidth(20.0)
		gl.glBegin(gl.GL_LINES)
		gl.glColor3f(0.3255, 0.851, 0.3099)
		gl.glVertex2f(140.0, gridRect[1] + gridRect[3] + 270)
		gl.glVertex2f(400.0, gridRect[1] + gridRect[3] + 270)
		
		gl.glColor3f(0.851, 0.3255, 0.3099)
		gl.glVertex2f(560.0, gridRect[1] + gridRect[3] + 270)
		gl.glVertex2f(820.0, gridRect[1] + gridRect[3] + 270)
		gl.glEnd()
		
		gl.glLineStipple(2, 0xF00F)
		gl.glBegin(gl.GL_LINES)
		gl.glVertex2f(980.0, gridRect[1] + gridRect[3] + 270)
		gl.glVertex2f(1100.0, gridRect[1] + gridRect[3] + 270)
		gl.glEnd()
		
		# Reset the line attributes
		gl.glLineStipple(1, 0xFFFF)		
		gl.glLineWidth(1.0)
		
		# Draw painter stuff
		self.printCenteredHor(painter, "Summary of Your Drive", self.fontLarge, 0)
		self.printCenteredHor(painter, "represents a glance to the display", self.fontNormal, 55)
		self.printText(painter, "START", self.fontNormal, gridRect[0] - 20, gridRect[1] + gridRect[3])
		self.printText(painter, "END", self.fontNormal, (gridRect[0] + gridRect[2]) - 40, gridRect[1] + gridRect[3])
		self.printText(painter, "Distraction Level:", self.fontNormal, 350, gridRect[1] + gridRect[3] + 40)
		self.printText(painter, "High", self.fontNormal, 570, gridRect[1] + gridRect[3] + 40)
		self.printText(painter, "Medium", self.fontNormal, 720, gridRect[1] + gridRect[3] + 40)
		self.printText(painter, "Low", self.fontNormal, 900, gridRect[1] + gridRect[3] + 40)
		self.printText(painter, "32%", self.fontNormal, 610, gridRect[1] + gridRect[3] + 83)
		self.printText(painter, "32%", self.fontNormal, 760, gridRect[1] + gridRect[3] + 83)
		self.printText(painter, "36%", self.fontNormal, 940, gridRect[1] + gridRect[3] + 83)
		self.printCenteredHor(painter, "Driving Performance", self.fontNormal, gridRect[1] + gridRect[3] + 140)
		self.printText(painter, "Safety Indicator:", self.fontNormal, 500, gridRect[1] + gridRect[3] + 170)
		self.printText(painter, "Safe", self.fontNormal, 690, gridRect[1] + gridRect[3] + 170, 92, 184, 92)
		self.printText(painter, "Unsafe", self.fontNormal, 750, gridRect[1] + gridRect[3] + 170, 217, 83, 79)
		self.printText(painter, "4 safe braking events", self.fontNormal, 150, gridRect[1] + gridRect[3] + 220)
		self.printText(painter, "4 unsafe braking events", self.fontNormal, 570, gridRect[1] + gridRect[3] + 220)
		self.printText(painter, "2 lane deviations", self.fontNormal, 990, gridRect[1] + gridRect[3] + 220)
		
		# End the painter
		painter.end()