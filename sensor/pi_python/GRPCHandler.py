import grpc
import time

import chair_pb2
import chair_pb2_grpc


class GRPCHandler():
	def __init__(self):
		self.grpc_channel = None
		self.grpc_service = None

	def initialize(self, server):
		self.grpc_channel = grpc.insecure_channel(server)
		self.grpc_service = chair_pb2_grpc.ChairServiceStub(grpc_channel)

	def buildMessage(self, version, sensor_type, values, timestamp = 0):
		timestamp = round(time.time())

		ret_msg = chair_pb2.Chair(version = version, timestamp = timestamp
								, sensor_type = sensor_type, values = values)

		return ret_msg

	def sendMessage(self, message):
		self.grpc_service.ChairUpdate(message)
