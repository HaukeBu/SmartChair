import hal_threads

import serial_dispatcher
import os
import constants
import config
import time
import helper
import hal

def main():
    dispatcher = serial_dispatcher.SerialDispatcher()
    for header in constants.SerialHeader:
        if header.name in config.config:
            interval = int(config.config[header.name]['Interval'])
            if interval > 1:
                function = getattr(cb,
                                   helper.uppercase_to_camelcase(header.name))

                dispatcher.append_callback(header, function, interval)

    serial_port = get_serial_port()

    if (serial_port == False or
        dispatcher.initialize(serial_port, constants.SERIAL_BAUDRATE) == False):
        print("Failed to find serial port")
        return

    hal_instance = hal.HAL()
    for element in constants.GyroscopeType:
        name = "GYROSCOPE_" + element.name
        interval = int(config.config[name]['Interval'])
        address = int(config.config[name]['Address'], 16)
        if interval > 0:
            hal_instance.append_callback(address, interval)


    serial_thread = Threads.SerialThread(dispatcher)
    hal_thread = Threads.HALThread()
    message_thread = Threads.MessageThread()

    print("Start threads...")
    serial_thread.start()
    hal_thread.start()
    message_thread.start()

    serial_thread.join()
    hal_thread.join()
    message_thread.join()

def get_serial_port():
    output = os.popen("""ls /dev/ | egrep 'wchusbserial|ttyUSB'""").read()

    output_lines = output.splitlines()

    output_lines.sort()

    if len(output_lines) > 0:
        return "/dev/" + output_lines[-1]
    else:
        return False

if __name__ == "__main__":
    main()
