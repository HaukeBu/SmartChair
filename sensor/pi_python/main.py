import Threads

import SerialDispatcher as sd
import Callbacks as cb
import HAL as hal

BAUDRATE = 38400

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

pi_sensors = hal.HAL()


serial_thread = Threads.SerialThread(dispatcher)
hal_thread = Threads.HALThread(pi_sensors)

serial_thread.start()
hal_thread.start()

serial_thread.join()
hal_thread.join()


def getSerialPort():
    output = os.popen("""ls /dev/ | egrep 'wchusbserial|ttyUSB'""").read()

    output_lines = output.splitlines()

    output_lines.sort()

    if len(output_lines) > 0:
        return "/dev/" + output_lines[-1]
    else:
        return False
