import smbus
import math

POWER_MGMT = 0x6b

GYRO_BACK_ADDRESS = 0x68
GYRO_SEAT_ADDRESS = 0x69

class HAL():
	__instance = None

	class __impl:
		def __init__(self):
			bus = smbus.SMBus(1)
			bus.write_byte_data(GYRO_BACK_ADDRESS, POWER_MGMT, 0)
			bus.write_byte_data(GYRO_SEAT_ADDRESS, POWER_MGMT, 0)

		def __readWord2c(self, gyro_address, reg):
			h = bus.read_byte_data(gyro_address, reg)
			l = bus.read_byte_data(gyro_address, reg + 1)
			value = (h << 8) + l

			if value >= 0x8000:
				return -((65535 - value) + 1)
			else:
				return value

		def getGyroBack(self):
			gyro_list = []

			# Accelerator
			gyro_list.append(self.__readWord2c(GYRO_BACK_ADDRESS, 0x3b))
			gyro_list.append(self.__readWord2c(GYRO_BACK_ADDRESS, 0x3d))
			gyro_list.append(self.__readWord2c(GYRO_BACK_ADDRESS, 0x3f))

			# Gyroscope
			gyro_list.append(self.__readWord2c(GYRO_BACK_ADDRESS, 0x43))
			gyro_list.append(self.__readWord2c(GYRO_BACK_ADDRESS, 0x45))
			gyro_list.append(self.__readWord2c(GYRO_BACK_ADDRESS, 0x47))

			return gyro_list

		def getGyroSeat(self):
			gyro_list = []

			# Accelerator
			gyro_list.append(self.__readWord2c(GYRO_SEAT_ADDRESS, 0x3b))
			gyro_list.append(self.__readWord2c(GYRO_SEAT_ADDRESS, 0x3d))
			gyro_list.append(self.__readWord2c(GYRO_SEAT_ADDRESS, 0x3f))

			# Gyroscope
			gyro_list.append(self.__readWord2c(GYRO_SEAT_ADDRESS, 0x43))
			gyro_list.append(self.__readWord2c(GYRO_SEAT_ADDRESS, 0x45))
			gyro_list.append(self.__readWord2c(GYRO_SEAT_ADDRESS, 0x47))

			return gyro_list

	def __init__(self):
		if HAL.__instance is None:
			HAL.__instance = HAL.__impl()

		self.__dict__['_Singleton__instance'] = HAL.__instance

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self.__instance, attr, value)
