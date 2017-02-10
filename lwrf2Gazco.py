#!/usr/bin/env python
"""
This module uses the custom Lightwaverf Gazco extension in Pigpio
to receive LWRF messages and translate them to Gazco On/Off

Pigpio must have been built with the Lightwave custom extension
Pigpiod must be running (sudo pigpiod)

"""
# 2017-01-13
# lwrf2Gazco.py

import time
import pigpio

# Pigpio custom extension calls for Lightwaverf
CUSTOM_LWRF           =7287
CUSTOM_LWRF_TX_INIT   =1
CUSTOM_LWRF_TX_BUSY   =2
CUSTOM_LWRF_TX_PUT    =3
CUSTOM_LWRF_TX_CANCEL =4
CUSTOM_LWRF_RX_INIT   =10
CUSTOM_LWRF_RX_CLOSE  =11
CUSTOM_LWRF_RX_READY  =12
CUSTOM_LWRF_RX_GET    =13
CUSTOM_GAZCO_TX_PUT   =20
CUSTOM_LWRF_TX_DEBUG  =99
CUSTOM_LWRF_RX_DEBUG  =100
LWRF_MSGLEN           =10
GAZCO_MSGLEN          =3

CUSTOM_PROTO_LWRF     =0
CUSTOM_PROTO_GAZCO    =1


class tx():

	def __init__(self, pi, txgpio):
		"""
		Initialise a transmitter with the pigpio and the transmit gpio.
		"""
		self.pi = pi
		(count, data) = self.pi.custom_2(CUSTOM_LWRF, [CUSTOM_LWRF_TX_INIT, txgpio])

	def put(self, data, repeat=1, proto=CUSTOM_PROTO_LWRF):
		"""
		Transmit a message repeat times
		0 is returned if message transmission has successfully started.
		Negative number indicates an error.
		"""
		ret = 0
		if len(data) <> LWRF_MSGLEN:
			ret = -1
		else:
			argx = [CUSTOM_LWRF_TX_PUT, repeat, proto]
			argx.extend(list(data))
			self.pi.custom_2(CUSTOM_LWRF, [CUSTOM_LWRF_TX_CANCEL])
			(count, data) = self.pi.custom_2(CUSTOM_LWRF, argx)
		return ret


	def ready(self):
		"""
		Returns True if a new message may be transmitted.
		"""
		(count, data) = self.pi.custom_2(CUSTOM_LWRF, [CUSTOM_LWRF_TX_BUSY])
		if (count == 0):
			return True
		else:
			return False

	def cancel(self):
		"""
		Cancels the wireless transmitter, aborting any message
		in progress.
		"""
		self.pi.custom_2(CUSTOM_LWRF, [CUSTOM_LWRF_TX_CANCEL])

class rx():

	def __init__(self, pi, rxgpio, repeat):
		"""
		Instantiate a LightwaveRF receiver with the Pi, the receive gpio, and
		Repeat count sets number of identical messages before a report 
		A repeat count > 0 also filters duplicates
		"""
		self.pi = pi
		self.pi.custom_2(CUSTOM_LWRF, [CUSTOM_LWRF_RX_INIT, rxgpio, repeat])

	def get(self):
		"""
		Returns the next unread message, or None if none is available.
		"""
		(count, data) = self.pi.custom_2(CUSTOM_LWRF, [CUSTOM_LWRF_RX_GET])
		if (count > 0):
			return data
		else:
			return None

	def ready(self):
		"""
		Returns True if there is a message available to be read.
		"""
		(count, data) = self.pi.custom_2(CUSTOM_LWRF, [CUSTOM_LWRF_RX_READY])
		if count > 0:
			return True
		else:
			return False

	def cancel(self):
		"""
		Cancels the wireless receiver.
		"""
		self.pi.custom_2(CUSTOM_LWRF, [CUSTOM_LWRF_RX_CLOSE])

"""
Main routine
"""

if __name__ == "__main__":

	import time
	import pigpio
	import lwrf2Gazco
	import logging

	#Edit the pins used and commands to be employed here
	RX=24
	TX=25
	LWRF_DEVICE_ON   = "1F71999990"
	LWRF_DEVICE_OFF  = "4070999990"
	GAZCO_DEVICE_ON  = "9999C80000"
	GAZCO_DEVICE_OFF = "9999D80000"
	TX_REPEAT = 10
	RX_REPEAT = 2
	
	logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/GazcoLog',level=logging.INFO)
	
	pi = pigpio.pi() # Connect to local Pi.

	rx = lwrf2Gazco.rx(pi, RX, RX_REPEAT) # Specify Pi, rx gpio, and repeat.
	tx = lwrf2Gazco.tx(pi, TX) # Specify Pi, tx gpio

	logging.info('Starting LWRF 2 Gazco')
	start = time.time()
   
	while True:
		if rx.ready():
			msg = rx.get()
			logging.info('Received msg %s', msg)
			if msg == LWRF_DEVICE_ON:
				logging.info('Wait for lightwave tx to stop')
				time.sleep(3)
				logging.info('Send Gazco On')
				tx.put(GAZCO_DEVICE_ON, TX_REPEAT, CUSTOM_PROTO_GAZCO)
			elif msg == LWRF_DEVICE_OFF:
				logging.info('Wait for lightwave tx to stop')
				time.sleep(3)
				logging.info('Send Gazco Off')
				tx.put(GAZCO_DEVICE_OFF, TX_REPEAT, CUSTOM_PROTO_GAZCO)
		time.sleep(0.02)
	rx.cancel()
	tx.cancel()
	pi.stop()
	time.sleep(2)

