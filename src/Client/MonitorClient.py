from twisted.spread import pb
from twisted.internet import reactor
import time
import sys, os
import subprocess
import threading
import _thread
'''
#2020-02-28 AB: Client Class running within MORPHEUS
'''
def main():
    # mc = MonitorClientBroker()
    # factory = pb.PBClientFactory()
    # reactor.connectTCP("localhost", 8800, factory)
    # factory.getRootObject().addCallback(mc.connect)
    # reactor.run()
    mc = MonitorClient()
    # mc.start()
    try:
        mc.runClient()
        while(True):
            print("____________________ Test Ping _________________")
            time.sleep(2)
            mc.ping()
            print("____________________ Test get_data  _________________")
            time.sleep(2)
            mc.get_data()
    except Exception as e:
        print(e)

class MonitorClient:
    '''
    2021-02-28 AB: Class responsible of communicating with monitorserver though contolling the client boker
    '''
    def __init__(self):
        self.mcb = MonitorClientBroker()
        self.factory = pb.PBClientFactory()
        self.reactor = reactor

        #TODO: INSTANTIATE QUEUE
        self.queue = []
    '''
    2021-02-28 AB: Run the Client in sequential mode
    '''
    def start(self):
        '''
        2021-02-28 AB: Runs the Client in sequential mode (main)
        '''
        self.reactor.connectTCP("localhost", 8800, self.factory)
        self.factory.getRootObject().addCallback(self.mcb.connect)
        self.reactor.run()

    def runClient(self):
        '''
        2021-02-28 AB: Runs the Client within a thead (threaded mode)
        '''
        try:
            # self.scopeClientBroker = ScopeClientBroker()
            # factory = pb.PBClientFactory()
            reactor.connectTCP("localhost", 8800, self.factory)
            self.factory.getRootObject().addCallback(self.mcb.connect)
            threading.Thread(target=reactor.run, args=(False,)).start()
            print("ClientSIDE REACTOR LAUNCH {}".format(time.time()))
        except Exception as e :
            print("error occured in runClient: {}".format(e) )
        finally:
            print("leaving runClient()")

        started = False
        time.sleep(1)


    def ping(self):
        self.mcb.ping_server()
        while (self.mcb.ping_recieved != True):
            time.sleep(1)
            print("awaiting sever ping response")
        if self.mcb.ping_recieved:
            self.ping_ms = self.mcb.ping_resp_time - self.mcb.ping_req_time
        print("PING = {}".format(self.ping_ms))

    def get_data(self):
        '''
        2021-02-28 AB: calls getData to get sensor info
        '''
        self.mcb.get_data()

        while(self.mcb.data_recieved != True):
            time.sleep(0.5) #do nothin
        if self.mcb.status['data'] == 'success':
            print(" Recieved serve data PROBE={} , BED={}, HB={}".format(self.mcb.probe, self.mcb.bed, self.mcb.hb))
            #TODO:
            '''
            add data to Queue
            make dictionary
            d= {}
            d['time'] = time.time()
            d['probe']
            .
            .
            add to self.queue



            '''
            data = {}
            data['time'] = time.time()
            data['probe'] = self.mcb.probe
            data['bed'] = self.mcb.bed
            data['hb'] = self.mcb.hb
            self.addToQueue(data)
            self.getQueue()



        else:
            print("Something went wrong in remote getData()")



## TODO ADD_TOQUEUE
    def addToQueue(self, dictionary):
        self.queue.append(dictionary)


## FUNCTION: GET_QUEUE
    def getQueue(self):
        dataTemp = self.queue.pop(0)
        print(" Queue server data PROBE={} , BED={}, HB={}".format(dataTemp['probe'], dataTemp['bed'], dataTemp['hb']))
        return dataTemp


class MonitorClientBroker:
    '''
    2021-02-28 AB: Class responsible for direct communication with server
    '''
    def __init__(self):
        self.server_ref = None
        self.status={}

        self.ping_recieved = False
        self.ping_resp_time = 0
        self.ping_req_time = 0

        self.probe = 0
        self.bed = 0
        self.hb = 0
    def connect(self, obj):
        #store the server refrence
        self.server_ref = obj
        print("Attempting Connection with server...")
        self.server_ref.callRemote("connect").addCallback(self.connect_cb)

    def connect_cb(self, stat):
        print("client connection successfully established.")


    def ping_server(self):
        '''
        2021-02-28 AB: Ping the Server
        '''
        self.ping_recieved = False
        self.server_ref.callRemote("ping", self.status).addCallback(self.ping_cb)
        self.ping_req_time = time.time()

    def ping_cb(self,stat):
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

    def get_data_cb(self, stat ):
        '''
        2021-02-28 AB: Call back for recieving data
        '''
        self.status= stat
        if stat['data'] == 'success':
            self.probe = stat['data_probe']
            self.hb = stat['data_hb']
            self.bed = stat['data_bed']

        self.data_recieved = True

    def step2(self, two):
        print("got two object:" + str( two))
        print("giving it back to one")
        print("one is" + str( self.server_ref))
        self.server_ref.callRemote("checkTwo", two)

main()
