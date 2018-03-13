import Constants
import GRPCHandler as grpc_handler
import Helper

def debug(payload):
	values = Helper.listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.SerialHeader.DEBUG,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)

def distance(payload):
	print("in distance")
	if len(payload) != 1:
		print("distance:: payload too long " + str(len(payload)))
		return

	values = Helper.listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.SerialHeader.DISTANCE,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)

def pressureBack(payload):
	values = Helper.listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.SerialHeader.PRESSURE_BACK,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)


def pressureSeat(payload):
	values = Helper.listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.SerialHeader.PRESSURE_SEAT,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)

def temperature(payload):
	if len(payload) != 1:
		print("temperature:: payload too long " + str(len(payload)))
		return

	values = Helper.listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.SerialHeader.TEMPERATURE,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)

def gyroscope(payload):
	values = Helper.listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.GRPCHeader.GYROSCOPE,
		values = values
	)
	
	grpc_handler.GRPCQueue().addMessage(message)
