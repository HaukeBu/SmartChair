import threading
import GRPCHandler as grpc_handler
import time
import HAL as hal
import Constants
import Config
import Callbacks
import Gyroscope as gy
import sys

class MessageThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True

	def run(self):
		queue = grpc_handler.GRPCQueue()
		handler = grpc_handler.GRPCHandler()

		handler.initialize(Constants.GRPC_SERVER_IP)

		print("Message thread started")
		while True:
			message = queue.getMessage()
			if type(message) != type(False):
				for i in range(Constants.GRPC_FAIL_RETRY):
					if handler.sendMessage(message):
						break

class SerialThread(threading.Thread):
	def __init__(self, serial):
		threading.Thread.__init__(self)
		self.daemon = True

		self.ser_dispatcher = serial

	def run(self):
		print("Serial thread started")
		while True:
			self.ser_dispatcher.dispatch()

class HALThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True

		self.hal_instance = hal.HAL()
		self.interval_list = self.hal_instance.getIntervalList()

		self.next_wakeup = {}
		for address, val in self.interval_list.iteritems():
			self.next_wakeup[int(address)] = 0


	def __getMillis(self):
		return int(round(time.time() * 1000))

	def __sleepTime(self):
		ret = sys.maxint

		for address, wakeup in self.next_wakeup.iteritems():
			if ret > (wakeup - self.__getMillis()):
				ret = wakeup - self.__getMillis()

		return max(0, ret / 1000)

	def run(self):
		if self.interval_list:
			print("HAL thread started")
			while True:
				for address, interval in self.interval_list.iteritems():
					if self.next_wakeup[int(address)] <= self.__getMillis():
						sensor_data = self.hal_instance.getData(address)
						Callbacks.gyroscope(address, sensor_data)
						self.next_wakeup[address] = interval + self.__getMillis()

				time.sleep(self.__sleepTime())

class GyroscopeThread(threading.Thread):
	def __init__(self, address):
		threading.Thread.__init__(self)
		self.daemon = True

		self.address = address
		self.gy = gy.Gyroscope(address)

	def run(self):
		self.gy.initialize()

		print("Gyroscope thread with address " + str(self.address) + " started")
		while True:
			sleep_time = self.gy.acquireData()
			if sleep_time > 0:
				time.sleep(sleep_time)
