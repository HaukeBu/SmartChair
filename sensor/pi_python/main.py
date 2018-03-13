import Threads

import SerialDispatcher as sd
import Callbacks as cb
import os
import Constants
import time



def main():
	port = getSerialPort()

	if port == False:
		print("Failed to find serial port")
		return

	dispatcher = sd.SerialDispatcher()

	# Add callback functions to serial dispatcher
	dispatcher.appendCallback(Constants.SerialHeader.DEBUG, cb.debug, 10)
	dispatcher.appendCallback(Constants.SerialHeader.DISTANCE, cb.distance, 100)
	dispatcher.appendCallback(Constants.SerialHeader.PRESSURE_BACK, cb.pressureBack, 200)
	dispatcher.appendCallback(Constants.SerialHeader.PRESSURE_SEAT, cb.pressureSeat, 1000)
	dispatcher.appendCallback(Constants.SerialHeader.TEMPERATURE, cb.temperature, 500)

	dispatcher.initialize(port, Constants.SERIAL_BAUDRATE)

	serial_thread = Threads.SerialThread(dispatcher)
	#hal_thread = Threads.HALThread()
	message_thread = Threads.MessageThread()

	serial_thread.start()
	#hal_thread.start()
	message_thread.start()

	serial_thread.join()
	#hal_thread.join()
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
