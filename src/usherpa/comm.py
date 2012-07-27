##
# This file is part of the uSherpa Python Library project
#
# Copyright (C) 2012 Stefan Wendler <sw@kaltpost.de>
#
# The uSherpa Python  Library is free software; you can redistribute 
# it and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  uSherpa Python Library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
# 
#  You should have received a copy of the GNU Lesser General Public
#  License along with the JSherpa firmware; if not, write to the Free
#  Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
#  02111-1307 USA.  
##

'''
This file is part of the uSherpa Python Library project
'''

import time

from array import array
from threading import Thread, Lock, Condition

class PacketException(Exception):
	'''
	Exception thrown whenever someting went wrong with package
	parsing or package assembling.
	'''

	def __init__(self, value):
		''' Constructor '''
		self.value = value

	def __str__(self):
		''' String representation '''
		return repr(self.value)

class PacketStreamException(Exception):
	'''
	Exception thrown whenever someting went wrong with prcessing
	a package stream. 
	'''

	def __init__(self, value):
		''' Constructor '''
		self.value = value

	def __str__(self):
		''' String representation '''
		return repr(self.value)

class Packet:
	'''
	Representation of a packet as defined in the uSherpa protocol.
	'''

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
	
	start			= 0 

	length			= 0 

	ptype			= 0 

	data			= None

	crc				= 0 

	def __init__(self):
		''' Constructor '''

		self.clear()

	def fromFields(self, start, length, ptype, data, crc = None):
		''' Assign package content from fields '''

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
		''' Clear package content '''

		self.start 			= 0
		self.length 		= 0
		self.ptype 			= 0
		self.data 			= None
		self.crc 			= 0
		self.currFill		= 0

	def addByte(self, b):
		''' 
		Add a single byte (e.g. from a stream) to packet content. 
		Bytes are only added when the PACKET_START_x byte was received
		before.
		'''

		if self.currFill == self.PACKET_FILL_WAIT:

			if b == self.PACKET_START_OUTB or b == self.PACKET_START_INB or b == self.PACKET_START_INBEV:
				self.currFill = self.currFill + 2
				self.start 	  = b;
				self.crc      = self.crc + b;

		elif self.currFill == self.PACKET_FILL_LENGTH:

			self.length = b;
			self.crc    = self.crc + b;

			if self.length - 4 > self.PACKET_MAX_DATA:
				raise PacketException("Packet to big: was " + 
					`self.length` + ", allowd " + `self.PACKET_MAX_DATA + 4`)

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

			b = b & 0xFF
			self.crc = self.crc & 0xFF

			if b != self.crc:
				raise PacketException("CRC error: expected " + hex(self.crc) + " and got " + hex(b))

		else:
			raise PacketException("Packet already complete")

	def fromByteArray(self, pkt):
		''' Assign packet content from a byte array '''

		self.clear()

		for b in pkt:
			self.addByte(b)

	def toByteArray(self):
		''' Return packet content as byte array '''

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
		''' Calculate and return CRC of the packets current content '''

		pkt = self.toByteArray()

		newCrc = 0

		for b in pkt:
			newCrc = newCrc + b
 
		return 0xFF & (newCrc - pkt[len(pkt) - 1])

	def checkCrc(self):
		''' Compare CRC from packet content to calulated CRC. Returns True or False. '''

		return (self.crc & 0xFF == self.calcCrc())
	
	def isComplete(self):
		''' Check if packet content is complete. '''	

		return (self.currFill == self.PACKET_FILL_COMPLETE)

	def __str__(self):
		''' String representation '''
	
		pkt = None

		try:
			pkt = self.toByteArray()
		except PacketException as e:
			return e.__str__()
 				
		s = "{"

		for b in pkt: 
			s = s + hex(b) + ", "

		s = s + "}"

		return s

