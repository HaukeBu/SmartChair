import threading
import GRPCHandler as grpc_handler
import time
import HAL as hal
import Constants
import Config
import Callbacks
import Gyroscope as gy

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



	def __getMillis(self):
		return int(round(time.time() * 1000))

	def __sleepTime(self):
		ret = 0

		if self.interval_back > 0 and self.interval_seat == 0:
			ret = self.next_back - self.__getMillis()
		elif self.interval_seat > 0 and self.interval_back == 0:
			ret = self.next_seat - self.__getMillis()
		else:
			ret = min(self.next_back - self.__getMillis()
					, self.next_seat - self.__getMillis())

		return max(0, ret / 1000)

	def run(self):
		hal_sensors = hal.HAL()
		if self.interval_back > 0 or self.interval_seat > 0:
			while True:
				if self.interval_back > 0 and self.next_back <= self.__getMillis():
					sensor_data = hal_sensors.getGyroBack()
					Callbacks.gyroscopeBack(sensor_data)
					self.next_back = self.__getMillis() + self.interval_back

				if self.interval_seat > 0 and self.next_seat <= self.__getMillis():
					sensor_data = hal_sensors.getGyroSeat()
					Callbacks.gyroscopeSeat(sensor_data)
					self.next_seat = self.__getMillis() + self.interval_seat

				time.sleep(self.__sleepTime())

class GyroscopeThread(threading.Thread):
	def __init__(self, address):
		threading.Thread.__init__(self)
		self.daemon = True

		self.gy = gy.Gyroscope(address)

	def run(self):
		while True:
			sleep_time = self.gy.acquireData()
			time.sleep(sleep_time)
