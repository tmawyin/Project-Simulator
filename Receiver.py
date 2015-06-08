import threading
import socket
import struct
import csv
import numpy as np
from PySide.QtCore import Qt, QObject, QThread, Signal
from NetClient import *

class Receiver(QThread):
	terminateScreen = Signal()
	
	# Receiver constructor
	def __init__(self, netclient, parID_Signal, name = "Receiver"):
		# Call the thread's constructor
		QThread.__init__(self)
		
		# Set the thread's data
		self.name = name
		
		# Initialize the variables
		self.netFileData = []
		self.recFileData = []
		self.receiverData ={"FRAME":'0',"GAZE":'0',"OneCount":'0',"ZeroCount":'0',"MaxCount":'0',"WarnCount":'0',"DangerCount":'0',"RstCount":'0',"GlanceCount":'0',"LowCount":'0'}
		self.frameValue = 0
		self.logStream = 0
		self.laneDepart = 0.0
		self.laneDeviation = 0.0
		
		self.distance = 0.0
		self.bumperTime = 0.0
		self.bumperDist = 0.0
		self.collisionTime = 0.0
		self.leadVehVel = 0.0

		self.numCollision = 0
		self.chassisAccel = 0.0

		self.participantID = 'Default'

		# Connecting to the netclient signal
		netclient.receiverDataSignal.connect(self.setReceiverVars, Qt.QueuedConnection)
		parID_Signal.connect(self.setReceiverParID,Qt.QueuedConnection)

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
		self.netFileData.append(['%s'%self.receiverData['FRAME'],'%s'%self.receiverData['GAZE'],'%s'%self.receiverData['OneCount'],'%s'%self.receiverData['ZeroCount'],'%s'%self.receiverData['MaxCount'],'%s'%self.receiverData['WarnCount'],'%s'%self.receiverData['DangerCount'],'%s'%self.receiverData['RstCount'],'%s'%self.receiverData['LowCount']])
		# with open('%s_net.csv'%self.participantID,'ab') as csvfile:
		# 	toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
		# 	toFile.writerow(['%s'%self.receiverData['FRAME'],'%s'%self.receiverData['GAZE'],'%s'%self.receiverData['OneCount'],'%s'%self.receiverData['ZeroCount'],'%s'%self.receiverData['MaxCount'],'%s'%self.receiverData['WarnCount'],'%s'%self.receiverData['DangerCount'],'%s'%self.receiverData['RstCount'],'%s'%self.receiverData['LowCount']])

	def setReceiverParID(self, variable):
		self.participantID = variable

	# Receiver destructor
	def exitAll():
		QThread.quit()
		self.quit()

	# Runs the receiver
	def run(self):
		# Check that the socket is alive
		if self.socket is None:
			return;
		
		# Keeps track of the packages received
		pkgCounter = 0

		while True:
			# Receive the data, then check that some data was returned
			packet = self.socket.recv(256)

			if not packet: break
						
			# VARIABLE: LOG STREAM
			if len(packet) == 20:
				# Unpack the data, disregard the other bytes
				data = struct.unpack('<fffff', packet[0:20])
				self.logStream = int(data[0])
				pkgCounter += 1
				# print("Log value is: %d" %self.logStream)

				# Use to show the postdrive screen	
				if self.logStream == 9:
					# Saving to files
					np.savetxt('../../participantData/Gamification/%s_data.csv'%self.participantID, np.asarray(self.recFileData), delimiter=",", fmt="%s")
					np.savetxt('../../participantData/Gamification/%s_net.csv'%self.participantID, np.asarray(self.netFileData), delimiter=",", fmt="%s")
					self.terminateScreen.emit()
					self.exitAll()
					break

			# VARIABLE: FRAME NUMBER	
			elif len(packet) == 4:
				# Unpack the data (integer type)
				data = struct.unpack('<i', packet)
				self.frameValue = data
				pkgCounter += 1
				# print("Frame value is: %d" %self.frameValue)

			# VARIABLE: NUMBER COLLISIONS
			elif len(packet) == 8:
				data = struct.unpack('<ff', packet[0:8])
				self.numCollision = int(data[0]) 
				# print('Num of Collisions: %d' %self.numCollision)

			# VARIABLE: FOLLOW INFO
			elif len(packet) == 36:
				data = struct.unpack('<fffffffff', packet[0:36])
				self.distance = float(data[1])
				self.bumperTime = float(data[2])
				self.bumperDist = float(data[3])
				self.collisionTime = float(data[4])
				self.leadVehVel = float(data[5])
				pkgCounter += 1
				# print('Lead distance is: %f' %self.distance)
		
			# VARIABLE: LANE DEVIATION
			elif len(packet) == 16:
				data = struct.unpack('<ffff', packet[0:16])
				self.laneDeviation = float(data[1])
				pkgCounter += 1
				# print('Lane deviation is: %f' %self.laneDeviation)

			# VARIABLE: LANE DEPARTURE
			elif len(packet) == 24:
				data = struct.unpack('<ffffff', packet[0:24])
				self.laneDepart = float(data[0])
				# print('Lane departure is: %f' %self.laneDepart)			
			
			# VARIABLE: ACCELERATION
			elif len(packet) == 12:
				data = struct.unpack('<fff', packet[0:12])
				self.chassisAccel = float(data[0])
				pkgCounter += 1
				# print('Acceleration x: %f' %self.chassisAccel)

			# Save variables to file
			if pkgCounter == 5:
				self.recFileData.append(['%d'%self.frameValue,'%d'%self.logStream,'%d'%self.numCollision,'%f'%self.laneDepart,'%f'%self.laneDeviation,'%f'%self.distance,'%f'%self.bumperTime,'%f'%self.bumperDist,'%f'%self.collisionTime,'%f'%self.leadVehVel,'%f'%self.chassisAccel])
				# with open('%s_data.csv'%self.participantID,'ab') as csvfile:
				# 	toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
				# 	toFile.writerow(['%d'%self.frameValue,'%d'%self.logStream,'%d'%self.numCollision,'%f'%self.laneDepart,'%f'%self.laneDeviation,'%f'%self.distance,'%f'%self.bumperTime,'%f'%self.bumperDist,'%f'%self.collisionTime,'%f'%self.leadVehVel,'%f'%self.chassisAccel])#,'%s'%self.receiverData['FRAME'],'%s'%self.receiverData['GAZE'],'%s'%self.receiverData['OneCount'],'%s'%self.receiverData['ZeroCount'],'%s'%self.receiverData['MaxCount'],'%s'%self.receiverData['WarnCount'],'%s'%self.receiverData['DangerCount'],'%s'%self.receiverData['RstCount'],'%s'%self.receiverData['LowCount']])
				pkgCounter = 0

		# Clean up
		self.socket.close()
		self.socket = None

# ---OLD CODE TO RUN RECEIVER ON ITS OWN---
# thread = Receiver();
# thread.start()

