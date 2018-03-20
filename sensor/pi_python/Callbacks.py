import Constants
import GRPCHandler as grpc_handler
import Helper

def debug(payload):
	values = Helper.listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.GRPCHeader.DEBUG,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)

def distance(payload):
	if len(payload) != 1:
		print("distance:: payload too long " + str(len(payload)))
		return

	# Convert raw data to distance in cm
	# See: http://www.instructables.com/id/Get-started-with-distance-sensors-and-Arduino/
	payload[0] = (6762 / (payload[0] - 9)) - 4

	values = Helper.listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.GRPCHeader.DISTANCE,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)

def pressureBack(payload):
	values = Helper.listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.GRPCHeader.PRESSURE_BACK,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)


def pressureSeat(payload):
	values = Helper.listToJSONString(payload)

	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.GRPCHeader.PRESSURE_SEAT,
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
		sensor_type = Constants.GRPCHeader.TEMPERATURE,
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)

def gyroscope(address, payload):
	values = Helper.listToJSONString(payload)

	gyro_name = "GYROSCOPE_" + Constants.GyroscopeType(address).name


	message = grpc_handler.buildMessage(
		version = Constants.GRPC_VERSION,
		sensor_type = Constants.GRPCHeader[gyro_name],
		values = values
	)

	grpc_handler.GRPCQueue().addMessage(message)
