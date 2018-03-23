import Threads

import SerialDispatcher as sd
import Callbacks as cb
import os
import Constants
import Config
import time
import Helper
import HAL as hal


def main():
	dispatcher = sd.SerialDispatcher()
	for header in Constants.SerialHeader:
		if header.name in Config.config:
			interval = int(Config.config[header.name]['Interval'])
			if interval > 1:
				function = getattr(cb, Helper.uppercaseToCamelcase(header.name))
				dispatcher.appendCallback(header, function, interval)

	serial_port = getSerialPort()

	if serial_port == False or dispatcher.initialize(serial_port, Constants.SERIAL_BAUDRATE) == False:
		print("Failed to find serial port")
		return

	hal_instance = hal.HAL()
	for element in Constants.GyroscopeType:
		name = "GYROSCOPE_" + element.name
		interval = int(Config.config[name]['Interval'])
		address = int(Config.config[name]['Address'], 16)
		if interval > 0:
			hal_instance.addCallback(address, interval)


	serial_thread = Threads.SerialThread(dispatcher)
	hal_thread = Threads.HALThread()
	message_thread = Threads.MessageThread()

	serial_thread.start()
	hal_thread.start()
	message_thread.start()

	serial_thread.join()
	hal_thread.join()
	message_thread.join()


def getSerialPort():
	output = os.popen("""ls /dev/ | egrep 'wchusbserial|ttyUSB'""").read()

	output_lines = output.splitlines()

	output_lines.sort()

	if len(output_lines) > 0:
		return "/dev/" + output_lines[-1]
	else:
		return False

if __name__ == "__main__":
	main()
