import OpenGL.GL as gl
import os
import sys
import pygame
from PySide import QtCore, QtGui, QtOpenGL
from Printer import Printer
from Button import Button
from ImageButton import ImageButton

class OpenglScreen(QtOpenGL.QGLWidget):
	SELECT_SCREEN = 1
	INTRO_SCREEN_1 = 2
	INTRO_SCREEN_2 = 3
	INTRO_SCREEN_3 = 4
	BADGE_SCREEN = 5

	def __init__(self, width, height):	
		# Base constructor
		QtOpenGL.QGLWidget.__init__(self)
		self.setMouseTracking(True)
		self.width = width
		self.height = height
		
		# Initialize the painter
		self.painter = QtGui.QPainter()
		self.printer = Printer()
		
		self.gender = -1
		self.avatarImg = None
		self.avatarTex = None

		# Adding the avatar buttons
		# Avatar Male
		self.initMImg = pygame.image.load("../../images/wireframe_m0.png")
		self.initMTex = 0
		# Avatar Female
		self.initFImg = pygame.image.load("../../images/wireframe_f0.png")
		self.initFTex = 0
		
		self.welcomeImg = pygame.image.load("../../images/welcome_intro/welcome_noavatars.png")
		self.welcomeTex = 0
		
		# self.btnGraph1 = Button(u"\u25c4", 10, 15, 100, 50)
		# self.btnGraph2 = Button(u"\u25ba", self.width - 110, 15, 100, 50)

		self.Next1btn = Button(u"\u25ba", self.width - 110, 15, 100, 50)
		self.Next1btn.disable()
		self.Next2btn = Button(u"\u25ba", self.width - 110, 15, 100, 50)
		self.Next2btn.disable()
		self.Next3btn = Button(u"\u25ba", self.width - 110, 15, 100, 50)
		self.Next3btn.disable()
		self.btnOkay = Button("DONE", self.width - 130, 15, 120, 50)
		self.btnOkay.disable()

		self.Back1btn = Button(u"\u25c4", 10, 15, 100, 50)
		self.Back1btn.disable()
		self.Back2btn = Button(u"\u25c4", 10, 15, 100, 50)
		self.Back2btn.disable()
		self.Back3btn = Button(u"\u25c4", 10, 15, 100, 50)
		self.Back3btn.disable()

		self.showing = self.SELECT_SCREEN


	def initializeGL(self):
		#self.autoBufferSwap(False)
	
		# Initialize the context
		gl.glClearColor(0.94, 0.94, 0.0, 1)
		gl.glEnable(gl.GL_LINE_STIPPLE)
		gl.glEnable(gl.GL_TEXTURE_2D)
		
		# self.badgeScreen.init("")
		self.initMTex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.initMTex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.initMImg.get_width(), self.initMImg.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.initMImg, "RGBA", 1))
		# Avatar Female
		self.initFTex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.initFTex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.initFImg.get_width(), self.initFImg.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.initFImg, "RGBA", 1))
		
		self.welcomeTex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.welcomeTex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.welcomeImg.get_width(), self.welcomeImg.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.welcomeImg, "RGBA", 1))

		self.buttonM = ImageButton(self.initMImg, self.initMTex, 1090, 535)
		self.buttonF = ImageButton(self.initFImg, self.initFTex, 444, 535)
		self.buttonM.enable()
		self.buttonF.enable()
		
	def resizeGL(self, width, height):
		# Update the attributes
		self.width = width
		self.height = height
		
		# Set up an orthographic view
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glLoadIdentity()
		gl.glOrtho(0, self.width, self.height, 0, -1, 1)
		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()
		
		# Set up the viewport
		gl.glViewport(0, 0, width, height)
	
	# Displaying the images for the new screens
	def displayImage(self, texture, image, x, y):
		gl.glPushMatrix()
		gl.glLoadIdentity()
		gl.glColor3f(0.94, 0.94, 0.94)
		#gl.glColor4f(1.0, 1.0, 1.0, 0.0)
		gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
		gl.glBegin(gl.GL_QUADS)
		gl.glTexCoord2f(0.0, 1.0)
		gl.glVertex2f(x, y)
		
		gl.glTexCoord2f(1.0, 1.0)
		gl.glVertex2f(x+image.get_width(), y)
		
		gl.glTexCoord2f(1.0, 0.0)
		gl.glVertex2f(x+image.get_width(), y+image.get_height())
		
		gl.glTexCoord2f(0.0, 0.0)
		gl.glVertex2f(x, y+image.get_height())
		gl.glEnd()
		gl.glPopMatrix()
		gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

	def mouseMoveEvent(self, event):
		self.buttonM.update(event.x(), event.y())
		self.buttonF.update(event.x(), event.y())
		self.btnOkay.update(event.x(), event.y())
		self.Next1btn.update(event.x(), event.y())
		self.Next2btn.update(event.x(), event.y())
		self.Next3btn.update(event.x(), event.y())
		self.btnOkay.update(event.x(), event.y())
		self.Back1btn.update(event.x(), event.y())
		self.Back2btn.update(event.x(), event.y())
		self.Back3btn.update(event.x(), event.y())
		self.repaint()
		
	def mousePressEvent(self, event):
		if( self.buttonM.isMouseOver() == True ):
			self.showing = self.INTRO_SCREEN_1
			self.Next1btn.enable()
			self.buttonF.disable()
			self.buttonM.disable()
			self.gender = 0	# Checking if male
			self.repaint()
		
		elif( self.buttonF.isMouseOver() == True ):
			self.showing = self.INTRO_SCREEN_1
			self.Next1btn.enable()
			self.buttonF.disable()
			self.buttonM.disable()
			self.gender = 1	# Checking if female
			self.repaint()
			
		if( self.Next1btn.isMouseOver() == True ):
			self.showing = self.INTRO_SCREEN_2
			self.Next2btn.enable()
			self.Back1btn.enable()
			self.Next1btn.disable()
			self.repaint()

		if( self.Next2btn.isMouseOver() == True ):
			self.showing = self.INTRO_SCREEN_3
			self.Next3btn.enable()
			self.Back2btn.enable()
			self.Next2btn.disable()
			self.repaint()

		if( self.Next3btn.isMouseOver() == True ):
			self.showing = self.BADGE_SCREEN
			self.btnOkay.enable()
			self.Back3btn.enable()
			self.Next3btn.disable()
			self.repaint()
			
		if( self.btnOkay.isMouseOver() == True ):
			import subprocess
			# os.chdir('../')
			theproc = subprocess.Popen([sys.executable, "index.py"])
			theproc.communicate()
			sys.exit(0)

		if( self.Back1btn.isMouseOver() == True ):
			self.showing = self.INTRO_SCREEN_1
			self.Back1btn.disable()
			self.Next2btn.disable()
			self.Next1btn.enable()
			self.repaint()

		if( self.Back2btn.isMouseOver() == True ):
			self.showing = self.INTRO_SCREEN_2
			self.Back2btn.disable()
			self.Next3btn.disable()
			self.Next2btn.enable()
			self.Back1btn.enable()
			self.repaint()

		if( self.Back3btn.isMouseOver() == True ):
			self.showing = self.INTRO_SCREEN_3
			self.Back3btn.disable()
			self.btnOkay.disable()
			self.Next3btn.enable()
			self.Back2btn.enable()
			self.repaint()

	def paintEvent(self, event):
		self.painter.begin(self)
		self.resizeGL(self.width, self.height)
		
		gl.glClearColor(0.94, 0.94, 0.94, 1)
		
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		gl.glLoadIdentity()
		
		if self.showing == self.SELECT_SCREEN:
			self.displayImage(self.welcomeTex,self.welcomeImg, 0, 0)
			self.buttonM.drawBackground()
			self.buttonF.drawBackground()
		
		elif self.showing == self.INTRO_SCREEN_1:
			# Loading the corresponding images based on the gender
			if self.gender == 0:
				self.intro1_Img = pygame.image.load("../../images/welcome_intro/intro_male_1.png")
				self.intro1_Tex = 0
				self.intro2_Img = pygame.image.load("../../images/welcome_intro/intro_male_2.png")
				self.intro2_Tex = 0
				self.intro3_Img = pygame.image.load("../../images/welcome_intro/intro_male_3.png")
				self.intro3_Tex = 0
				self.intro4_Img = pygame.image.load("../../images/welcome_intro/intro_male_4.png")
				self.intro4_Tex = 0
			else:
				self.intro1_Img = pygame.image.load("../../images/welcome_intro/intro_female_1.png")
				self.intro1_Tex = 0
				self.intro2_Img = pygame.image.load("../../images/welcome_intro/intro_female_2.png")
				self.intro2_Tex = 0
				self.intro3_Img = pygame.image.load("../../images/welcome_intro/intro_female_3.png")
				self.intro3_Tex = 0
				self.intro4_Img = pygame.image.load("../../images/welcome_intro/intro_female_4.png")
				self.intro4_Tex = 0

			# Getting the images ready to display
			self.intro1_Tex = gl.glGenTextures(1)
			gl.glBindTexture(gl.GL_TEXTURE_2D, self.intro1_Tex)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
			gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.intro1_Img.get_width(), self.intro1_Img.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.intro1_Img, "RGBA", 1))

			# Displaying everything for First intro screen
			self.displayImage(self.intro1_Tex,self.intro1_Img, 0, 0)
			self.Next1btn.drawBackground()
			self.Next1btn.drawText(self.painter, self.printer, self.printer.fontNormal)

		elif self.showing == self.INTRO_SCREEN_2:
			# Getting the images ready to display
			self.intro2_Tex = gl.glGenTextures(1)
			gl.glBindTexture(gl.GL_TEXTURE_2D, self.intro2_Tex)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
			gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.intro2_Img.get_width(), self.intro2_Img.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.intro2_Img, "RGBA", 1))

			# Displaying everything for First intro screen
			self.displayImage(self.intro2_Tex,self.intro2_Img, 0, 0)
			self.Next2btn.drawBackground()
			self.Back1btn.drawBackground()
			self.Next2btn.drawText(self.painter, self.printer, self.printer.fontNormal)
			self.Back1btn.drawText(self.painter, self.printer, self.printer.fontNormal)

		elif self.showing == self.INTRO_SCREEN_3:
			# Getting the images ready to display
			self.intro3_Tex = gl.glGenTextures(1)
			gl.glBindTexture(gl.GL_TEXTURE_2D, self.intro3_Tex)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
			gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.intro3_Img.get_width(), self.intro3_Img.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.intro3_Img, "RGBA", 1))

			# Displaying everything for First intro screen
			self.displayImage(self.intro3_Tex,self.intro3_Img, 0, 0)
			self.Next3btn.drawBackground()
			self.Back2btn.drawBackground()
			self.Next3btn.drawText(self.painter, self.printer, self.printer.fontNormal)
			self.Back2btn.drawText(self.painter, self.printer, self.printer.fontNormal)

		elif self.showing == self.BADGE_SCREEN:
			# self.badgeScreen.draw()
			self.intro4_Tex = gl.glGenTextures(1)
			gl.glBindTexture(gl.GL_TEXTURE_2D, self.intro4_Tex)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
			gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.intro4_Img.get_width(), self.intro4_Img.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.intro4_Img, "RGBA", 1))

			# Displaying everything for First intro screen
			self.displayImage(self.intro4_Tex,self.intro3_Img, 0, 0)
			self.btnOkay.drawBackground()
			self.Back3btn.drawBackground()
			self.btnOkay.drawText(self.painter, self.printer, self.printer.fontNormal)
			self.Back3btn.drawText(self.painter, self.printer, self.printer.fontNormal)
				
		self.painter.end()
		#self.swapBuffers()
		
	def paintGL(self):
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		gl.glLoadIdentity()
		