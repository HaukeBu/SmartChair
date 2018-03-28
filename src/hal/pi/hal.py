import gyroscope
import config
import constants
import hal_threads

class HAL():
    __instance = None

    class __impl:
        def __init__(self):
            self.interval_list = {}

        def append_callback(self, address, interval):
            print("Add new callback function for GYROSCOPE_" +
                  Constants.GyroscopeType(address).name +
                  ", Interval = " + str(interval))

            thread = Threads.GyroscopeThread(address)
            thread.start()

            self.interval_list[address] = interval

        def get_data(self, address):
            return gyroscope.Gyroscope(address).get_data()

        def get_interval_list(self):
            return self.interval_list


    def __init__(self):
        if HAL.__instance is None:
            HAL.__instance = HAL.__impl()

        self.__dict__['_Singleton__instance'] = HAL.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)
