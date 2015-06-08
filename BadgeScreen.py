from PySide import QtCore, QtGui, QtOpenGL
import OpenGL.GL as gl
import pygame
from Printer import Printer
import numpy as np

class BadgeScreen():
	def __init__(self, width, height, printer):
		# Set the screen attributes
		self.width = width
		self.height = height
		self.printer = printer
		self.numDrives = 0
		self.totalBadges = []
		self.numBadges = 0
		self.avaText = 0

		# Position of the badges
		self.positionX = [1223, 1406, 1592]
		self.positionY = [307, 545, 784]

		self.toWrite = ["Well Done!", "Keep it up!","Nicely Done!","Better luck next time!"]

		self.roadEye = [0,0,0]
		self.safeRespond = [0,0,0]
		self.laneKeeper = [0,0,0]

		# Avatar position
		self.avatarX = 797
		self.avatarY = 313
		
		# Load the images
		# Banner:
		self.bannerImg = pygame.image.load("../../images/wireframe_badgebanner.png")
		self.bannerTex = 0
		# Firework:
		self.fireImg = pygame.image.load("../../images/wireframe_fireworks.png")
		self.fireTex = 0
		# Stars:
		self.starImg = pygame.image.load("../../images/wireframe_stars.png")
		self.starTex = 0
		# Box
		self.boxImg = pygame.image.load("../../images/wireframe_msgbox.png")
		self.boxTex = 0

		# Grey No Drive Badge:
		self.greyBadgeImg = pygame.image.load("../../images/badge_default.png")
		self.greyBadgeTex = 0

		# Grey No Badge:
		self.greyNoBadgeImg = pygame.image.load("../../images/badges_null1.png")
		self.greyNoBadgeTex = 0

		# Road Eye Badge:
		self.roadEyeImg1 = pygame.image.load("../../images/badges_eyes1.png")
		self.roadEyeTex1 = 0
		self.roadEyeImg2 = pygame.image.load("../../images/badges_eyes2.png")
		self.roadEyeTex2 = 0
		self.roadEyeImg3 = pygame.image.load("../../images/badges_eyes3.png")
		self.roadEyeTex3 = 0

		# Safe Respond Badge:
		self.safeRespondImg1 = pygame.image.load("../../images/badges_safe1.png")
		self.safeRespondTex1 = 0
		self.safeRespondImg2 = pygame.image.load("../../images/badges_safe2.png")
		self.safeRespondTex2 = 0
		self.safeRespondImg3 = pygame.image.load("../../images/badges_safe3.png")
		self.safeRespondTex3 = 0

		# Lane Keeper Badges
		self.laneKeeperImg1 = pygame.image.load("../../images/badges_lane1.png")
		self.laneKeeperTex1 = 0
		self.laneKeeperImg2 = pygame.image.load("../../images/badges_lane2.png")
		self.laneKeeperTex2 = 0
		self.laneKeeperImg3 = pygame.image.load("../../images/badges_lane3.png")
		self.laneKeeperTex3 = 0

		# Text Badge
		self.eyesImg = pygame.image.load("../../images/wireframes_eyeslabel.png")
		self.eyesTex = 0
		self.respondImg = pygame.image.load("../../images/wireframes_safelabel.png")
		self.respondTex = 0
		self.laneImg = pygame.image.load("../../images/wireframes_lanelabel.png")
		self.laneTex = 0

		self.roadEyeImg = [self.greyBadgeImg for x in range(3)]
		self.safeRespondImg = self.roadEyeImg
		self.laneKeeperImg = self.roadEyeImg
		
	def init(self, parID, gender):
		# Opening and loading the file
		self.parID = parID
		self.gender = gender
		driver = self.parID.split("_")
		driverData = np.genfromtxt('../../participantData/Gamification/%s_drives.csv'%driver[0], delimiter=',')
		if len(driverData.shape) == 1:
			driverData = np.array([driverData])
		driverData = np.delete(driverData,0,0)

		# Need to check the size of the file <=3
		if driverData.shape[0] > 3:
			self.numDrives = 3
		else:
			self.numDrives = driverData.shape[0]

		for i in range(self.numDrives):
			self.numBadges = 0
			# road eyes badge - 0:high; 1:medium
			if driverData[i,0] <= 5 or driverData[i,1] <= 10:
				self.roadEyeImg[i] = self.roadEyeImg1
				self.roadEye[i] =1
				self.numBadges += 1
			elif (driverData[i,0] <= 10 and driverData[i,0] > 5) or (driverData[i,1] <= 20 and driverData[i,1] > 10):
				self.roadEyeImg[i] = self.roadEyeImg2
				self.roadEye[i] = 2
				self.numBadges += 1
			elif (driverData[i,0] <= 15 and driverData[i,0] > 10) or (driverData[i,1] <= 30 and driverData[i,1] > 20):
				self.roadEyeImg[i] = self.roadEyeImg3
				self.roadEye[i] = 3
				self.numBadges += 1
			else:
				self.roadEye[i] = 4
				self.roadEyeImg[i] = self.greyNoBadgeImg

			# safe responder badge
			if driverData[i,4] <= 0:
				self.safeRespondImg[i] = self.safeRespondImg1
				self.safeRespond[i] = 1
				self.numBadges += 1
			elif driverData[i,4] == 1: #or driverData[i,4] == 3:
				self.safeRespondImg[i] = self.safeRespondImg2
				self.safeRespond[i] = 2
				self.numBadges += 1
			elif driverData[i,4] == 2 or driverData[i,4] == 3:
				self.safeRespondImg[i] = self.safeRespondImg3
				self.safeRespond[i] = 3
				self.numBadges += 1
			else:
				self.safeRespond[i] = 4
				self.safeRespondImg[i] = self.greyNoBadgeImg

			# lane keeper badge
			if driverData[i,3] == 0:
				self.laneKeeperImg[i] = self.laneKeeperImg1
				self.laneKeeper[i] = 1
				self.numBadges += 1
			elif driverData[i,3] == 1:
				self.laneKeeperImg[i] = self.laneKeeperImg2
				self.laneKeeper[i] = 2
				self.numBadges += 1
			elif driverData[i,3] == 2:
				self.laneKeeperImg[i] = self.laneKeeperImg3
				self.laneKeeper[i] = 3
				self.numBadges += 1
			else:
				self.laneKeeper[i] = 4
				self.laneKeeperImg[i] = self.greyNoBadgeImg

			self.totalBadges.append(self.numBadges)
		
		'''TESTING'''
		# self.laneKeeper[2] = 4
		# self.safeRespond[2] = 4
		# self.roadEye[2] = 4
		# self.numBadges = 0

		# Avatar pictures
		if self.gender == 0:
			self.avatar1Img = pygame.image.load("../../images/wireframes_m1.png")
			self.avatar1Tex = 0
			self.avatar2Img = pygame.image.load("../../images/wireframes_m2.png")
			self.avatar2Tex = 0
			self.avatar3Img = pygame.image.load("../../images/wireframes_m3.png")
			self.avatar3Tex = 0
		elif self.gender == 1:
			self.avatar1Img = pygame.image.load("../../images/wireframes_f1.png")
			self.avatar1Tex = 0
			self.avatar2Img = pygame.image.load("../../images/wireframes_f2.png")
			self.avatar2Tex = 0
			self.avatar3Img = pygame.image.load("../../images/wireframes_f3.png")
			self.avatar3Tex = 0

		# Banner
		self.bannerTex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.bannerTex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.bannerImg.get_width(), self.bannerImg.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.bannerImg, "RGBA", 1))

		# Box
		self.boxTex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.boxTex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.boxImg.get_width(), self.boxImg.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.boxImg, "RGBA", 1))

		# Avatar
		self.avatar1Tex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.avatar1Tex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.avatar1Img.get_width(), self.avatar1Img.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.avatar1Img, "RGBA", 1))
		self.avatar2Tex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.avatar2Tex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.avatar2Img.get_width(), self.avatar2Img.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.avatar2Img, "RGBA", 1))
		self.avatar3Tex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.avatar3Tex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.avatar3Img.get_width(), self.avatar3Img.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.avatar3Img, "RGBA", 1))

		# Firework
		self.fireTex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.fireTex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.fireImg.get_width(), self.fireImg.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.fireImg, "RGBA", 1))

		# Stars
		self.starTex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.starTex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.starImg.get_width(), self.starImg.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.starImg, "RGBA", 1))

		# Grey Badge
		self.greyBadgeTex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.greyBadgeTex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.greyBadgeImg.get_width(), self.greyBadgeImg.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.greyBadgeImg, "RGBA", 1))
		# Grey NO Badge
		self.greyNoBadgeTex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.greyNoBadgeTex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.greyNoBadgeImg.get_width(), self.greyNoBadgeImg.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.greyNoBadgeImg, "RGBA", 1))

		# Road Eye Badges
		self.roadEyeTex1 = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.roadEyeTex1)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.roadEyeImg1.get_width(), self.roadEyeImg1.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.roadEyeImg1, "RGBA", 1))
		self.roadEyeTex2 = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.roadEyeTex2)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.roadEyeImg2.get_width(), self.roadEyeImg2.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.roadEyeImg2, "RGBA", 1))
		self.roadEyeTex3 = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.roadEyeTex3)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.roadEyeImg3.get_width(), self.roadEyeImg3.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.roadEyeImg3, "RGBA", 1))

		# Safe Response Badges
		self.safeRespondTex1 = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.safeRespondTex1)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.safeRespondImg1.get_width(), self.safeRespondImg1.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.safeRespondImg1, "RGBA", 1))
		self.safeRespondTex2 = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.safeRespondTex2)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.safeRespondImg2.get_width(), self.safeRespondImg2.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.safeRespondImg2, "RGBA", 1))
		self.safeRespondTex3 = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.safeRespondTex3)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.safeRespondImg3.get_width(), self.safeRespondImg3.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.safeRespondImg3, "RGBA", 1))

		# Lane Keeper Badges
		self.laneKeeperTex1 = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.laneKeeperTex1)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.laneKeeperImg1.get_width(), self.laneKeeperImg1.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.laneKeeperImg1, "RGBA", 1))
		self.laneKeeperTex2 = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.laneKeeperTex2)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.laneKeeperImg2.get_width(), self.laneKeeperImg2.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.laneKeeperImg2, "RGBA", 1))
		self.laneKeeperTex3 = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.laneKeeperTex3)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.laneKeeperImg3.get_width(), self.laneKeeperImg3.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.laneKeeperImg3, "RGBA", 1))

		# Badges Text 
		self.eyesTex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.eyesTex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.eyesImg.get_width(), self.eyesImg.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.eyesImg, "RGBA", 1))
		self.respondTex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.respondTex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.respondImg.get_width(), self.respondImg.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.respondImg, "RGBA", 1))
		self.laneTex = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.laneTex)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.laneImg.get_width(), self.laneImg.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pygame.image.tostring(self.laneImg, "RGBA", 1))
		
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
		
	def displayImageCentered(self, texture, image, x, y, width, height):
		img_x = 0
		img_y = 0
		
		# Calculate the x
		if( width > 0 ):
			img_x = (width/2.0) - (image.get_width() / 2.0)
		
		# Calculate the y
		if( height > 0 ):
			img_y = (height/2.0) - (image.get_height() / 2.0)
			
		# Display the image
		self.displayImage(texture, image, x + img_x, y + img_y)
		
	def draw(self, painter):
		# Banner
		self.displayImageCentered(self.bannerTex, self.bannerImg, 0, 110, self.width, 0)
		
		# Badge Text
		self.displayImage(self.eyesTex,self.eyesImg, 1395, 265)
		self.displayImage(self.respondTex,self.respondImg, 1349, 503)
		self.displayImage(self.laneTex,self.laneImg, 1379, 741)

		# Avatar
		if self.numDrives == 1:
			self.displayImage(self.avatar1Tex,self.avatar1Img, self.avatarX, self.avatarY)
			self.avaText = 1
		if self.numDrives == 2 and self.totalBadges[1] >=1:
			self.displayImage(self.avatar2Tex,self.avatar2Img, self.avatarX, self.avatarY)
			self.avaText = 2
		elif self.numDrives == 2 and self.totalBadges[1] < 1:
			self.displayImage(self.avatar1Tex,self.avatar1Img, self.avatarX, self.avatarY)
			self.avaText = 1
		if self.numDrives == 3 and self.totalBadges[2] >= 1 and self.totalBadges[1] >= 1:
			self.displayImage(self.avatar3Tex,self.avatar3Img, self.avatarX-20, self.avatarY)
			self.avaText = 3
		elif self.numDrives == 3 and self.totalBadges[2] >= 1 and self.totalBadges[1] < 1:
			self.displayImage(self.avatar2Tex,self.avatar2Img, self.avatarX, self.avatarY)
			self.avaText = 2
		elif self.numDrives == 3 and self.totalBadges[2] < 1 and self.totalBadges[1] < 1:
			self.displayImage(self.avatar1Tex,self.avatar1Img, self.avatarX, self.avatarY)
			self.avaText = 1

		# self.avaText = 3
		# Badges
		for i in range(len(self.roadEye)):
			if self.roadEye[i] == 1:
				self.displayImage(self.roadEyeTex1,self.roadEyeImg[i], self.positionX[i], self.positionY[0])
			elif self.roadEye[i] == 2:
				self.displayImage(self.roadEyeTex2,self.roadEyeImg[i], self.positionX[i], self.positionY[0])
			elif self.roadEye[i] == 3:
				self.displayImage(self.roadEyeTex3,self.roadEyeImg[i], self.positionX[i], self.positionY[0])
			elif self.roadEye[i] == 4:
				self.displayImage(self.greyNoBadgeTex,self.roadEyeImg[i], self.positionX[i], self.positionY[0])
			else:
				self.displayImage(self.greyBadgeTex,self.roadEyeImg[i], self.positionX[i], self.positionY[0])

		for i in range(len(self.safeRespond)):
			if self.safeRespond[i] == 1:
				self.displayImage(self.safeRespondTex1,self.safeRespondImg[i], self.positionX[i], self.positionY[1])
			elif self.safeRespond[i] == 2:
				self.displayImage(self.safeRespondTex2,self.safeRespondImg[i], self.positionX[i], self.positionY[1])
			elif self.safeRespond[i] == 3:
				self.displayImage(self.safeRespondTex3,self.safeRespondImg[i], self.positionX[i], self.positionY[1])
			elif self.safeRespond[i] == 4:
				self.displayImage(self.greyNoBadgeTex,self.safeRespondImg[i], self.positionX[i], self.positionY[1])
			else:
				self.displayImage(self.greyBadgeTex,self.safeRespondImg[i], self.positionX[i], self.positionY[1])

		for i in range(len(self.laneKeeper)):
			if self.laneKeeper[i] == 1:
				self.displayImage(self.laneKeeperTex1,self.laneKeeperImg[i], self.positionX[i], self.positionY[2])
			elif self.laneKeeper[i] == 2:
				self.displayImage(self.laneKeeperTex2,self.laneKeeperImg[i], self.positionX[i], self.positionY[2])
			elif self.laneKeeper[i] == 3:
				self.displayImage(self.laneKeeperTex3,self.laneKeeperImg[i], self.positionX[i], self.positionY[2])
			elif self.laneKeeper[i] == 4:
				self.displayImage(self.greyNoBadgeTex,self.laneKeeperImg[i], self.positionX[i], self.positionY[2])
			else:
				self.displayImage(self.greyBadgeTex,self.laneKeeperImg[i], self.positionX[i], self.positionY[2])
		
		# Box
		self.displayImage(self.boxTex,self.boxImg, 183, 322)
		# Stars
		# self.displayImage(self.starTex,self.starImg, 501, 766)
		

		# Display the text
		if self.numDrives == 1 and self.numBadges >=1:
			# self.displayImage(self.fireTex,self.fireImg, 215, 350)
			self.printer.printText(painter, self.toWrite[0], self.printer.fontNormal_2, 347, 850, self.width, self.height)
		elif self.numDrives == 2 and self.numBadges >=1:
			# self.displayImage(self.fireTex,self.fireImg, 215, 350)
			self.printer.printText(painter, self.toWrite[1], self.printer.fontNormal_2, 347, 850, self.width, self.height)
		elif self.numDrives == 3 and self.numBadges >=1:
			# self.displayImage(self.fireTex,self.fireImg, 215, 350)
			self.printer.printText(painter, "RH badge attained!", self.printer.fontNormal_2, 280, 800, self.width, self.height)
			self.printer.printText(painter, self.toWrite[2], self.printer.fontNormal_2, 347, 850, self.width, self.height)
		elif self.numBadges == 0:
			self.printer.printText(painter, self.toWrite[3], self.printer.fontNormal_2, 235, 531, self.width, self.height)

		self.printer.printText(painter, "You collected   badges", self.printer.fontNormal_2, 240, 413, self.width, self.height)
		self.printer.printText(painter, "%d"%(self.numBadges), self.printer.fontNormal_2, 498, 413, self.width, self.height, 76,124,255)
		self.printer.printText(painter, "on this drive!", self.printer.fontNormal_2, 333, 464, self.width, self.height)


		if self.avaText == 1:
			self.printer.printText(painter, "Augmented reality", self.printer.fontNormal_2, 277, 600, self.width, self.height)
			self.printer.printText(painter, "specs and smartwatch", self.printer.fontNormal_2, 248, 653, self.width, self.height)
			self.printer.printText(painter, "- Equipped!", self.printer.fontNormal_2, 343, 703, self.width, self.height)
		elif self.avaText == 2 and self.gender == 0:
			self.printer.printText(painter, "A suit armour with", self.printer.fontNormal_2, 277, 580, self.width, self.height)
			self.printer.printText(painter, "built-in sensors and", self.printer.fontNormal_2, 260, 623, self.width, self.height)
			self.printer.printText(painter, "respectable beard", self.printer.fontNormal_2, 265, 673, self.width, self.height)
			self.printer.printText(painter, "- Equipped!", self.printer.fontNormal_2, 343, 723, self.width, self.height)
		elif self.avaText == 2 and self.gender == 1:
			self.printer.printText(painter, "A suit armour with", self.printer.fontNormal_2, 277, 580, self.width, self.height)
			self.printer.printText(painter, "built-in sensors and", self.printer.fontNormal_2, 260, 623, self.width, self.height)
			self.printer.printText(painter, "respectable boots", self.printer.fontNormal_2, 265, 673, self.width, self.height)
			self.printer.printText(painter, "- Equipped!", self.printer.fontNormal_2, 343, 723, self.width, self.height)
		elif self.avaText == 3 and self.gender ==  0:
			self.printer.printText(painter, "Exoskeleton boots", self.printer.fontNormal_2, 277, 580, self.width, self.height)
			self.printer.printText(painter, "and bulletproof cape", self.printer.fontNormal_2, 260, 623, self.width, self.height)
			self.printer.printText(painter, "- Equipped", self.printer.fontNormal_2, 320, 673, self.width, self.height)
		elif self.avaText == 3 and self.gender ==  1:
			self.printer.printText(painter, "Thermal bulletproof", self.printer.fontNormal_2, 277, 600, self.width, self.height)
			self.printer.printText(painter, "  cape - Equipped  ", self.printer.fontNormal_2, 277, 653, self.width, self.height)
