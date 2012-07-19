
from array import array

class PacketException(Exception):

	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


class Packet:

	PACKET_MAX_DATA 		= 32

	PACKET_START_OUTB		= 0x24

	PACKET_START_INB 		= 0x2b
	
	PACKET_START_INBEV		= 0x21

	PACKET_FILL_WAIT 		= 0

	PACKET_FILL_START 		= 1
	
	PACKET_FILL_LENGTH		= 2
	
	PACKET_FILL_TYPE 		= 3
	
	PACKET_FILL_DATA 		= 4
	
	PACKET_FILL_CRC 		= 5

	PACKET_FILL_COMPLETE 	= 6
	
	currFill 		= 0
	
	start	= 0 

	length	= 0 

	ptype	= 0 

	data	= None

	crc		= 0 

	def __init__(self):

			self.clear()

	def fromFields(self, start, length, ptype, data, crc = None):

		self.clear()

		self.start 	= start
		self.length = length
		self.ptype 	= ptype
		self.data 	= data

		self.currFill = self.PACKET_FILL_COMPLETE

		self.crc = crc

		if crc == None:
			self.crc = self.calcCrc()
		elif not self.checkCrc():
			raise PacketException("CRC error")

	def clear(self):

		self.start 			= 0
		self.length 		= 0
		self.ptype 			= 0
		self.data 			= None
		self.crc 			= 0
		self.currFill		= 0

	def addByte(self, b):

		if self.currFill == self.PACKET_FILL_WAIT:

			if b == self.PACKET_START_OUTB or b == self.PACKET_START_INB or b == self.PACKET_START_INBEV:
				self.currFill = self.currFill + 2
				self.start 	  = b;
				self.crc      = self.crc + b;

		elif self.currFill == self.PACKET_FILL_LENGTH:

			self.length = b;
			self.crc    = self.crc + b;

			if self.length - 4 > self.PACKET_MAX_DATA:
				raise PacketException("Packet to big: was " + `length` + ", allowd " + `self.PACKET_MAX_DATA + 4`)

			if self.length - 4 > 0:
				self.data = array('B')

			self.currFill = self.currFill + 1

		elif self.currFill == self.PACKET_FILL_TYPE:

			self.ptype 	  = b;
			self.crc   	  = self.crc + b;
			self.currFill = self.currFill + 1

			if self.data == None:
				self.currFill = self.currFill + 1

		elif self.currFill == self.PACKET_FILL_DATA:

			if not self.data == None: 

				self.data.append(b)
				self.crc = self.crc + b;

				if len(self.data) == self.length - 4:
					self.currFill = self.currFill + 1

		elif self.currFill == self.PACKET_FILL_CRC:

			self.currFill = self.currFill + 1

			if b != self.crc:
				raise PacketException("CRC error: expected " + `crc` + " and got " + `b`)

		else:
			raise PacketException("Packet already complete")

	def fromByteArray(self, pkt):
		self.clear()

		for b in pkt:
			self.addByte(b)

	def toByteArray(self):

		if not self.isComplete():
			raise PacketException("Incompelte packet")

		if self.length > 4 and (self.data == None or not len(self.data) == self.length - 4):
			raise PacketException("Invalid packet")

		pkt = array('B')

		pkt.append(self.start)
		pkt.append(self.length)
		pkt.append(self.ptype)

		if not self.data ==  None:

			for b in self.data:
				pkt.append(b)			

		if self.crc == None:
			pkt.append(0)
		else:
			pkt.append(self.crc)

		return pkt

	def calcCrc(self):

		pkt = self.toByteArray()

		newCrc = 0

		for b in pkt:
			newCrc = 0xFF & (newCrc + b)
 
		return (newCrc - pkt[len(pkt) - 1])

	def checkCrc(self):

		return (self.crc == self.calcCrc())
	
	def isComplete(self):
	
		return (self.currFill == self.PACKET_FILL_COMPLETE)

	def __str__(self):
		
		pkt = None

		try:
			pkt = self.toByteArray()
		except PacketException as e:
			return e.value
 				
		s = "{"

		for b in pkt: 
			s = s + hex(b) + ", "

		s = s + "}"

		return s
