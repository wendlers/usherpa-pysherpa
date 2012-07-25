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
