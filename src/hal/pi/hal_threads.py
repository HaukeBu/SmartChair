import threading
import grpc_handler
import time
import hal
import constants
import callbacks
import gyroscope
import sys

class MessageThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        queue = grpc_handler.GRPCQueue()
        handler = grpc_handler.GRPCHandler()

        handler.initialize(constants.GRPC_SERVER_IP)

        print("Message thread started")
        while True:
            message = queue.get_message()
            if type(message) != type(False):
                for i in range(constants.GRPC_FAIL_RETRY):
                    if handler.send_message(message):
                        break

class SerialThread(threading.Thread):
    def __init__(self, serial):
        threading.Thread.__init__(self)
        self.daemon = True

        self.ser_dispatcher = serial

    def run(self):
        print("Serial thread started")
        while True:
            self.ser_dispatcher.dispatch()

class HALThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        self.hal_instance = hal.HAL()
        self.interval_list = self.hal_instance.get_interval_list()

        self.next_wakeup = {}
        for address, val in self.interval_list.iteritems():
            self.next_wakeup[int(address)] = 0


    def __get_millis(self):
        return int(round(time.time() * 1000))

    def __sleep_time(self):
        ret = sys.maxint

        for address, wakeup in self.next_wakeup.iteritems():
            if ret > (wakeup - self.__get_millis()):
                ret = wakeup - self.__get_millis()

        return max(0, ret / 1000)

    def run(self):
        if self.interval_list:
            print("HAL thread started")
            while True:
                for address, interval in self.interval_list.iteritems():
                    if self.next_wakeup[int(address)] <= self.__get_millis():
                        sensor_data = self.hal_instance.get_data(address)

                        callbacks.gyroscope(address, sensor_data)

                        self.next_wakeup[address] = interval + self.__get_millis()

                time.sleep(self.__sleep_time())

class GyroscopeThread(threading.Thread):
    def __init__(self, address):
        threading.Thread.__init__(self)
        self.daemon = True

        self.address = address
        self.gyroscope = gyroscope.Gyroscope(address)

    def run(self):
        self.gyroscope.initialize()

        print("Gyroscope thread with address " + str(self.address) + " started")
        while True:
            sleep_time = self.gyroscope.acquire_data()
            if sleep_time > 0:
                time.sleep(sleep_time)
