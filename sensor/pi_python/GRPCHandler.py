import grpc
import time
import Queue

import Chair_pb2
import Chair_pb2_grpc

def buildMessage(version, sensor_type, values, timestamp = 0):
	timestamp = int(time.time())

	ret_msg = Chair_pb2.Chair(version = version, timestamp = timestamp
							, sensor_type = sensor_type.value, values = values)

	return ret_msg

class GRPCQueue():
	__instance = None

	class __impl:
		def __init__(self):
			self.message_queue = Queue.Queue()

		def addMessage(self, message):
			self.message_queue.put(message)

		def getMessage(self):
			if not self.message_queue.empty():
				return self.message_queue.get()
			else:
				return False

	def __init__(self):
		if GRPCQueue.__instance is None:
			GRPCQueue.__instance = GRPCQueue.__impl()

		self.__dict__['_Singleton__instance'] = GRPCQueue.__instance

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self.__instance, attr, value)


class GRPCHandler():
	__instance = None

	class __impl:
		def __init__(self):
			self.is_initialized = False
			self.message_queue = Queue.Queue()
			self.grpc_channel = None
			self.grpc_service = None

		def initialize(self, server):
			if not self.is_initialized:
				self.grpc_channel = grpc.insecure_channel(server)
				self.grpc_service = Chair_pb2_grpc.ChairServiceStub(self.grpc_channel)
				self.is_initialized = True

		def sendMessage(self, message):
			if self.is_initialized:
				try:
					self.grpc_service.ChairUpdate(message)
					return True
				except:
					return False

	def __init__(self):
		if GRPCHandler.__instance is None:
			GRPCHandler.__instance = GRPCHandler.__impl()

		self.__dict__['_Singleton__instance'] = GRPCHandler.__instance

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self.__instance, attr, value)
