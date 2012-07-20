#!/bin/python

import time
import traceback

from array import array
from usherpa.comm import Packet, PacketStream, PacketException, PacketStreamException

print "Packet-Stream Test"

class DummyStream:

	slow	= False

	idx 	= 0

	data 	= array('B', [ 0x18, 0x01, 0x24, 0x07, 0x06, 0x22, 0x20, 0x4e, 0xc1, 0xFF, 0x24, 0x06, 0x05, 0x13, 0x03, 0x45, ])

	def write(self, b):
		print "> " + hex(b)

	def read(self):

		if self.slow:
			print "slow-read!"
			time.sleep(5)

		b = self.data[self.idx]	

		self.idx = self.idx + 1

		if self.idx >= len(self.data): 
			self.idx = 0

		return b	

s = DummyStream()

ps = PacketStream(s)

try:
	ps.start()

	p = Packet()
	p.fromByteArray(array('B', [0x24, 0x07, 0x06, 0x22, 0x20, 0x4e, 0xc1]))
	print "p: " + p.__str__()

	ps.send(p)
	r = ps.receive()

	print "r: " + r.__str__()

	r = ps.xfer(p)

	print "r: " + r.__str__()

	s.slow = True

	r = ps.xfer(p)

	print "r: " + r.__str__()

except PacketException as e:
	print e
except PacketStreamException as e:
	print e
except Exception as e:
	print traceback.format_exc()
finally:
	ps.close()
