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
