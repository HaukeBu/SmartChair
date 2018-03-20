import serial
import CRC16
import Constants
import time


class SerialDispatcher():
	def __init__(self):
		self.callback_list = {}
		self.interval_list = {}
		self.initialized = False

	def initialize(self, port, baudrate):
		self.ser_con = serial.Serial()

		self.ser_con.port = port
		self.ser_con.baudrate = baudrate
		self.ser_con.timeout = None

		try:
			self.ser_con.open()
		except serial.SerialException:
			return False

		self.ser_con.flushOutput()
		self.ser_con.flushInput()

		time.sleep(2)

		self.__sendInitMessage()

		self.initialized = True

		print("Initialized serial dispatcher")

		return True

	def __sendInitMessage(self):
		crc_list = []
		crc_list.append(Constants.SERIAL_VERSION)

		length = 0
		for _, val in self.interval_list.iteritems():
			if val > 0:
				length += 1

		crc_list.append(length)

		for idx, val in self.interval_list.iteritems():
			crc_list.append(idx)
			crc_list.append(val & 0xFF)
			crc_list.append(val >> 8)

		crc = CRC16.crc16_ccitt(crc_list, len(crc_list))

		self.ser_con.write(chr(Constants.SERIAL_SEND_START))
		for val in crc_list:
			self.ser_con.write(chr(val))
		self.ser_con.write(chr(crc & 0xFF))
		self.ser_con.write(chr(crc >> 8))
		self.ser_con.write(chr(Constants.SERIAL_SEND_END))


	def appendCallback(self, idx, cb, interval):
		if self.initialized:
			print("Can't append callback function when already initialized")
			return False
		else:
			self.callback_list[idx.value] = cb
			self.interval_list[idx.value] = interval
			print("Add new callback function for " + idx.name + ", Interval = " + str(interval))
			return True

	def __readByte(self):
		return ord(self.ser_con.read())

	def dispatch(self):
		# Read until start sequence occurs
		while self.__readByte() != Constants.SERIAL_READ_START:
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
		if last_byte != Constants.SERIAL_READ_END:
			print("No Termination byte " + hex(last_byte))
			return Constants.SerialDispatchError.NO_TERMINATION_BYTE


		crc_t = CRC16.crc16_ccitt(buffer, buffer[2] + 3)
		if crc != crc_t:
			print("*** Checksum error")
			print("Sent: " + hex(crc) + ", Check: " + hex(crc_t))
			return Constants.SerialDispatchError.CHECKSUM_ERROR

		if buffer[0] != Constants.SERIAL_VERSION:
			print("Version error")
			return Constants.SerialDispatchError.VERSION_ERROR

		payload = []
		for i in range(3, len(buffer), 2):
			payload.append((buffer[i + 1] << 8) | buffer[i])

		if buffer[1] in self.callback_list:
			self.callback_list[buffer[1]](payload)
