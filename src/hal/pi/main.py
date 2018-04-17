import hal_threads

import serial_dispatcher
import callbacks
import os
import constants
import config
import time
import helper
import hal

def main():
    dispatcher = serial_dispatcher.SerialDispatcher()
    for header in constants.SerialHeader:
        if header.name in config.parsed_config:
            interval = int(config.parsed_config[header.name]['Interval'])
            if interval > 1:
                function = getattr(callbacks, header.name.lower())

                dispatcher.append_callback(header, function, interval)

    serial_port = get_serial_port()

    if (serial_port == False or
        dispatcher.initialize(serial_port, constants.SERIAL_BAUDRATE) == False):
        print("Failed to find serial port")
        return

    hal_instance = hal.HAL()
    for element in constants.GyroscopeType:
        name = "GYROSCOPE_" + element.name
        interval = int(config.parsed_config[name]['Interval'])
        address = int(config.parsed_config[name]['Address'], 16)
        if interval > 0:
            hal_instance.append_callback(address, interval)


    serial_thread = hal_threads.SerialThread(dispatcher)
    hal_thread = hal_threads.HALThread()
    message_thread = hal_threads.MessageThread()

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
