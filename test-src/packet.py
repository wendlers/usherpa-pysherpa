#!/bin/python

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

