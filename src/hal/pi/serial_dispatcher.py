import serial
import crc16
import constants
import time

SERIAL_READ_START = 0xAF
SERIAL_READ_END = 0xFE
SERIAL_SEND_START = 0xDE
SERIAL_SEND_END = 0xED

class SerialDispatcher():
    def __init__(self):
        self.callback_list = {}
        self.interval_list = {}
        self.initialized = False

    def initialize(self, port, baudrate):
        self.ser_con = serial.Serial()

        self.ser_con.port = port
        self.ser_con.baudrate = baudrate
        self.ser_con.timeout = None

        try:
            self.ser_con.open()
        except serial.SerialException:
            return False

        self.ser_con.flushOutput()
        self.ser_con.flushInput()

        time.sleep(2)

        self.__send_init_message()

        self.initialized = True

        print("Initialized serial dispatcher")

        return True

    def __send_init_message(self):
        crc_list = []
        crc_list.append(constants.SERIAL_VERSION)

        length = 0
        for _, val in self.interval_list.iteritems():
            if val > 0:
                length += 1

        crc_list.append(length)

        for idx, val in self.interval_list.iteritems():
            crc_list.append(idx)
            crc_list.append(val & 0xFF)
            crc_list.append(val >> 8)

        crc = crc16.crc16_ccitt(crc_list, len(crc_list))

        self.ser_con.write(chr(SERIAL_SEND_START))
        for val in crc_list:
            self.ser_con.write(chr(val))
        self.ser_con.write(chr(crc & 0xFF))
        self.ser_con.write(chr(crc >> 8))
        self.ser_con.write(chr(SERIAL_SEND_END))


    def append_callback(self, idx, cb, interval):
        if self.initialized:
            print("Can not append callback function when already initialized")
            return False
        else:
            self.callback_list[idx.value] = cb
            self.interval_list[idx.value] = interval
            print("Add new callback function for " + idx.name +
                  ", Interval = " + str(interval))

            return True

    def __read_byte(self):
        return ord(self.ser_con.read())

    def dispatch(self):
        # Read until start sequence occurs
        while self.__read_byte() != SERIAL_READ_START:
            time.sleep(0.01)

        buffer = []
        # Version
        buffer.append(self.__read_byte())
        # Type
        buffer.append(self.__read_byte())
        # Length
        buffer.append(self.__read_byte())

        # Payload
        for i in range(buffer[2]):
            buffer.append(self.__read_byte())

        # CRC Checksum
        crc1 = self.__read_byte()
        crc2 = self.__read_byte()
        crc = (crc2 << 8) | crc1

        last_byte = self.__read_byte()
        if last_byte != SERIAL_READ_END:
            return constants.SerialDispatchError.NO_TERMINATION_BYTE


        crc_t = crc16.crc16_ccitt(buffer, buffer[2] + 3)
        if crc != crc_t:
            return constants.SerialDispatchError.CHECKSUM_ERROR

        if buffer[0] != constants.SERIAL_VERSION:
            return constants.SerialDispatchError.VERSION_ERROR

        payload = []
        for i in range(3, len(buffer), 2):
            payload.append((buffer[i + 1] << 8) | buffer[i])

        if buffer[1] in self.callback_list:
            self.callback_list[buffer[1]](payload)
