import Constants
import GRPCHandler as grpc_handler

def listToJSONString(lst):
	ret_str = '"values": ['

	for idx in range(len(lst)):
		ret_str += '{"id": ' + str(idx) + ', "value": ' + str(lst[idx]) + '}'

		if idx < len(lst) - 1:
			ret_str += ', '

	ret_str += ']'

	return ret_str

def debug(payload):
	values = listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.SerialHeader.DEBUG,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)

def distance(payload):
	if len(payload) != 1:
		print("distance:: payload too long " + str(len(payload)))
		return

	values = listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.SerialHeader.DISTANCE,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)

def pressureBack(payload):
	values = listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.SerialHeader.PRESSURE_BACK,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)


def pressureSeat(payload):
	values = listToJSONString(payload)

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

	values = listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.SerialHeader.TEMPERATURE,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)
