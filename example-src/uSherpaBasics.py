import time
import traceback

from usherpa.api import *
from usherpa.serialcomm import *

try:

	print "uSherpaBasics"

	ps = SerialPacketStream("/dev/ttyS0")
	ps.start()

	us = uSherpa(ps)

	# send null packet
	print "Sending NULL: "
	us.packetNull()
	print "-> OK"

	# retrive system info an print it 
	print "Sending SYSTEMINFO: "  
   	inf = us.systemInfo()
	print "-> OK: ", inf

	# configure pin 1.0 (internal LED on Launchpad) for output
 	print "Set P1.0 to OUTPUT: "  
	us.pinMode(uSherpa.PIN_1_0, uSherpa.OUTPUT)
	print "-> OK"

	# set pin 1.0 to high (enable LED)
  	print "Set P1.0 to HIGH: "  
	us.digitalWrite(uSherpa.PIN_1_0, uSherpa.HIGH)
	print "-> OK"

	time.sleep(0.5);

except Exception as e:
	print traceback.format_exc()

finally:
	ps.stop()	
	pass
