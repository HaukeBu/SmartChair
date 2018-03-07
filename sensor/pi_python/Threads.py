import threading
import GRPCHandler as grpc_handler
import time
import HAL as hal
import Constants

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
				#print(message)

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

	def run(self):
		hal_sensors = hal.HAL()
		while True:
			sensor_data = hal_sensors.getGyro()
			#print("gryo: " + str(sensor_data))

