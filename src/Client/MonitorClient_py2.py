from twisted.spread import pb
from twisted.internet import reactor, threads
from collections import deque
import sys
import time
import threading
import random
'''
#2020-02-28 AB: Client Class running within MORPHEUS
'''

HOST_IP = '192.168.137.239'
HOST_PORT = 8800
class MonitorClientBroker:
    '''
    2021-02-28 AB: Class responsible for direct communication with server
    '''

    def __init__(self):
        self.server_ref = None
        self.status={}
        # Flags for waiting
        self.ping_recieved = False
        self.temp_set = False
        self.data_recieved = False

        self.ping_resp_time = 0
        self.ping_req_time = 0

        self.probe = 0
        self.bed = 0
        self.hb = 0

    def connect(self, obj):
        # store the server refrence
        self.server_ref = obj
        print("Attempting Connection with server...")
        self.server_ref.callRemote("register").addCallback(self.connect_cb)

    def connect_cb(self, stat):
        print("client connection successfully established.")

    def ping_server(self):
        '''
        2021-02-28 AB: Ping the Server
        '''
        self.ping_recieved = False
        self.server_ref.callRemote("ping", self.status).addCallback(self.ping_cb)
        self.ping_req_time = time.time()

    def ping_cb(self, stat):
        '''
        2021-02-28 AB: Call back for ping
        '''
        self.ping_resp_time = time.time()
        if stat['ping'] == 'success':
            print("ping retuned successfully")
        self.ping_recieved = True

    def get_data(self):
        self.data_recieved = False
        self.server_ref.callRemote("getData", self.status).addCallback(self.get_data_cb)

    def get_data_cb(self, stat):
        '''
        2021-02-28 AB: Call back for recieving data
        '''
        self.status = stat
        if stat['data'] == 'success':
            self.probe = stat['data_probe']
            self.hb = stat['data_hb']
            self.bed = stat['data_bed']

        self.data_recieved = True

    def set_temp(self, new_temp):
        self.status['set_temp'] = "not"
        self.server_ref.callRemote("setTemp", self.status, new_temp).addCallback(self.set_temp_cb)

    def set_temp_cb(self, stat):
        if stat['set_temp'] == 'success':
            print("new temp setting successful. ")
        else:
            print("failed to set temp on server side")
        self.temp_set = True

    def step2(self, two):
        print("got two object:" + str(two))
        print("giving it back to one")
        print("one is" + str(self.server_ref))
        self.server_ref.callRemote("checkTwo", two)


class DataReciver(pb.Referenceable):

    def __init__(self, maxlen=10):
        self.data = deque(maxlen=maxlen)

    def remote_transfer(self, data):
        print(self.data)
        self.data.appendleft(data)

    def get(self):

        return self.data.pop()

class MonitorClient:
    '''
    2021-02-28 AB: Class responsible of communicating with monitorserver though contolling the client boker
    '''

    def __init__(self, data_reciever):
        self.factory = pb.PBClientFactory()
        self.data_reciever = data_reciever
        self.uuid = None

    def connect(self, host="192.168.137.239", port=8800):
        '''
        2021-02-28 AB: Runs the Client in sequential mode (main)
        '''
        reactor.connectTCP(host, port, self.factory)
        self.factory.getRootObject().addCallback(self._client_connected)
        reactor.run()

    def connect_threaded(self, other_threads, *args, **kwargs):
        print(args,kwargs)
        threads.callMultipleInThread(other_threads)
        self.connect(*args, **kwargs)

    def _client_connected(self, obj):
        self.server = obj

        d = self.server.callRemote("register", self.data_reciever)
        d.addCallback(self._recv_register)

    def _recv_register(self, uuid):
        print("UUID: {}".format(uuid))
        self.uuid = uuid

    def _disconnect(self):
        try:
            return self.server.callRemote("unregister", self.uuid)
        except pb.DeadReferenceError:
            print("Could not disconnect stale connection")

    def quit(self):
        d = self.server.callRemote("unregister", self.uuid)
        if d:
            d.addCallback(self._recv_unregister)

    def _recv_unregister(self, _):
        print("Unregistered from server")
        reactor.callFromThread(reactor.stop)

    def ping(self):
        self.server.callRemote("ping", time.time()).addCallback(self._recv_ping)

    def _recv_ping(self, args):
        call_time, server_recv_time = args
        t = time.time()
        print("To Server Delay: {}".format(server_recv_time - call_time))
        print("RTT: {}".format(t - call_time))

    def start_transfer(self):
        """WIP"""
        self.server.callRemote("start_transfer", self.uuid)

    def stop_transfer(self):
        """WIP"""
        self.server.callRemote("stop_transfer", self.uuid)
    def pprint(*args, **kwargs):
        print(args,kwargs)

    def fetch_data(self, callback=pprint):
        self.server.callRemote("get_data", self.uuid).addCallback(callback)



    def runClient(self):
        '''
        2021-02-28 AB: Runs the Client within a thead (threaded mode)
        '''
        try:
            # self.scopeClientBroker = ScopeClientBroker()
            # factory = pb.PBClientFactory()
            reactor.connectTCP("192.168.137.239", 8800, self.factory)
            self.factory.getRootObject().addCallback(self.mcb.connect)
            threading.Thread(target=reactor.run, args=(False,)).start()
            print("ClientSIDE REACTOR LAUNCH {}".format(time.time()))
        except Exception as e:
            print("error occured in runClient: {}".format(e))
        finally:
            print("leaving runClient()")

        time.sleep(1)

    def set_data(self, new_data):
        d = self.server.callRemote("set_data", new_data)
        d.addCallback(self._recv_set_data)

    def _recv_set_data(self, server_resp):
        print("temp_set: {}".format(server_resp))

def _mock_main_thread(mc):
    print("This is the mock main")
    while True:
        action = input(">>> ")
        if action == "ping":
            reactor.callFromThread(mc.ping)
        elif action == "start":
            reactor.callFromThread(mc.start_transfer)
            time.sleep(1)
            reactor.callFromThread(mc.start_transfer)
        elif action == "data":
            reactor.callFromThread(mc.fetch_data)
        elif "set" in action:
            reactor.callFromThread(
                mc.set_data, int("".join(action.split()[1:])))
        elif action == "quit":
            reactor.callFromThread(mc.quit)
            break
    print("finished")


def main2():
    dr = DataReciver()
    mc = MonitorClient(dr)
    mc.connect_threaded([(_mock_main_thread, (mc,), {}, )])

if __name__ == "__main__":
    main2()
