import serial
import CRC16
import Constants
import time

VERSION = 1

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

		print("Initialized serial dispatcher")

	def appendCallback(self, idx, cb):
		self.callback_list.insert(idx.value, cb)
		print("Add new callback function for " + idx.name)

	def __readByte(self):
		return ord(self.ser_con.read())

	def dispatch(self):
		# Read until start sequence occurs
		while self.__readByte() != 0xAF:
			time.sleep(0.01)

		buffer = []
		# Version
		buffer.append(self.__readByte())
		# Type
		buffer.append(self.__readByte())
		# Length
		buffer.append(self.__readByte())

		# Payload
		for i in range(buffer[2]):
			buffer.append(self.__readByte())

		# CRC Checksum
		crc1 = self.__readByte()
		crc2 = self.__readByte()
		crc = (crc2 << 8) | crc1

		last_byte = self.__readByte()
		if last_byte != 0xFE:
			print("No Termination byte " + hex(last_byte))
			return Constants.SerialDispatchError.NO_TERMINATION_BYTE


		crc_t = CRC16.crc16_ccitt(buffer, buffer[2] + 3)
		if crc != crc_t:
			print("*** Checksum error")
			print("Sent: " + hex(crc) + ", Check: " + hex(crc_t))
			return Constants.SerialDispatchError.CHECKSUM_ERROR

		if buffer[0] != VERSION:
			print("Version error")
			return Constants.SerialDispatchError.VERSION_ERROR

		payload = []
		for i in range(3, len(buffer), 2):
			payload.append((buffer[i + 1] << 8) | buffer[i])

		self.callback_list[buffer[1]](payload)
