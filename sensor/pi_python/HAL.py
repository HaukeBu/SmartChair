import Gyroscope as gy
import Config

class HAL():
	__instance = None

	class __impl:
		def __init__(self):
			self.interval_list = {}

		def addCallback(self, address, interval):
			print("Add new callback function for GYROSCOPE_"
					+ GyroscopeType(address).name +
					", Interval = " + interval)

			thread = gy.GyroscopeThread(back_info['Address'])
			thread.start()

			self.interval_list[address] = interval

		def getData(self, address):
			return gy.Gyroscope(address).getData()

		def getIntervalList(self):
			return self.interval_list


	def __init__(self):
		if HAL.__instance is None:
			HAL.__instance = HAL.__impl()

		self.__dict__['_Singleton__instance'] = HAL.__instance

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self.__instance, attr, value)
