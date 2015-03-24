import optparse
import smcoredata
import sys
import csv

from PySide.QtCore import QObject, QThread, Signal

sys.path.append('C:\Users\jxie\MyProjects\coredata-3.2.2.67479\pycoredata-3.4')

class NetClient(QThread):
	# The signals
	glanceWarningSignal = Signal()
	glanceDangerSignal = Signal()
	glanceResetSignal = Signal()
	# Signal to send data to the receiver code
	receiverDataSignal = Signal(object)

	# Constructor
	def __init__(self, name = "NetClient"):

		# Call the thread's constructor
		QThread.__init__(self)

		# Initialize the net client
		self.OnOff = False
		self.glance = []
		self.frame = []
		# Variables to keep track of glance counts
		self.oneCount = 0
		self.zeroCount = 0
		self.maxOnes = 0
		self.warnCount = 0
		self.dangerCount = 0
		self.resetCount = 0
		self.duration = []
		self.listOfDict = []
		
		# Not sure if this is going to work. This might not even be used...
		self.usage = __doc__
		self.parser = optparse.OptionParser(self.usage)
		self.options, self.args = self.parser.parse_args()
		
	def handleEngineOutputData(self, output_data, fromAddr):
		# Replace this code with your own
		#print output_data

		wout = open("faceData_write", "at")
		wout.write(output_data)
		wout.write("\n")
		wout.close()

	# Apply sub-fixation threshold
	def count(self, oneCount, zeroCount):
		# Keep current glance count if less than 50 ms off display
		if (oneCount != 0) & (zeroCount <= 3):
			print "stay"
			#pass
			
		# Reset glance count if more than 50 ms off display
		elif zeroCount == 4:
			# Keepts trakc of max number of ones prior to the zero
			self.maxOnes = oneCount
			# Resetting all values
			oneCount = 0
			zeroCount = 0
			# Resetting the glance warning/danger signal
			self.glanceResetSignal.emit()
		else:
			zeroCount
		
		return oneCount, zeroCount
		
	def isSurface(self, dictValue):
		# Saving the frame number
		self.frame.append(dictValue['FRAME_NUM'])
		#  If "SURFACE" value is reached increase oneCount and set zeroCount to 0
		if dictValue['GAZE_ITEM_NAME'] == 'Surface':
			self.glance.append(1)
			self.oneCount += 1
			self.zeroCount = 0
			self.oneCount, self.zeroCount = self.count(self.oneCount,self.zeroCount)
		else:
			self.glance.append(0)
			self.zeroCount += 1
			self.oneCount, self.zeroCount = self.count(self.oneCount,self.zeroCount)

		if self.maxOnes > 0:
			self.duration.append(self.maxOnes)


	def receiveEngineOutputData(self):
		buffer = smcoredata.VectorUInt8();
		fromAddr = smcoredata.InetAddress();
		input_socket = smcoredata.DatagramSocket(smcoredata.DEFAULT_PORT_NUMBER);
		# print smcoredata.DEFAULT_PORT_NUMBER

		# Save variables to file - header
		with open('GlancesNetclient.csv','ab') as csvfile:
			toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
			toFile.writerow(["Frame Number","Gaze","One Counter","Zero Counter","Max Counter","Warn Counter","Danger Counter","Reset Counter"])

		while True:
			buffer.clear();

			input_socket.receiveDatagram(buffer, fromAddr);
			pos = 0;

			# Extract all the objects from the buffer
			while pos < buffer.size():
				self.OnOff = True
				# Check for an EngineOutputData object in the buffer
				serializable, pos = smcoredata.SerializableFactory.newObject(buffer, pos)

				# Checking if we recived data of the type we need
				if serializable != None and serializable.objectID() == smcoredata.EngineOutputData.ENGINE_OUTPUT_DATA_ID:
					# Converts packet to string in order to handle it properly
					string_Val = str(serializable)
					# Saving information to file
					#handleEngineOutputData(string_Val, fromAddr)
					# Converts and append data to a dictionary
					ToDict = dict(item.split(":") for item in string_Val.split(","))
					#print ToDict
					self.listOfDict.append(ToDict)
					# Checking if the glance is "Surface" or not
					self.isSurface(ToDict)
					#print "oneCount:", self.oneCount
					#print "duration:", self.duration
					#print "zeroCount:", self.zeroCount

				else:
					print "\nUnrecognised packet received, header id: %d\n" % ord(buffer[0])
			
				if self.oneCount >= 120 and self.oneCount <= 150:
					self.warnCount += 1
					self.resetCount = 0
					self.dangerCount = 0
					self.glanceWarningSignal.emit()
				elif self.oneCount > 150:
					self.dangerCount += 1
					self.resetCount = 0
					self.warnCount = 0
					self.glanceDangerSignal.emit()
				else:
					self.resetCount +=1
					self.warnCount = 0
					self.dangerCount = 0
					self.glanceResetSignal.emit()
			
				# Save variables to file
				with open('GlancesNetclient.csv','ab') as csvfile:
					toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
					toFile.writerow(['%s'%ToDict['FRAME_NUM'],'%s'%ToDict['GAZE_ITEM_NAME'],'%d'%self.oneCount,'%d'%self.zeroCount,'%d'%self.maxOnes,'%d'%self.warnCount,'%d'%self.dangerCount,'%d'%self.resetCount])

				# Creating a dictionary to pass to the receiver
				var ={"FRAME":ToDict['FRAME_NUM'],"GAZE":ToDict['GAZE_ITEM_NAME'],"OneCount":self.oneCount,"ZeroCount":self.zeroCount,"MaxCount":self.maxOnes,"WarnCount":self.warnCount,"DangerCount":self.dangerCount,"RstCount":self.resetCount}
				self.receiverDataSignal.emit(var)

			# Breaking the loop if no data: WARNING - This causes problems
			#if buffer.size() == 0:
			#	break
				

		# Should account for final glances
		if self.oneCount > 0:
			self.maxOnes = self.oneCount
			self.duration.append(self.maxOnes)
		
	def run(self):
		self.receiveEngineOutputData()
		