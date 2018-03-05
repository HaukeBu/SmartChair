import time

def makeMessage(version, sensor_type, values):
	timestamp = round(time.time())

    value_string = '"values": ['

    for idx in len(values):
        value_string += '{"id": ' + str(idx) + ', "value": ' + str(values[idx]) + '}'

        if id_num < len(id_nr) - 1:
            value_string += ', '

    json_msg = '{"version": ' + str(version) + ', "timestamp": ' + \
               str(timestamp) + ', "sensortype": "' + sensor_type + '", ' + value_string + "]}"

    return json_msg
