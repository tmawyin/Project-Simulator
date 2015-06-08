import sys
from PySide import QtCore, QtGui, QtOpenGL
from PySide.QtGui import QMainWindow, QPushButton, QApplication, QDesktopWidget
from OpenglScreen import OpenglScreen

class MainWindow(QMainWindow):	

	def __init__(self, parent = None):
		# Initialize the constructor
		super(MainWindow, self).__init__(parent)

		# Show the application in fullscreen
		self.showFullScreen()
		
		# Setting the frames to be full screen
		desktop = QDesktopWidget()
		width = desktop.geometry().width()
		height = desktop.geometry().height()
		
		self.openglScreen = OpenglScreen(width, height)
		self.setCentralWidget(self.openglScreen)
		
if __name__=='__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()
	app.exec_()
	
	
