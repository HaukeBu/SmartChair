import threading
import GRPCHandler as grpc_handler
import time
import HAL as hal
import Constants
import Config
import Callbacks

class MessageThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True

	def run(self):
		print("Start message")
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
		print("Start serial thread")
		while True:
			self.ser_dispatcher.dispatch()

class HALThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True
		self.next_back = 0
		self.next_seat = 0

	def __getMillis(self):
		millis = int(round(time.time() * 1000))

	def __sleepTime(self):
		return min(next_back - __getMillis(), next_seat - __getMillis())

	def run(self):
		hal_sensors = hal.HAL()
		interval_back = Config.config['GYROSCOPE_BACK']['Interval']
		interval_seat = Config.config['GYROSCOPE_SEAT']['Interval']
		if interval_back > 0 || interval_seat > 0:
			while True:
				if interval_back > 0 and self.next_back <= __getMillis():
					sensor_data = hal_sensors.getGyroBack()
					Callbacks.gyroscopeBack(sensor_data)
					self.next_back = __getMillis() + interval_back

				if interval_seat > 0 and self.next_seat <= __getMillis():
					sensor_data = hal_sensors.getGyroSeat()
					Callbacks.gyroscopeSeat(sensor_data)
					self.next_seat = __getMillis() + interval_seat

				time.sleep(__sleepTime())
