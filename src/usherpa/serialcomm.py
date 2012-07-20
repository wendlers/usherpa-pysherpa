import serial

from usherpa.comm import *

class SerialPacketStream(PacketStream):

	def __init__(self, port, speed = 9600):
		print "init serial"
		serStream = serial.Serial()
		serStream.port 		= port
		serStream.speed 	= speed
		serStream.timeout 	= 1
		serStream.open()
		PacketStream.__init__(self, serStream)

#	def __del__(self):
#		PacketStream.__del__(self)

