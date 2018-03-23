import configparser
import Helper

config = configparser.ConfigParser()
config.optionxform = str
config.read("pi_config.ini")
