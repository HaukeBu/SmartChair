import threading
import GRPCHandler as grpc_handler
#import HAL as hal

class MessageThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True

	def run(self):
		queue = grpc_handler.GRPCQueue()
		#handler = grpc_handler.GRPCHandler()

		#handler.initialize()

		while True:
			message = queue.getMessage()
			if type(message) != type(False):
				#handler.sendMessage(message)
				print(message)

class SerialThread(threading.Thread):
	def __init__(self, serial):
		threading.Thread.__init__(self)
		self.daemon = True

		self.ser_dispatcher = serial

	def run(self):
		while True:
			self.ser_dispatcher.dispatch()

'''
class HALThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True

	def run(self):
		hal_sensors = hal.HAL()
		while True:
			sensor_data = hal_sensors.getGyro()
'''
