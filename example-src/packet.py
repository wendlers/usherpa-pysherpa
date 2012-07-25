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

from array import array
from usherpa.comm import Packet, PacketException

print "Packet Test"

# incomplete packet
p1 = Packet()
print "p1: " + p1.__str__()

# fill from bytes
pNull = array('B', [0x24, 0x04, 0x00, 0x28])

try:

	p1.fromByteArray(pNull)
	print "p1: " + p1.__str__() 

except PacketException as e:
	 print e

# from single parameters, including CRC
try:

	p2 = Packet()
	p2.fromFields(0x24, 0x04, 0x02, None, 0x2a)
	print "p2: " + p2.__str__()

except PacketException as e:
	 print e

# from single parameters, excluding CRC
try:

	p3 = Packet()
	p3.fromFields(0x24, 0x04, 0x02, None)
	print "p3: " + p3.__str__()

except PacketException as e:
	 print e

# again from byte array
try:

	p4 = Packet()
	p4.fromByteArray(array('B', [0x24, 0x07, 0x06, 0x22, 0x20, 0x4e, 0xc1]))
	print "p4: " + p4.__str__()

except PacketException as e:
	 print e

# consume from byte array with leading garbage
try:
	data = array('B', [ 0x18, 0x01, 0x24, 0x07, 0x06, 0x22, 0x20, 0x4e, 0xc1, 0xFF, 0x24, 0x06, 0x05, 0x13, 0x03, 0x45, ])

	p5 = Packet()

	for b in data:

		p5.addByte(b)

		if p5.isComplete() :
			print "Found packet in stream: " + p5.__str__()
			p5.clear()

except PacketException as e:
	 print e

# from single parameters, including WRONG CRC
try:
	p6 = Packet()
	p6.fromFields(0x24, 0x04, 0x02, None, 0x20)
	print "p6: " + p6.__str__()

except PacketException as e:
	 print e

