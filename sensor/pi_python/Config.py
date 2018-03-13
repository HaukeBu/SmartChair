import configparser
import Helper

config = configparser.ConfigParser()
config.optionxform = str
config.read("pi_config.ini")

if __name__ == "__main__":
	for entry in config['SERIAL']:
		name = "SERIAL_" + Helper.camelcaseToUppercase(entry)
		val = config['SERIAL'][entry]
		try:
			if "0x" in val:
				exec("%s = %d" % (name, int(val, 16)))
			else:
				exec("%s = %d" % (name, int(val)))
		except:
			exec("%s = '%s'" % (name, val))

	for entry in config['GRPC']:
		name = "GRPC_" + Helper.camelcaseToUppercase(entry)
		val = config['GRPC'][entry]
		try:
			if "0x" in val:
				exec("%s = %d" % (name, int(val, 16)))
			else:
				exec("%s = %d" % (name, int(val)))
		except:
			exec("%s = '%s'" % (name, val))


	print(SERIAL_READ_START)
