import grpc
import time
import Queue

import chair_pb2
import chair_pb2_grpc

def build_message(version, sensor_type, values, timestamp = 0):
    timestamp = int(time.time() * 1000)

    ret_msg = chair_pb2.ChairInformation(version = version,
                                         timestamp = timestamp,
                                         sensor_type = sensor_type.value,
                                         values = values)

    return ret_msg

class GRPCQueue():
    __instance = None

    class __impl:
        def __init__(self):
            self.message_queue = Queue.Queue()

        def add_message(self, message):
            self.message_queue.put(message)

        def get_message(self):
            if not self.message_queue.empty():
                return self.message_queue.get()
            else:
                return False

    def __init__(self):
        if GRPCQueue.__instance is None:
            GRPCQueue.__instance = GRPCQueue.__impl()

        self.__dict__['_Singleton__instance'] = GRPCQueue.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)


class GRPCHandler():
    __instance = None

    class __impl:
        def __init__(self):
            self.is_initialized = False
            self.message_queue = Queue.Queue()
            self.grpc_channel = None
            self.grpc_service = None

        def initialize(self, server):
            if not self.is_initialized:
                self.grpc_channel = grpc.insecure_channel(server)
                self.grpc_service = chair_pb2_grpc.ChairServiceStub(self.grpc_channel)
                self.is_initialized = True

        def send_message(self, message):
            if self.is_initialized:
                try:
                    self.grpc_service.ChairUpdate(message)
                    return True
                except:
                    return False

    def __init__(self):
        if GRPCHandler.__instance is None:
            GRPCHandler.__instance = GRPCHandler.__impl()

        self.__dict__['_Singleton__instance'] = GRPCHandler.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)
