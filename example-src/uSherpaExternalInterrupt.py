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

The following example shows:

- how to connect to the MCU through serial line, 
- configure pins as digital input, 
- enable external interrupts for this input,
- and provide an event handler which is called
  whenever a state change is detecetd on the input pin
'''

import traceback

from usherpa.api import *
from usherpa.serialcomm import *

# Searial Packet stream instance
ps = None

def exti(packet):
	''' Callback handler for external interrupts received from uSherpa ''' 
 
	print "Received external interrupt: ", packet

try:

	print "uSherpaExternal Interrupt"

	ps = SerialPacketStream("/dev/ttyUSB0")
	
	# register callback handler for external interrupts
	ps.evHandler = exti
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

	# for pin 1.3 enable external interrupt for high-to-low transitions
 	print "Enable EXTI on HIGH-LOW transition for P1.3: "
	us.externalInterrupt(uSherpa.PIN_1_3, uSherpa.EDGE_HIGHLOW);
	print "-> OK"

	# for pin 2.3 enable external interrupt for low-to-high transitions
 	print "Enable EXTI on HIGH-LOW transition for P2.3: "
	us.externalInterrupt(uSherpa.PIN_2_3, uSherpa.EDGE_LOWHIGH);
	print "-> OK"

	# for pin 2.4 enable external interrupt for high-to-low transitions
 	print "Enable EXTI on HIGH-LOW transition for P2.4: "
	us.externalInterrupt(uSherpa.PIN_2_4, uSherpa.EDGE_HIGHLOW);
	print "-> OK"
	
	print "Press ENTER to exit"
	raw_input()

	# reset MCU 
  	print "RESET: "  
	us.reset()
	print "-> OK"

except Exception as e:
	print traceback.format_exc()

finally:
	if not ps == None:
		ps.stop()	
