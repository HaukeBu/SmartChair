from enum import Enum

VERSION = 1

class SerialHeader(Enum):
	DEBUG = 0
	DISTANCE = 1
	PRESSURE_BACK = 2
	PRESSURE_SEAT = 3
	TEMPERATURE = 4

class SerialDispatchError(Enum):
	NO_TERMINATION_BYTE = 1
	CHECKSUM_ERROR = 2
	VERSION_ERROR = 3
