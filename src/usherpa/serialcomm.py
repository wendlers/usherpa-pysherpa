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

import serial

from usherpa.comm import *

class SerialPacketStream(PacketStream):
	''' A packet stream operating on the serial line '''
	
	def __init__(self, port = "/dev/ttyACM0", speed = 19200):
		''' 
		Constructor for packet stream over serial line. 

		@param	port	(optional) serial port, default is '/dev/ttyACM0'
		@param	speed	(optional) speed for serial port, default is 19200 bauds
		'''

		serStream = serial.Serial()
		serStream.port 		= port
		serStream.baudrate 	= speed
		serStream.timeout 	= 1
		serStream.open()

		PacketStream.__init__(self, serStream)

