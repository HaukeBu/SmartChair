import Threads

import SerialDispatcher as sd
import Callbacks as cb
import os

BAUDRATE = 38400
SERVER_IP = "localhost:50051"

def main():
	port = getSerialPort()

	if port == False:
		print("Failed to find serial port")
		return

	dispatcher = sd.SerialDispatcher(port, BAUDRATE)

	# Add callback functions to serial dispatcher
	dispatcher.appendCallback(Header.DEBUG, cb.debug)
	dispatcher.appendCallback(Header.DISTANCE, cb.distance)
	dispatcher.appendCallback(Header.PRESSURE_BACK, cb.pressureBack)
	dispatcher.appendCallback(Header.PRESSURE_SEAT, cb.pressureSeat)
	dispatcher.appendCallback(Header.TEMPERATURE, cb.temperature)


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
