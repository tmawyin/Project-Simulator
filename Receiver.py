import threading
import socket
import struct
import csv
from PySide.QtCore import Qt, QObject, QThread, Signal
from NetClient import *

class Receiver(QThread):
	# Receiver constructor
	def __init__(self, netclient, name = "Receiver"):
		# Call the thread's constructor
		QThread.__init__(self)
		
		# Set the thread's data
		self.name = name
		
		# Initialize the variables
		self.receiverData ={}
		self.frameValue = 0
		self.logStream = 0
		self.speed = 0.0
		self.laneDepart = 0
		self.distance = 0.0
		self.bumperTime = 0.0
		self.bumperDist = 0.0
		self.collisionTime = 0.0
		self.leadVehVel = 0.0
		# self.isTaskReady = False
		# self.isTaskCompleted = False
		# self.isTaskRecorded = False

		# Connecting to the netclient signal
		netclient.receiverDataSignal.connect(self.setReceiverVars, Qt.QueuedConnection)

		try:
			# Create a new socket, use IPv4 and UDP
			# Then bind the socket to localhost and the port
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.socket.bind(('', 1224))
			
		except socket.error as err:
			# Could not create the socket, bind it, or listen on the port.
			# Print the error message
			print "Could not create the socket:", err
			self.socket = None
	
	def setReceiverVars(self, variable):
		self.receiverData = variable
		#print "Testing Testing::::", self.receiverData

	# Runs the receiver
	def run(self):
		# Check that the socket is alive
		if self.socket is None:
			return;
					
		while True:
			# Receive the data, then check that some data was returned
			packet = self.socket.recv(256)

			if not packet: break
						
			# VARIABLE: LOG STREAM
			if len(packet) == 20:
				# Unpack the data, disregard the other bytes
				data = struct.unpack('<fffff', packet[0:20])
				self.logStream = int(data[0])
				print("Log value is: %d" %self.logStream)
			
				# # Check the data
				# if data == 1 and self.isTaskReady == False:
				# 	self.isTaskCompleted = False
				# 	self.isTaskRecorded = False
				# 	self.isTaskReady = True
				# 	#print("Data is 1")
				# else:
				# 	self.isTaskReady = False
				# 	#print("Data is 0")
			
			# VARIABLE: FRAME NUMBER	
			elif len(packet) == 4:
				# Unpack the data (integer type)
				data = struct.unpack('<i', packet)
				self.frameValue = data
				print("Frame value is: %d" %self.frameValue)

				# if self.isTaskCompleted == True and self.isTaskRecorded == False:
				# 	# Set the last frame value
				# 	self.lastTaskFrame = data[0]
				# 	self.isTaskRecorded = True
				# 	print("Set frame")

			# VARIABLE: AVERAGE SPEED
			elif len(packet) == 8:
				data = struct.unpack('<ff', packet[0:8])
				self.speed = float(data[0]) 
				print('Speed is: %f' %self.speed)

			# VARIABLE: FOLLOW INFO
			elif len(packet) == 36:
				data = struct.unpack('<fffffffff', packet[0:36])
				self.distance = float(data[1])
				self.bumperTime = float(data[2])
				self.bumperDist = float(data[3])
				self.collisionTime = float(data[4])
				self.leadVehVel = float(data[5])
				print('Lead distance is: %f' %self.distance)
		
			# VARIABLE: LANE DEPARTURE
			elif len(packet) == 12:
				data = struct.unpack('<fff', packet[0:12])
				self.laneDepart = float(data[0])
				print('Lane departure is: %f' %self.laneDepart)

			# Save variables to file
			with open('ReceiverData.csv','ab') as csvfile:
				toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
				toFile.writerow(['%d'%self.frameValue,'%d'%self.laneDepart,'%f'%self.speed,'%f'%self.laneDepart,'%f'%self.distance,'%f'%self.bumperTime,'%f'%self.bumperDist,'%f'%self.collisionTime,'%f'%self.leadVehVel])

		# Clean up
		self.socket.close()
		self.socket = None

# ---OLD CODE TO RUN RECEIVER ON ITS OWN---
# thread = Receiver();
# thread.start()

