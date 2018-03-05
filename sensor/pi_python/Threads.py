import threading

class SerialThread(threading.Thread):
	def __init__(self, serial):
		threading.Thread.__init__(self)
		self.daemon = True

		self.ser_dispatcher = serial

	def run(self):
		while True:
			self.ser_dispatcher.dispatch()

class HALThread(threading.Thread):
	def __init__(self, hal):
		threading.Thread.__init__(self)
		self.daemon = True

		self.hal = hal

	def run(self):
		while True:
			sensor_data = self.hal.getGyro()

			
