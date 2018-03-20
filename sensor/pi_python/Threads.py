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

		while True:
			message = queue.getMessage()
			if type(message) != type(False):
				handler.sendMessage(message)

class SerialThread(threading.Thread):
	def __init__(self, serial):
		threading.Thread.__init__(self)
		self.daemon = True

		self.ser_dispatcher = serial

	def run(self):
		while True:
			self.ser_dispatcher.dispatch()

class HALThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True

		self.hal_instance = hal.HAL()
		self.interval_list = self.hal_instance.getIntervalList()

		self.next_wakeup = {}


	def __getMillis(self):
		return int(round(time.time() * 1000))

	def __sleepTime(self):
		ret = sys.maxint

		for address, wakeup in self.next_wakeup.iteritems():
			if ret > (self.wakeup - self.__getMillis()):
				ret = self.wakeup - self.__getMillis()

		return max(0, ret / 1000)

	def run(self):
		if interval_list:
			while True:
				for address, interval in interval_list.iteritems():
					if self.next_wakeup[address] <= self.__getMillis():
						sensor_data = self.hal_instance.getData(address)
						Callbacks.gyroscope(address, sensor_data)
						self.next_wakeup[address] = interval + self.__getMillis()

				time.sleep(self.__sleepTime())

class GyroscopeThread(threading.Thread):
	def __init__(self, address):
		threading.Thread.__init__(self)
		self.daemon = True

		self.gy = gy.Gyroscope(address)

	def run(self):
		self.gy.initialize()
		while True:
			sleep_time = self.gy.acquireData()
			time.sleep(sleep_time)
