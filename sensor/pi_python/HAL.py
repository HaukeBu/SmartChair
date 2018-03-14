import smbus
import math

POWER_MGMT = 0x6b

GYRO_BACK_ADDRESS = 0x68
GYRO_SEAT_ADDRESS = 0x69

class HAL():
	__instance = None

	class __impl:
		def __init__(self):
			self.bus = smbus.SMBus(1)
			self.bus.write_byte_data(GYRO_BACK_ADDRESS, POWER_MGMT, 0)
			self.bus.write_byte_data(GYRO_SEAT_ADDRESS, POWER_MGMT, 0)

		def __readWord2c(self, gyro_address, reg):
			h = self.bus.read_byte_data(gyro_address, reg)
			l = self.bus.read_byte_data(gyro_address, reg + 1)
			value = (h << 8) + l

			if value >= 0x8000:
				return -((65535 - value) + 1)
			else:
				return value

		def __distance(self, a, b):
			return math.sqrt((a*a) + (b*b))

		def getGyroBack(self):
			gyro_list = []

			# Accelerator
			acc_x = self.__readWord2c(GYRO_BACK_ADDRESS, 0x3b)
			acc_y = self.__readWord2c(GYRO_BACK_ADDRESS, 0x3d)
			acc_z = self.__readWord2c(GYRO_BACK_ADDRESS, 0x3f)

			gyro_list.append(acc_x)
			gyro_list.append(acc_y)
			gyro_list.append(acc_z)

			# Gyroscope
			gyro_list.append(self.__readWord2c(GYRO_BACK_ADDRESS, 0x43))
			gyro_list.append(self.__readWord2c(GYRO_BACK_ADDRESS, 0x45))
			gyro_list.append(self.__readWord2c(GYRO_BACK_ADDRESS, 0x47))

			# Rotation
			rot_x = math.degrees(math.atan2(acc_y, self.__distance(acc_x, acc_z)))
			rot_y = math.degrees(math.atan2(acc_x, self.__distance(acc_y, acc_z)))
			rot_z = math.degrees(math.atan2(self.__distance(acc_y, acc_x), acc_z))

			gyro_list.append(rot_x)
			gyro_list.append(rot_y)
			gyro_list.append(rot_z)

			return gyro_list

		def getGyroSeat(self):
			gyro_list = []

			# Accelerator
			acc_x = self.__readWord2c(GYRO_SEAT_ADDRESS, 0x3b)
			acc_y = self.__readWord2c(GYRO_SEAT_ADDRESS, 0x3d)
			acc_z = self.__readWord2c(GYRO_SEAT_ADDRESS, 0x3f)

			gyro_list.append(acc_x)
			gyro_list.append(acc_y)
			gyro_list.append(acc_z)

			# Gyroscope
			gyro_list.append(self.__readWord2c(GYRO_SEAT_ADDRESS, 0x43))
			gyro_list.append(self.__readWord2c(GYRO_SEAT_ADDRESS, 0x45))
			gyro_list.append(self.__readWord2c(GYRO_SEAT_ADDRESS, 0x47))

			rot_x = math.degrees(math.atan2(acc_y, self.__distance(acc_x, acc_z)))
			rot_y = math.degrees(math.atan2(acc_x, self.__distance(acc_y, acc_z)))
			rot_z = math.degrees(math.atan2(self.__distance(acc_y, acc_x), acc_z))

			# Rotation
			gyro_list.append(rot_x)
			gyro_list.append(rot_y)
			gyro_list.append(rot_z)

			return gyro_list

	def __init__(self):
		if HAL.__instance is None:
			HAL.__instance = HAL.__impl()

		self.__dict__['_Singleton__instance'] = HAL.__instance

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self.__instance, attr, value)
