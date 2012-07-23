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
