import sys
from twisted.spread import pb
from twisted.internet import reactor, threads
from abc import ABC, abstractmethod
import time
from threading import Event
from uuid import uuid1
from random import randint

'''
#2020-02-28 AB: Animal monitor server class to be run on the Raspberry Pi
'''
HOST_IP = '10.0.0.126'


class MockController():
    def set(self, vals):
        print("setting", vals)
        return True

class MockDataProducer():
    def __iter__(self):
        return self

    def __next__(self):
        return {"Val_A": randint(1, 100)}


class MonitorServer(pb.Root):

    def __init__(self, data_producer, controller):
        self.data_producer = data_producer
        self.controller = controller
        self.clients = {}

    def start_server_threaded(self, other_threads, *args, **kwargs):
        threads.callMultipleInThread(other_threads)
        self.start_server(*args, **kwargs)

    def start_server(self, host_port=8800):
        print("server started")
        reactor.listenTCP(host_port, pb.PBServerFactory(self))
        reactor.run()

    def remote_register(self, obj):
        uuid = str(uuid1())

        self.clients[uuid] = {
            "obj": obj,
            "stop": Event(),
        }
        print(f"Registered: {uuid}")
        return uuid

    def remote_unregister(self, uuid):
        print(f"Unregistered: {uuid}")
        self.clients[uuid]["stop"].set()

    def remote_start_transfer(self, uuid):
        self.clients[uuid]["stop"].clear()
        reactor.callInThread(self._send_data, uuid)

    def _send_data(self, uuid):
        def _send_data_err_callback(self, reason):
            self.clients[uuid]["stop"].set()
        try:
            for data in self.data_producer:
                if uuid not in list(self.clients) or\
                   not self.clients[uuid] or\
                   self.clients[uuid]["stop"].is_set():
                    break
                d = self.clients[uuid]["obj"].callRemote("transfer", data)
                d.addErrback(_send_data_err_callback)
        except pb.DeadReferenceError:
            print("stale reference: the client disconnected or crashed")
        except Exception as e:
            import traceback
            print("e:", e)
            traceback.print_exc()

    def remote_get_data(self, _):
        return next(self.data_producer)

    def remote_set_data(self, vals):
        return self.controller.set(vals)

    def remote_stop_transfer(self, uuid):
        if uuid in self.clients:
            self.clients[uuid]["run"].set()
            return True
        else:
            return False

    def remote_ping(self, call_time):
        '''
        2021-02-28 AB: return a simple message for ping measurement
        '''
        server_time = time.time()
        print(f"Server recive time: {server_time - call_time}")
        return call_time, server_time



def _mock_main_thread():
    print("This is the mock main")


if __name__ == "__main__":
    # s = ArduinoSensors()
    # s.start()
    ms = MonitorServer(MockDataProducer(), MockController())
    ms.start_server_threaded([(_mock_main_thread, tuple(), {}, )])
    # ms.start_server()
    print("started server threaded")
