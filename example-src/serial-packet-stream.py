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
import time

from usherpa.comm import *
from usherpa.serialcomm import *

T  = 0.5
ps = None

try:

	ps = SerialPacketStream("/dev/ttyUSB0")
	ps.start()

	# xfer packet for PIN FUNCTION digital p1.0 (LED on Launchpad) 
	pcfg = Packet()
	pcfg.fromFields(0x24, 0x06, 0x04, array('B', [ 0x10, 0x03 ] ));

	# set p1.0 to high 
	phi = Packet()
	phi.fromFields(0x24, 0x06, 0x05, array('B', [ 0x10, 0x01 ] ));

	# set p1.0 to low 
	plo = Packet()
	plo.fromFields(0x24, 0x06, 0x05, array('B', [ 0x10, 0x00 ] ));

	print "Setup Pin 1.0"
	ps.xfer(pcfg)

	while True:
		try:
			print "Pin 1.0 ON"
			ps.xfer(phi)
			time.sleep(T);
			print "Pin 1.0 OFF"
			ps.xfer(plo)
			time.sleep(T);
		except KeyboardInterrupt:
			break
		except: 
			print traceback.format_exc()
			break

except Exception as e:
	print traceback.format_exc()

finally:
	ps.stop()	
