
import time

from array import array
from threading import Thread, RLock

from usherpa.util import synchronized

class PacketException(Exception):

	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)

class PacketStreamException(Exception):

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

class PacketStream(Thread):

	stream 		= None

	sendLock    = None

	packet  	= None

	running 	= False

	def __init__(self, stream):
		self.stream   = stream
		self.sendLock = RLock()
		Thread.__init__(self)

	def __del__(self):
		self.stop()
	
	def start(self):
		Thread.start(self)
		while not self.running:
			print "wait for thread to startup"
			time.sleep(0.1)
			
	def stop(self):
		self.interrupt()
		self.join()
		self.stream.close()

#	@synchronized("sendLock")
	def send(self, pkt):
		if self.stream == None:
			raise PacketStreamException("No stream found!") 

#		for b in pkt.toByteArray():
#			self.stream.write(b)
		self.stream.write(pkt.toByteArray())

	def receive(self):
		if not self.running:
			raise PacketStreamException("Reader thread must be started") 

		tout = 10 

		while self.packet == None or not self.packet.isComplete():	

			tout = tout - 1

			if tout == 0:
				raise PacketStreamException("Read timeout")

			time.sleep(0.25)

		p = Packet()
		p.fromByteArray(self.packet.toByteArray())

		self.packet = None
		
		return p

	def xfer(self, pkt):
		self.send(pkt)
		return self.receive()

	def run(self):

		p = Packet()

		self.running = True

		while self.running:

			s = self.stream.read()

			if len(s) != 1:
				continue

			b = array('B', [ ord(s) ])
			
#			print hex(b[0])

			p.addByte(b[0])

			if p.isComplete():
				self.packet = Packet()
				self.packet.fromByteArray(p.toByteArray()) 
				p.clear()

	def interrupt(self):
		self.running = False
