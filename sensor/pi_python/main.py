import Threads

import SerialDispatcher as sd
import Callbacks as cb
import os
import Constants
import Config
import time
import Helper
import HAL



def main():
	port = getSerialPort()

	if port == False:
		print("Failed to find serial port")
		return

	#Config.readConfig()

	dispatcher = sd.SerialDispatcher()

	for header in Constants.SerialHeader:
		if header.name in Config.config:
			interval = int(Config.config[header.name]['Interval'])
			if interval > 1:
				function = getattr(cb, Helper.uppercaseToCamelcase(header.name))
				dispatcher.appendCallback(header, function, interval)

	dispatcher.initialize(port, Constants.SERIAL_BAUDRATE)

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
