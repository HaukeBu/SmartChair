import smbus
import math

# Power Management
power_mgmt_1 = 0x6b

# detect sudo i2cdetect -y 1
gyro_address_first = 0x68
gyro_address_second = 0x69


bus = smbus.SMBus(1)
bus.write_byte_data(gyro_address_first, power_mgmt_1, 0)
bus.write_byte_data(gyro_address_second, power_mgmt_1, 0)


def read_word_2c(gyro_address, reg):
	h = bus.read_byte_data(gyro_address, reg)
	l = bus.read_byte_data(gyro_address, reg + 1)
	value = (h << 8) + l

	if value >= 0x8000:
		return -((65535 - value) + 1)
	else:
		return value


def get_gyro_values():
	gyro_list = []

	# Accelerator
	gyro_list.append(read_word_2c(gyro_address_first, 0x3b)
	gyro_list.append(read_word_2c(gyro_address_first, 0x3d)
	gyro_list.append(read_word_2c(gyro_address_first, 0x3f)
	gyro_list.append(read_word_2c(gyro_address_second, 0x3b)
	gyro_list.append(read_word_2c(gyro_address_second, 0x3d)
	gyro_list.append(read_word_2c(gyro_address_second, 0x3f)

	# Gyroscope
	gyro_list.append(read_word_2c(gyro_address_first, 0x43))
	gyro_list.append(read_word_2c(gyro_address_first, 0x45))
	gyro_list.append(read_word_2c(gyro_address_first, 0x47))
	gyro_list.append(read_word_2c(gyro_address_second, 0x43))
	gyro_list.append(read_word_2c(gyro_address_second, 0x45))
	gyro_list.append(read_word_2c(gyro_address_second, 0x47))

	return gyro_list
