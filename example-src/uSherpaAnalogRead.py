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

	print "uSherpaAnalogRead"

	ps = SerialPacketStream("/dev/ttyUSB0")
	ps.start()

	us = uSherpa(ps)

	# configure pin 1.5 for analog input 
 	print "Set P1.5 to ANALOG input: "  
	us.pinMode(uSherpa.PIN_1_5, uSherpa.ANALOG)
	print "-> OK"

	# performe analog read on pin 1.5
	a = us.analogRead(uSherpa.PIN_1_5);

	# convert value from analog read to volts: 
	# - assuming Vmax is 3.3V
	# - assuming max value from analog read is 1024
	v = (3.3 / 1024.0) * a

	print "-> OK: ~ volts " + `v` + " (" + `a` + ")"
	
	# reset MCU 
  	print "RESET: "  
	us.reset()
	print "-> OK"

except Exception as e:
	print traceback.format_exc()

finally:
	if not ps == None:
		ps.stop()	
