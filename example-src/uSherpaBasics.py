import time
import traceback

from usherpa.api import *
from usherpa.serialcomm import *

# Searial Packet stream instance
ps = None

try:

	print "uSherpaPulselenghtRed"

	ps = SerialPacketStream("/dev/ttyUSB0")
	ps.start()

	us = uSherpa(ps)

	# send null packet
	print "Sending NULL: "
	us.packetNull()
	print "-> OK"

	# retrive system info an print it 
	print "Sending SYSTEMINFO: "  
   	inf = us.systemInfo()
	print "-> OK: ", hex(inf["board_type"]), hex(inf["mcu_type"]), hex(inf["firmware_rev"])

	# configure pin 1.0 (internal LED on Launchpad) for output
 	print "Set P1.0 to OUTPUT: "  
	us.pinMode(uSherpa.PIN_1_0, uSherpa.OUTPUT)
	print "-> OK"

	# set pin 1.0 to high (enable LED)
  	print "Set P1.0 to HIGH: "  
	us.digitalWrite(uSherpa.PIN_1_0, uSherpa.HIGH)
	print "-> OK"

	time.sleep(0.25);

	# toggel LED 10 times
	for i in range(0, 10):
	  	print "TOGGLE P1.0: "  
		us.digitalWrite(uSherpa.PIN_1_0, uSherpa.TOGGLE)
		print "-> OK"

		time.sleep(0.25);

	# reset MCU 
  	print "RESET: "  
	us.reset()
	print "-> OK"

except Exception as e:
	print traceback.format_exc()

finally:
	if not ps == None:
		ps.stop()	