class PacketStream(Thread):
	''' 
	General packet stream implementation. The packet stream implementation
	is responsible for parsing packets out of a physical transport stream
	(e.g. the serial line) and to put packets on that physical transport
	stream. Packet reading from the stream is done in a reader thread.
	'''	

	stream 		= None

	sendLock	= None

	xferLock    = None

	packetAvail = None

	packet  	= None

	running 	= False

	evHandler   = None

	def __init__(self, stream):
		''' Constructor '''

		self.stream   		= stream
		self.sendLock 		= Lock()
		self.xferLock 		= Lock()
		self.packetAvail 	= Condition()

		Thread.__init__(self)

	def __del__(self):
		''' Destructor, stops the receiver thread if running '''
		self.stop()
	
	def start(self):
		''' Start the receiver thread '''

		Thread.start(self)

		while not self.running:
			print "wait for thread to startup"
			time.sleep(0.1)
			
	def stop(self):
		''' Stop the receiver thread, close the stream '''

		self.interrupt()
		self.join()
		self.stream.close()

	def send(self, pkt):
		''' 
		Send a packet blocking through the assigned stream.		
		'''
	
		if self.stream == None:
			raise PacketStreamException("No stream found!") 

		self.sendLock.acquire()
		# TODO: check if this is really needed
		self.stream.flushOutput()
		self.stream.flushInput()

		try:

			for b in pkt.toByteArray():
				self.stream.write(chr(b))

		except Exception as e:
			raise PacketStreamException(e.__str__())
		finally:
			self.sendLock.relese()

		# only works with pyserial >= 2.5
		# self.stream.write(pkt.toByteArray())

	def receive(self):
		'''
		Receive a packet blocking from the stream. If after one second
		no packet was received, a PacketStreamException will be thrown.
		'''
		
		if not self.running:
			raise PacketStreamException("Reader thread must be started") 

		self.packetAvail.acquire()

		# wait until response packet is available
		if self.packet == None or not self.packet.isComplete():	
			self.packetAvail.wait(1)

		# if packet is still not available, raise timeout exception
		if self.packet == None or not self.packet.isComplete():	
			self.packetAvail.release()
			raise PacketStreamException("Read timeout")
	
		# copy the newly received packet
		p = Packet()
		p.fromByteArray(self.packet.toByteArray())

		self.packet = None
		
		self.packetAvail.release()

		return p

	def xfer(self, pkt):
		'''
		Send a packet, wait for the response, and return the response packet.
		If after one second no response packet was received, a PacketStreamException
		will be thrown. This method is synchronized in a way, that no two callers
		could perform an xfer at the same time.
		'''

		res = None

		self.xferLock.acquire()
		
		try:
			self.send(pkt)
			res = self.receive()
		except Exception as e:
			raise PacketStreamException(e.__str__())
		finally:
			self.xferLock.release()
		
		return res

	def run(self):
		''' Overlodad run function, executed when start is called '''
	
		p = Packet()

		# byte array to convert received
		ba = array('B', [ 0 ])

		self.running = True

		while self.running:

			s = self.stream.read(Packet.PACKET_MAX_DATA + 4)

			'''
			nb = self.stream.inWaiting()

			if nb > 1:
				print "multible bytes waiting: " + `nb`
				s = self.stream.read(nb)
			else:
				s = self.stream.read()
			'''

			# timed out (since nothing to read on stream)
			if len(s) < 1:
				continue

			# pump all received to packet
			for bs in s:

				ba[0] = ord(bs) 
			
				p.addByte(bs)

				if p.isComplete():
					if not self.evHandler == None and p.start == Packet.PACKET_START_INBEV:
						# event handler registered, and event received
						ep = Packet()
						ep.fromByteArray(p.toByteArray()) 
						p.clear()
						thread.start_new_thread(self.evHandler, (ep))
					else:
						self.packetAvail.acquire()
						self.packet = Packet()
						self.packet.fromByteArray(p.toByteArray()) 
						p.clear()
						self.packetAvail.notify()
						self.packetAvail.release()

	def interrupt(self):
		''' 
		Interrupt the receiver thread. This method is normally called 
		from the desructor, or when the stop method is called.
		'''

		self.running = False
