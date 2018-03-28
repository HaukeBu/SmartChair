import smbus
import math
import constants
from threading import Lock
import time

GYRO_CONFIG_POWER = 0x6B
GYRO_CONFIG_LOWPASS = 0x1A
GYRO_CONFIG_FULL_SCALE = 0x1B
GYRO_CONFIG_SAMPLE_RATE = 0x19

GYRO_ACC_X = 0
GYRO_ACC_Y = 1
GYRO_ACC_Z = 2
GYRO_X = 3
GYRO_Y = 4
GYRO_Z = 5

class Gyroscope():
    __instances = {}

    class __impl:
        def __init__(self, address):
            self.bus = smbus.SMBus(1)
            self.address = address

            self.values = []
            self.values_mutex = Lock()

            self.gyro_x = 0
            self.gyro_y = 0
            self.gyro_z = 0

            self.x_offset = -281.00
            self.y_offset = 18.00
            self.z_offset = -83.00

            self.initialized = False

        def initialize(self):
            if self.initialized:
                return

            self.bus.write_byte_data(self.address, GYRO_CONFIG_POWER, 0)

            self.bus.write_byte_data(self.address, GYRO_CONFIG_LOWPASS, 0x01)

            self.bus.write_byte_data(self.address, GYRO_CONFIG_FULL_SCALE, 0x08)

            sample_div = int(1000 / constants.GYRO_SAMPLE_FREQUENCY - 1)
            self.bus.write_byte_data(self.address, GYRO_CONFIG_SAMPLE_RATE,
                                      sample_div)

            self.__calibrate()

            self.initialized = True

        def acquire_data(self):
            if not self.initialized:
                return -1
            else:
                self.values_mutex.acquire()

            sample_freq = constants.GYRO_SAMPLE_FREQUENCY
            start_time = round(time.time() * 1000)

            self.values[:] = []

            self.__read_data()

            gyro_list = self.values

            distance = self.__distance(gyro_list[GYRO_ACC_Y],
                                       gyro_list[GYRO_ACC_Z])
            ay = math.degrees(math.atan2(gyro_list[GYRO_ACC_X], distance))

            distance = self.__distance(gyro_list[GYRO_ACC_X],
                                       gyro_list[GYRO_ACC_Z])
            ax = math.degrees(math.atan2(gyro_list[GYRO_ACC_Y], distance))

            self.gyro_x = self.gyro_x + gyro_list[GYRO_X] / sample_freq
            self.gyro_y = self.gyro_y - gyro_list[GYRO_Y] / sample_freq
            self.gyro_z = self.gyro_z + gyro_list[GYRO_Z] / sample_freq

            self.gyro_x = self.gyro_x*0.96 + ax*0.04
            self.gyro_y = self.gyro_y*0.96 + ay*0.04

            gyro_list.append(self.gyro_x)
            gyro_list.append(self.gyro_y)
            gyro_list.append(self.gyro_z)

            end_time = round(time.time() * 1000)
            self.values_mutex.release()

            sleep_time = ((1.0 / sample_freq) * 1000.0)
            sleep_time = sleep_time - (end_time - start_time)
            sleep_time = sleep_time / 1000

            if sleep_time <= 0:
                sleep_time = 0

            return sleep_time

        def get_data(self):
            if not self.initialized:
                return []

            self.values_mutex.acquire()
            ret = self.values
            self.values_mutex.release()

            return ret

        def __calibrate(self):
            x_offset = 0.0
            y_offset = 0.0
            z_offset = 0.0

            for i in range(constants.GYRO_CALIBRATION_LOOP):
                x_offset += self.__read_word(0x43)
                y_offset += self.__read_word(0x45)
                z_offset += self.__read_word(0x47)


            self.x_offset = x_offset / constants.GYRO_CALIBRATION_LOOP
            self.y_offset = y_offset / constants.GYRO_CALIBRATION_LOOP
            self.z_offset = z_offset / constants.GYRO_CALIBRATION_LOOP


        def __read_data(self):
            sensitivity = constants.GYRO_SENSITIVITY

            # Accelerometer
            self.values.append(self.__read_word(0x3b))
            self.values.append(self.__read_word(0x3d))
            self.values.append(self.__read_word(0x3f))

            # Gyroscope
            x = (self.__read_word(0x43) - self.x_offset) / sensitivity
            y = (self.__read_word(0x45) - self.y_offset) / sensitivity
            z = (self.__read_word(0x47) - self.z_offset) / sensitivity

            self.values.append(x)
            self.values.append(y)
            self.values.append(z)

        def __read_word(self, reg):
            h = self.bus.read_byte_data(self.address, reg)
            l = self.bus.read_byte_data(self.address, reg + 1)
            value = (h << 8) + l

            ret = 0.0
            if value >= 0x8000:
                ret = -((65535 - value) + 1)
            else:
                ret = value

            return ret * 1.0

        def __distance(self, a, b):
            return math.sqrt(a*a + b*b)

    def __init__(self, address):
        if address not in Gyroscope.__instances:
            Gyroscope.__instances[address] = Gyroscope.__impl(address)

        self.__address = address

    def __getattr__(self, attr):
        return getattr(self.__instances[self.__address], attr)
