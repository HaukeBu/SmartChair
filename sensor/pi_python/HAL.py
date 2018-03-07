import Gyroscope as gy

class HAL():
	def getGyro(self):
		return gy.get_gyro_values()
