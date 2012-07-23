import time
import traceback

from usherpa.api import *
from usherpa.serialcomm import *

# Searial Packet stream instance
ps = None

dc 		= 0
dcDir 	= 5

try:

	print "uSherpaPwmLed"

	ps = SerialPacketStream("/dev/ttyUSB0")
	ps.start()

	us = uSherpa(ps)

	# configure pin 1.6 (internal LED on Launchpad) for PWM output
 	print "Set P1.6 to OUTPUT: "  
	us.pinMode(uSherpa.PIN_1_6, uSherpa.PWM)
	print "-> OK"

	# set PWM period to 1000us on pin 1.6 
	print "Set P1.6 period to 1000us: "
	us.pwmPeriod(uSherpa.PIN_1_6, 1000)
	print "OK"    

	try:

		while True:
			# modify duty-cycle
			dc = dc + dcDir

		    # if max. duty cycle (0xFF) reached, reverse direction
			if dc >= 0xFF:
				dcDir = -dcDir
       			# make sure DC is still valid
				dc = 0xFF
			# if min. duty cycle (0x00) reached, reverse direction
			elif dc <= 0x00:
				dcDir = -dcDir
       			# make sure DC is still valid
				dc = 0x00
   
			# write modified DC   
			print "Set P1.6 duty cycle to " + hex(dc) + ": "
			us.pwmDuty(uSherpa.PIN_1_6, dc)
			print "OK"    

	except KeyboardInterrupt: 
		pass

	# reset MCU 
  	print "RESET: "  
	us.reset()
	print "-> OK"

except Exception as e:
	print traceback.format_exc()

finally:
	if not ps == None:
		ps.stop()	
