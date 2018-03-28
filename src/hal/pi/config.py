import configparser

parsed_config = configparser.ConfigParser()
parsed_config.optionxform = str
parsed_config.read("pi_config.ini")
