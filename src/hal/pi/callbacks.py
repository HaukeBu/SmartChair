import constants
import grpc_handler
import helper

def debug(payload):
    values = helper.list_to_json_string(payload)

    message = grpc_handler.build_message(
        version = constants.GRPC_VERSION,
        sensor_type = constants.GRPCHeader.DEBUG,
        values = values
    )

    grpc_handler.GRPCQueue().add_message(message)

def distance(payload):
    if len(payload) != 1:
        print("distance:: payload too long " + str(len(payload)))
        return

    # Convert raw data to distance in cm
    # See: http://www.instructables.com/id/Get-started-with-distance-sensors-and-Arduino/
    if payload[0] != 9:
        payload[0] = (6762 / (payload[0] - 9)) - 4
    else:
        payload[0] = 0

    values = helper.list_to_json_string(payload)

    message = grpc_handler.build_message(
        version = constants.GRPC_VERSION,
        sensor_type = constants.GRPCHeader.DISTANCE,
        values = values
    )

    grpc_handler.GRPCQueue().add_message(message)

def pressure_back(payload):
    values = helper.list_to_json_string(payload)

    message = grpc_handler.build_message(
        version = constants.GRPC_VERSION,
        sensor_type = constants.GRPCHeader.PRESSURE_BACK,
        values = values
    )

    grpc_handler.GRPCQueue().add_message(message)


def pressure_seat(payload):
    values = helper.list_to_json_string(payload)

    message = grpc_handler.build_message(
        version = constants.GRPC_VERSION,
        sensor_type = constants.GRPCHeader.PRESSURE_SEAT,
        values = values
    )

    grpc_handler.GRPCQueue().add_message(message)

def temperature(payload):
    if len(payload) != 1:
        print("temperature:: payload too long " + str(len(payload)))
        return

    values = helper.list_to_json_string(payload)

    message = grpc_handler.build_message(
        version = constants.GRPC_VERSION,
        sensor_type = constants.GRPCHeader.TEMPERATURE,
        values = values
    )

    grpc_handler.GRPCQueue().add_message(message)

def gyroscope(address, payload):
    values = helper.list_to_json_string(payload)

    gyro_name = "GYROSCOPE_" + constants.GyroscopeType(address).name


    message = grpc_handler.build_message(
        version = constants.GRPC_VERSION,
        sensor_type = constants.GRPCHeader[gyro_name],
        values = values
    )

    grpc_handler.GRPCQueue().add_message(message)
