import serial
import CRC16
import Constants
import time

VERSION = 1

SERIAL_READ_START = 0xAF
SERIAL_READ_END = 0xFE

SERIAL_SEND_START = 0xDE
SERIAL_SEND_END = 0xED

class SerialDispatcher():
	def __init__(self):
		self.callback_list = []
		self.interval_list = []
		self.initialized = False

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

		self.__sendInitMessage()

		self.initialized = True

		print("Initialized serial dispatcher")

	def __sendInitMessage(self):
		crc_list = []
		crc_list.append(VERSION)

		length = 0
		for _, element in interval_list:
			if element > 0:
				length += 1

		crc_list.append(length)

		for idx, val in interval_list:
			crc_list.append(idx)
			crc_list.append(val & 0xFF)
			crc_list.append(val >> 8)

		crc = CRC16.crc16_ccitt(crc_list, len(crc_list))

		self.ser_con.write(SERIAL_SEND_START)
		self.ser_con.write(crc_list)
		self.ser_con.write(crc & 0xFF)
		self.ser_con.write(crc >> 8)
		self.ser_con.write(SERIAL_SEND_END)

	def appendCallback(self, idx, cb, interval):
		if self.initialized:
			print("Can't append callback function when already initialized")
			return False
		else:
			self.callback_list.insert(idx.value, cb)
			self.interval_list.insert(idx.value, interval)
			print("Add new callback function for " + idx.name)
			return True

	def __readByte(self):
		return ord(self.ser_con.read())

	def dispatch(self):
		# Read until start sequence occurs
		while self.__readByte() != SERIAL_READ_START:
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
		if last_byte != SERIAL_READ_END:
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
