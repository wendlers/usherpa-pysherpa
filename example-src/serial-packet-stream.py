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
