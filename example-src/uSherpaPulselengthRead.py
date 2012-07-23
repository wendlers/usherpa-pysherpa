import time
import traceback

from usherpa.api import *
from usherpa.serialcomm import *

# Searial Packet stream instance
ps = None


try:

	print "uSherpaPwmRead"

	ps = SerialPacketStream("/dev/ttyUSB0")
	ps.start()

	us = uSherpa(ps)

	# configure pin 1.3 (internal button on Launchpad) for input 
 	print "Set P1.3 to INPUT: "  
	us.pinMode(uSherpa.PIN_1_3, uSherpa.INPUT)
	print "-> OK"

	# read pin 1.3 until state changed form high to low
 	print "Read P1.3 DIGITAL (wait for button press)"

	pl = us.pulselengthRead(uSherpa.PIN_1_3); 

	print "Pulselenght was: " + `pl`

	# reset MCU 
  	print "RESET: "  
	us.reset()
	print "-> OK"

except Exception as e:
	print traceback.format_exc()

finally:
	if not ps == None:
		ps.stop()	
