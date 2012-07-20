#!/bin/python

import time

from array import array
from usherpa.comm import Packet, PacketStream, PacketException

print "Packet-Stream Test"

class DummyStream:

	idx 	= 0

	data 	= array('B', [ 0x18, 0x01, 0x24, 0x07, 0x06, 0x22, 0x20, 0x4e, 0xc1, 0xFF, 0x24, 0x06, 0x05, 0x13, 0x03, 0x45, ])

	def write(self, b):
		print "> " + hex(b)

	def read(self):
		b = self.data[self.idx]	

		self.idx = self.idx + 1

		if self.idx >= len(self.data): 
			self.idx = 0

		print "< " + hex(b)

		return b	

s = DummyStream()

ps = PacketStream(s)

try:

	p = Packet()
	p.fromByteArray(array('B', [0x24, 0x07, 0x06, 0x22, 0x20, 0x4e, 0xc1]))
	print "p: " + p.__str__()

	ps.send(p)
	r = ps.receive()

	print "r: " + r.__str__()

except Exception as e:
	print e

# time.sleep(5)

del ps
