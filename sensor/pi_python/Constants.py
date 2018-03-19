from enum import Enum
import Config
import Helper

for entry in Config.config['SERIAL']:
	name = "SERIAL_" + Helper.camelcaseToUppercase(entry)
	val = Config.config['SERIAL'][entry]
	try:
		if "0x" in val:
			exec("%s = %d" % (name, int(val, 16)))
		else:
			exec("%s = %d" % (name, int(val)))
	except:
		exec("%s = '%s'" % (name, val))

for entry in Config.config['GRPC']:
	name = "GRPC_" + Helper.camelcaseToUppercase(entry)
	val = Config.config['GRPC'][entry]
	try:
		if "0x" in val:
			exec("%s = %d" % (name, int(val, 16)))
		else:
			exec("%s = %d" % (name, int(val)))
	except:
		exec("%s = '%s'" % (name, val))

for entry in Config.config['GYROSCOPE']:
	name = "GYRO_" + Helper.camelcaseToUppercase(entry)
	val = Config.config['GYROSCOPE'][entry]
	try:
		if "0x" in val:
			exec("%s = %d" % (name, int(val, 16)))
		else:
			exec("%s = %d" % (name, int(val)))
	except:
		exec("%s = '%s'" % (name, val))

class SerialHeader(Enum):
	DEBUG = 0
	DISTANCE = 1
	PRESSURE_BACK = 2
	PRESSURE_SEAT = 3
	TEMPERATURE = 4

class GRPCHeader(Enum):
	DEBUG = 0
	DISTANCE = 1
	PRESSURE_BACK = 2
	PRESSURE_SEAT = 3
	TEMPERATURE = 4
	GYROSCOPE_BACK = 5
	GYROSCOPE_SEAT = 6

class GyroscopeType(Enum):
	BACK = 0x68
	SEAT = 0x69

class SerialDispatchError(Enum):
	NO_TERMINATION_BYTE = 1
	CHECKSUM_ERROR = 2
	VERSION_ERROR = 3
	CALLBACK_FUNCTION_NOT_EXISTENT = 4
