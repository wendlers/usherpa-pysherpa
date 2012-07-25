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

import traceback

from usherpa.api import *
from usherpa.serialcomm import *

# Searial Packet stream instance
ps = None

try:

	print "uSherpaDigitalRead"

	ps = SerialPacketStream("/dev/ttyUSB0")
	ps.start()

	us = uSherpa(ps)

	# configure pin 1.3 (internal button on Launchpad) for input 
 	print "Set P1.3 to INPUT: "  
	us.pinMode(uSherpa.PIN_1_3, uSherpa.INPUT)
	print "-> OK"

	# configure pin 2.3 for input with PULLDOWN 
 	print "Set P2.3 to INPUT-PULLDOWN: "  
	us.pinMode(uSherpa.PIN_2_3, uSherpa.PULLDOWN)
	print "-> OK"

	# configure pin 2.4 for input with PULLUP 
 	print "Set P2.4 to INPUT-PULLUP: "  
	us.pinMode(uSherpa.PIN_2_4, uSherpa.PULLUP)
	print "-> OK"

	# read pin 1.3 until state changed form high to low
 	print "Read P1.3 DIGITAL (wait for button press): "
	while us.digitalRead(uSherpa.PIN_1_3) == uSherpa.HIGH:
		pass
	print "-> OK"

	# read pin 2.3 until state changed form low to hight
 	print "Read P2.3 DIGITAL (wait for button press): "
	while us.digitalRead(uSherpa.PIN_2_3) == uSherpa.LOW:
		pass
	print "-> OK"

	# read pin 2.4 until state changed form hight to low
 	print "Read P2.4 DIGITAL (wait for button press): "
	while us.digitalRead(uSherpa.PIN_2_4) == uSherpa.HIGH:
		pass
	print "-> OK"

	# reset MCU 
  	print "RESET: "  
	us.reset()
	print "-> OK"

except Exception as e:
	print traceback.format_exc()

finally:
	if not ps == None:
		ps.stop()	
