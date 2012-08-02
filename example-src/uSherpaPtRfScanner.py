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

from usherpa.api import *
from usherpa.serialcomm import *

# Searial Packet stream instance
ps = None

def dcConvert(dc):
	d = 0xFF / 100 * dc
	return int(d)

try:

	print "uSherpaServoPanTiltRanger"

	ps = SerialPacketStream("/dev/ttyUSB0")
	ps.start()

	us = uSherpa(ps)

	dc1 = 8.3 
	dc2 = 8.3

	# configure pin 2.0 for input 
 	print "Set P2.0 to INPUT: "  
	us.pinMode(uSherpa.PIN_2_0, uSherpa.INPUT)
	print "-> OK"

	# configure pin 1.6 (internal LED on Launchpad) for PWM output
 	print "Set P1.6 to OUTPUT: "  
	us.pinMode(uSherpa.PIN_1_6, uSherpa.PWM)
	print "-> OK"

	# set PWM period to 22000us on pin 1.6 
	print "Set P1.6 period to 22000us: "
	us.pwmPeriod(uSherpa.PIN_1_6, 22000)
	print "OK"    

	# set initial PWM duty cycle on pin 1.6 
	print "Set P1.6 DC: "
	us.pwmDuty(uSherpa.PIN_1_6, dcConvert(dc1))
	print "OK"    

	# configure pin 2.2 (internal LED on Launchpad) for PWM output
 	print "Set P2.2to OUTPUT: "  
	us.pinMode(uSherpa.PIN_2_2, uSherpa.PWM)
	print "-> OK"

	# set PWM period to 22000us on pin 2.2 
	print "Set P2.2 period to 22000us: "
	us.pwmPeriod(uSherpa.PIN_2_2, 22000)
	print "OK"    

	# set initial PWM duty cycle on pin 2.2
	print "Set P2.2 DC: "
	us.pwmDuty(uSherpa.PIN_2_2, dcConvert(dc2))
	print "OK"    

	pos1= [ 14, 8.3, 4, 8.3 ]
	pos2 = [ 10, 8.3, 6 ]
	
	y = 0

	try:

		for i in range(3):
			x = 0
			scanMatrix = [] 
			scanMatrix.append([])
			scanMatrix.append([])
			scanMatrix.append([])
			scanMatrix.append([])

			for p1 in pos1:
				x = x + 1
				us.pwmDuty(uSherpa.PIN_1_6, dcConvert(p1))	
				y = 0
				for p2 in pos2:
					y = y + 1					
					us.pwmDuty(uSherpa.PIN_2_2, dcConvert(p2))	
					time.sleep(0.2)

					pl = us.pulselengthRead(uSherpa.PIN_2_0, True); 		
					n = `x` + "x" + `y`
					scanMatrix[x - 1].append( { n : pl })

			print scanMatrix
	except Exception as e: 
		print e

	us.pwmDuty(uSherpa.PIN_1_6, dcConvert(dc1))
	us.pwmDuty(uSherpa.PIN_2_2, dcConvert(dc2))
	# reset MCU 
  	print "RESET: "  
	us.reset()
	print "-> OK"

except Exception as e:
	print traceback.format_exc()

finally:
	if not ps == None:
		ps.stop()	
