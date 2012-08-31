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
This file provides the main API class for using uSherpa. 

Minimal Usage example:
----------------------

from usherpa.api import *
from usherpa.serialcomm import *

# Searial packet stream instance
ps = None

try:

	# Create serial packet stream that connects to MCU running uSherpa via serial 
	# line on port'/dev/ttyUSB0'.
	ps = SerialPacketStream("/dev/ttyUSB0")

	# Start the packet streams receiver thread
	ps.start()

	# Creat uSherpa API instance using serial packet stream as transport
	us = uSherpa(ps)

	# Configure pin 1.0 (internal LED on Launchpad) for output
	us.pinMode(uSherpa.PIN_1_0, uSherpa.OUTPUT)

	# Set pin 1.0 to high (enable LED)
	us.digitalWrite(uSherpa.PIN_1_0, uSherpa.HIGH)

except Exception as e:
	print e 

finally:
	if not ps == None:
		# Stop packet streams receiver thread
		ps.stop()	
'''

from usherpa.comm import *

class uSherpaException(Exception):
	'''
	Exception thrown whenever someting went wrong while using the uSherpa API.
	'''

	def __init__(self, value):
		''' 
		Constructor 
		
		@param value	Message to assign to this exception
		'''

		self.value = value

	def __str__(self):
		''' String representation '''
		return repr(self.value)

class uSherpa:
	''' uSherpa API main class '''
	
	# OUT-bound packet of type NULL
	PACKET_OUT_NULL 							= 0x00 
	
 	# OUT-bound packet of type SYSTEM INFO 
	PACKET_OUT_SYSTEM_INFO 						= 0x02

 	# OUT-bound packet of type PIN FUNCTION 
	PACKET_OUT_PIN_FUNCTION 					= 0x04

 	# OUT-bound packet of type PIN CONTROL 
	PACKET_OUT_PIN_CONTROL 						= 0x05

 	# OUT-bound packet of type PWM FUNCTION 
	PACKET_OUT_PWM_FUNCTION 					= 0x06

  	# OUT-bound packet of type PWM CONTROL 
	PACKET_OUT_PWM_CONTROL 						= 0x07

 	# OUT-bound packet of type EXTERNAL 
	# INTERRUPT FUNCTION 
	PACKET_OUT_EXTERNAL_INTERRUPT_FUNCTION 		= 0x0A

 	# OUT-bound packet of type RESET 
	PACKET_OUT_RESET							= 0xFF

 	# IN-bound packet of type STATUS
	PACKET_IN_STATUS 							= 0x01

 	# IN-bound packet of type SYSTEM INFO
	PACKET_IN_SYSTEM_INFO						= 0x02

 	# IN-bound packet of type DIGITAL PIN READ
	PACKET_IN_DIGITAL_PIN_READ 					= 0x03

  	# IN-bound packet of type ANALOG PIN READ 
	PACKET_IN_ANALOG_PIN_READ					= 0x04

 	# IN-bound packet of type PULSE LENGTH READ 
	PACKET_IN_PULSELENGTH_READ 					= 0x05

 	# Return status ACK for the STATUS 
	# OUT-bound packet
	PACKET_RETURN_ACK							= 0x01

 	# Return status BAD PACKET for the STATUS 
	# OUT-bound packet
	PACKET_RETURN_BAD_PACKET					= 0x02

 	# Return status INVALID PACKET for the 
	# STATUS OUT-bound packet
	PACKET_RETURN_INVALID_PACKET				= 0x03

 	# Return status INVLAID DATA for the STATUS 
	# OUT-bound packet
	PACKET_RETURN_INAVLID_DATA					= 0x04

 	# Return status INVALID PIN COMMAND for the 
	# STATUS OUT-bound packet
	PACKET_RETURN_INVALID_PIN_COMMAND			= 0x05

 	# Control command PIN CLEAR for the PIN 
	# CONTROL packet
	PIN_CONTROL_CLEAR							= 0x00

 	# Control command PIN SET for the PIN 
	# CONTROL packet
	PIN_CONTROL_SET								= 0x01

 	# Control command PIN TOGGLE for the PIN 
	# CONTROL packet
	PIN_CONTROL_TOGGLE							= 0x02

 	# Control command DIGITAL READ for the PIN 
	# CONTROL packet
	PIN_CONTROL_DIGITAL_READ					= 0x03

 	# Control command ANALOG READ for the PIN 
	# CONTROL packet
	PIN_CONTROL_ANALOG_READ						= 0x04

 	# Control command PULSELENGTH READ for the 
	# PIN CONTROL packet
	PIN_CONTROL_PULSELENGTH_READ				= 0x05

 	# Control command PULSELENGTH READ DHF for the 
	# PIN CONTROL packet
	PIN_CONTROL_PULSELENGTH_READ_DHF			= 0x06

 	# PIN function input float
	PIN_FUNCTION_INPUT_FLOAT					= 0x00

 	# PIN function input with internal pull-up 
	# enabled
	PIN_FUNCTION_INPUT_PULLUP					= 0x01

 	# PIN function input with internal pull-down 
	# enabled
	PIN_FUNCTION_INPUT_PULLDOWN					= 0x02

 	# PIN function output 
	PIN_FUNCTION_OUTPUT							= 0x03

 	# PIN function analog input
	PIN_FUNCTION_ANALOG_IN						= 0x04

 	# PIN function PWM output
	PIN_FUNCTION_PWM							= 0x05

	# PIN function EXTERNAL INTERRUPT DISABLE
	PIN_FUNCTION_EXTI_DISABLE 					= 0x00
	
	# PIN function EXTERNAL INTERRUPT HIGH-LOW
	PIN_FUNCTION_EXTI_LOWHIGH 					= 0x01
	
	# PIN function EXTERNAL INTERRUPT HIGH-LOW
	PIN_FUNCTION_EXTI_HIGHLOW 					= 0x02

	# Constant to write a low value to a pin 
	# (in a call to digitalWrite()).
	LOW = PIN_CONTROL_CLEAR

	# Constant to write a high value to a pin 
	# (in a call to digitalWrite()).
	HIGH = PIN_CONTROL_SET

	# Constant to write a high value to a pin 
	# (in a call to digitalWrite()).
	TOGGLE = PIN_CONTROL_TOGGLE

	# Constant to set a pin to output mode 
	# (in a call to pinMode()).
	OUTPUT = PIN_FUNCTION_OUTPUT

	# Constant to set a pin to input mode float
	# (in a call to pinMode()).
	INPUT = PIN_FUNCTION_INPUT_FLOAT

	# Constant to set a pin to input mode pull up
	# (in a call to pinMode()).
	PULLUP = PIN_FUNCTION_INPUT_PULLUP

	# Constant to set a pin to input mode pull down
	# (in a call to pinMode()).
	PULLDOWN = PIN_FUNCTION_INPUT_PULLDOWN

	# Constant to set a pin to input mode analog
	# (in a call to pinMode()).
	ANALOG = PIN_FUNCTION_ANALOG_IN

	# Constant to set a pin to output mode PWM
	# (in a call to pinMode()).
	PWM = PIN_FUNCTION_PWM

    # No edge detectino for external interrupt
	EDGE_NONE	= PIN_FUNCTION_EXTI_DISABLE
	
    # Low-to-high edge detectino for external interrupt
	EDGE_LOWHIGH = PIN_FUNCTION_EXTI_LOWHIGH
	
    # High-tolow edge detectino for external interrupt
	EDGE_HIGHLOW = PIN_FUNCTION_EXTI_HIGHLOW	
	
	# PIN P1.0 on MSP430/Launchpad
	PIN_1_0		= 0x10

	# PIN P1.1 on MSP430/Launchpad
	PIN_1_1		= 0x11
	
	# PIN P1.2 on MSP430/Launchpad
	PIN_1_2		= 0x12
	
	# PIN P1.3 on MSP430/Launchpad
	PIN_1_3		= 0x13
	
	# PIN P1.4 on MSP430/Launchpad
	PIN_1_4		= 0x14
	
	# PIN P1.5 on MSP430/Launchpad
	PIN_1_5		= 0x15
	
	# PIN P1.6 on MSP430/Launchpad
	PIN_1_6		= 0x16
	
	# PIN P1.7 on MSP430/Launchpad
	PIN_1_7		= 0x17

	# PIN P2.0 on MSP430/Launchpad
	PIN_2_0		= 0x20
	
	# PIN P2.1 on MSP430/Launchpad
	PIN_2_1		= 0x21
	
	# PIN P2.2 on MSP430/Launchpad
	PIN_2_2		= 0x22
	
	# PIN P2.3 on MSP430/Launchpad
	PIN_2_3		= 0x23
	
	# PIN P2.3 on MSP430/Launchpad
	PIN_2_4		= 0x24
	
	# PIN P2.5 on MSP430/Launchpad
	PIN_2_5		= 0x25
	
	# PIN P2.6 on MSP430/Launchpad
	PIN_2_6		= 0x26
	
	# PIN P2.7 on MSP430/Launchpad
	PIN_2_7		= 0x27

	# Packet stream used for transfer
	packetStream 	= None

	# Number of retrys on xfer
	retrys		 	= 0

	def __init__(self, packetStream):
		''' 
		Constructor which takes a PacketStream as argument. The PacketStream 
		then is used as pysical transport to the MCU.
	 	
		@param	packetStream	the packet stream to use for communication
	 	@raises	uSherpaException
		'''
	
		self.packetStream = packetStream

		# check if version matches
   		inf = self.systemInfo()

		if inf["firmware_rev"] != 0x01:
			raise uSherpaException("Firmware version mismatch: expected 0x01, and got %x" % 
				inf["firmware_rev"])

	def __xferAndCheckType(self, ptype, data, checkType):
		'''
		Send data to MCU, receive response. ptype is the packet type to send,
		and data is the payload in form of an array('B', [,,,]). Check type
		it the packet type against which the type of the return packet is chacked.
		If the types don't match a uSherpaException is thrown. If the CRC of the
		received packet is wrong, also a uSherpaException is thrown.

	 	@param 	ptype			type for packet to send 
	 	@param 	data			data for packet to send
	 	@param 	checkType		type to which the type of the returned packet is checked
	 	@return	the returned packet
	 	@raises uSherpaException
		''' 

		ret 	= None 
		length 	= 4

		if not data == None: 
			length = length + len(data)
		
		try:
			p = Packet()
			p.fromFields(Packet.PACKET_START_OUTB, length, ptype, data)

			ret = self.packetStream.xfer(p, self.retrys)

		except Exception as e:
			raise uSherpaException(e.__str__())

		if not ret.ptype == checkType:
			# print ret
			raise uSherpaException("Wrong packet type. Expected " + 
				`checkType` + " and received " + `ret.ptype`)


		return ret

	def __xferAndCheckAck(self, ptype, data):
		'''
		Send a packet, and check if the return packet was a ACK packet. If not, throws a
	 	uSherpaException.
	  
	 	@param 	ptype			type for packet to send 
	 	@param 	data			data for packet to send
	 	@raises	uSherpaException
		'''
	
		ret = self.__xferAndCheckType(ptype, data, self.PACKET_IN_STATUS);
		
		if not ret.data[0] == self.PACKET_RETURN_ACK:
			msg = "Wrong status. Expected ACK and received "

 			if ret.data[0] == self.PACKET_RETURN_BAD_PACKET: 
				msg = msg + "BAD PACKET"
			elif ret.data[0] == self.PACKET_RETURN_INVALID_PACKET: 
				msg = msg + "INVALID PACKET"
			elif ret.data[0] == self.PACKET_RETURN_INAVLID_DATA: 
				msg = msg + "INVALID DATA"
			elif ret.data[0] == self.PACKET_RETURN_INVALID_PIN_COMMAND: 
				msg = msg + "INVALID PIN COMMAND"
			else:
				msg = msg + "UNKNOWN"

			raise uSherpaException(msg)

	def packetNull(self):
		'''
	 	Send NULL packet.

 	 	@raises	uSherpaException
		'''

		self.__xferAndCheckAck(self.PACKET_OUT_NULL, None)

	def pinMode(self, pin, mode):
		'''
		Set a digital pin to input or output mode.
	 	Also sets pull-ups/downs for input if requested. 

	 	@param 	pin 		the pin whose mode to set 
	 	@param 	mode 		either input (with options) or output
 	 	@raises uSherpaException 
		'''
	
		self.__xferAndCheckAck(self.PACKET_OUT_PIN_FUNCTION, array('B', [pin, mode]))

	def pwmPeriod(self, pin, period): 
		'''
	 	Setup PWM period. This is only allowed for a pin configured in mode PWM
		before.
	 
	 	@param 	pin 	the pin to set the PWM period for 
	 	@param 	period 	PWM period in microseconds
 	 	@raises	uSherpaException 
		'''
	
		lsb =  0x000000FF & period 
		msb = (0x0000FF00 & period) >> 8

		self.__xferAndCheckAck(self.PACKET_OUT_PWM_FUNCTION, array('B', [pin, lsb, msb]))

	def pwmDuty(self, pin, duty):	
		'''
	 	Setup PWM duty cycle for the PWM. 0 means 0%, 0xFF (255) means 100%.
	
	 	@param 	pin 	the pin whose mode to set 
	 	@param 	duty 	duty cycle 0-255 is 0-100%
 	 	@raises uSherpaException 
		'''
	
		self.__xferAndCheckAck(self.PACKET_OUT_PWM_CONTROL, array('B', [pin, duty]))

	def digitalWrite(self, pin, value):
		'''
	 	Write to a digital pin (the pin must have been put into output mode with pinMode()).
	 
	 	@param 	pin 		the pin to write to 
	 	@param 	value      		the value to write: LOW, HIGH or TOGGLE
 	 	@raises	uSherpaException  
		'''
	
		self.__xferAndCheckAck(self.PACKET_OUT_PIN_CONTROL, array('B', [pin, value]))

	def digitalRead(self, pin):
		'''
		Read from digital pin (the pin must have been put into input mode with pinMode()).

	 	@param 	pin 		the pin to read from 
	 	@return current state of the pin
 	 	@raises uSherpaException 
		'''

		ret = self.__xferAndCheckType(self.PACKET_OUT_PIN_CONTROL,  
			array('B', [pin, self.PIN_CONTROL_DIGITAL_READ]),
			self.PACKET_IN_DIGITAL_PIN_READ)

		return ret.data[1]

	def analogRead(self, pin):
		'''
		Perform analog read from pin (the pin must have been put into input mode with pinMode()).
	 
	 	@param 	pin 		the pin to read from 
	 	@return current value of pin
 	 	@raises	uSherpaException 
		'''
	
		ret = self.__xferAndCheckType(self.PACKET_OUT_PIN_CONTROL, 
			array('B', [pin, self.PIN_CONTROL_ANALOG_READ]), 
			self.PACKET_IN_ANALOG_PIN_READ)

		lsb = 0x00FF & ret.data[1]
		msb = 0x00FF & ret.data[2]
		val = 0xFFFF & (lsb | (msb << 8))
		
		return val

	def pulselengthRead(self, pin, dhf=False):
		'''
		Read pulselenght from pin (the pin must have been put into input mode with
		pinMode()). The function waits until the requested pin changes its state, 
		then measures the time it takes until the original pin state is seen again. 
		In case the state changes take longer then 0xFFFF, the function terminates,
		with an exeption. 

		If dhf (drive-high-first) is set to True, the input is switched to output
		and driven high for at lieat 10us. Then, the pin is set back to wathever
		input it was before, and the pulse-length is read. This is especially 
		helpful when working with sensors that return the values digitally.
	
		@param 	pin 	the pin to read from 
		@param 	dhf 	if set to True, the pin is driven high for ~10us before 
						pulse-lenght is measuered	
		@return pulse-lenght read on pin	
 		@raises	uSherpaException 
		'''

		mode = self.PIN_CONTROL_PULSELENGTH_READ

		if dhf:
			mode = self.PIN_CONTROL_PULSELENGTH_READ_DHF

		ret = self.__xferAndCheckType(self.PACKET_OUT_PIN_CONTROL,  
			array('B', [pin, mode]),  
			self.PACKET_IN_PULSELENGTH_READ)
	
		lsb = 0x00FF & ret.data[1]
		msb = 0x00FF & ret.data[2]
		val = 0xFFFF & (lsb | (msb << 8))
		
		if val >= 0xFFFF:
			raise uSherpaException("Pulselength read timed out")

		return val

	def systemInfo(self):
		'''
		System info from uSherpa firmware running on MCU.

	 	@return	System info as a dictionary (board_type, mcu_type, firmware_rev) 
 	 	@raises	uSherpaException 
		'''
	
		ret = self.__xferAndCheckType(self.PACKET_OUT_SYSTEM_INFO, None, self.PACKET_IN_SYSTEM_INFO)

		board_type = 0x000000FF & ret.data[0]
		mcu_type   = 0x000000FF & ret.data[1]
		fw_rev	   = 0x000000FF & ret.data[2]
		
		inf = { "board_type" : board_type, "mcu_type" : mcu_type, "firmware_rev" : fw_rev } 

		return inf

	def reset(self):
		'''
		Reset MCU. 

 		@raises	uSherpaException 
		'''

		self.__xferAndCheckAck(self.PACKET_OUT_RESET, None)

	def externalInterrupt(self, pin, mode, triggerCount = 0): 
		'''
		Enabled / disables external interrupts for a given pin. 
		Interrupting is disabled if mode is set to EDGE_NONE, 
		and enabled with EDGE_LOWHIGH or EDGE_HIGHLOW. 

		@param pin		the pin for which to disable/enable external interrupt 
		@param mode		edge mode for extrnal interrupt (EDGE_LOWHIGH, EDGE_HIGHLOW, EDGE_NONE)
 		@raises	uSherpaException 
		'''

		self.__xferAndCheckAck(self.PACKET_OUT_EXTERNAL_INTERRUPT_FUNCTION, 
			array('B', [pin, mode, triggerCount]))
	
