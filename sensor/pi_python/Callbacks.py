import Constants
import GRPCHandler as grpc_handler

def listToJSONString(lst):
	ret_str = '"values": ['

	for idx in range(len(lst)):
		ret_str += '{"id": ' + str(idx) + ', "value": ' + str(lst[idx]) + '}'

		if id_num < len(id_nr) - 1:
			ret_str += ', '

	ret_str += ']'

	return ret_str

def debug(payload):
	values = listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = VERSION,
		sensor_type = Constants.Header.DEBUG,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)

def distance(payload):
	if len(payload) != 1:
		return

	values = listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = VERSION,
		sensor_type = Constants.Header.DISTANCE,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)

def pressureBack(payload):
	values = listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = VERSION,
		sensor_type = Constants.Header.PRESSURE_BACK,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)


def pressureSeat(payload):
	values = listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = VERSION,
		sensor_type = Constants.Header.PRESSURE_SEAT,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)

def temperature(payload):
	if len(payload) != 1:
		return

	values = listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = VERSION,
		sensor_type = Constants.Header.TEMPERATURE,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)
