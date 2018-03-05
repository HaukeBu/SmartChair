import serial
import CRC16
from enum import Enum

VERSION = 1

class Header(Enum):
	DEBUG = 0
	DISTANCE = 1
	PRESSURE_BACK = 2
	PRESSURE_SEAT = 3
	TEMPERATURE = 4

class DispatchError(Enum):
	NO_TERMINATION_BYTE = 1
	CHECKSUM_ERROR = 2
	VERSION_ERROR = 3

class SerialDispatcher():
    def __init__(self):
        self.callback_list = []

	def initialize(self, port, baudrate):
		self.ser_con = serial.Serial()

		self.ser_con.port = port
		self.ser_con.baudrate = baudrate
		self.ser_con.timeout = None

		try:
			self.ser_con.open()
		except serial.SerialException:
			return 1

		self.ser_con.flushOutput()
		self.ser_con.flushInput()

	def appendCallback(self, idx, cb):
		self.callback_list[idx] = cb

    def dispatch(self):
		# Read until start sequence occurs
        while self.ser_con.read(1) != 0xAF:

		buffer = []
		# Version
		buffer[0] = self.ser_con.read(1)
		# Type
		buffer[1] = self.ser_con.read(1)
		# Length
		buffer[2] = self.ser_con.read(1)

		# Payload
		for i in range(buffer[2]):
			buffer[i + 3] = self.ser_con.read(1)

		# CRC Checksum
		crc1 = self.ser_con.read(1)
		crc2 = self.ser_con.read(1)
		crc = (crc2 << 8) | crc1

		if self.ser_con.read(1) != 0xFE:
			return DispatchError.NO_TERMINATION_BYTE

		# TODO write crc16 module
		if crc != CRC16.crc16_ccitt(buffer, buffer[2]):
			return DispatchError.CHECKSUM_ERROR

		if buffer[0] != VERSION:
			return DispatchError.VERSION_ERROR

		payload = []
		for i in range(3, buffer[2], 2):
			payload[i] = (buffer[i + 1] << 8) | buffer[i]

		self.callback_list[buffer[1]](payload)
