from twisted.spread import pb
from twisted.internet import reactor
import time
import random

'''
#2020-02-28 AB: Animal monitor server class to be run on the Raspberry Pi
'''
class SensorData(pb.Referenceable):
    def remote_print(self, arg):
        print("two.print was given", arg)

class MonitorServer(pb.Root):
    def __init__(self, sd):
        #pb.Root.__init__(self)   # pb.Root doesn't implement __init__
        self.sensor_data = sd
        self.status = {}

        self.t= 37
        self.hb=50
    def remote_connect(self):
        print("Connection Request Recieved")
        self.status['connect'] = 'success'
        return self.status

    def remote_getData(self):
        print ("Returning Sensor Data"+str( self.sensor_data))
        return self.sensor_data

    def remote_checkTwo(self, newtwo):
        print("One.checkTwo(): comparing my two" + str(self.sensor_data))
        print("One.checkTwo(): against your two" + str( newtwo))
        if self.sensor_data == newtwo:
            print("One.checkTwo(): our twos are the same")

    def remote_ping(self, stat):
        '''
        2021-02-28 AB: return a simple message for ping measurement
        '''

        print("server recieved ping request")
        self.status = stat
        self.status['ping'] = 'success'
        return self.status

    def remote_getData(self, stat):
        '''
        2021-02-28 AB: Return Sensor Data
        '''
        self.status['data'] = 'success'
        self.status['data_probe'] = random.randint(30,40)
        self.status['data_hb'] = random.randint(60,80)
        self.status['data_bed'] = random.randint(40,50)

        return self.status


sd = SensorData()
root_obj = MonitorServer(sd)
try:
    reactor.listenTCP(8800, pb.PBServerFactory(root_obj))
except Exception as e:
    print("Issue with connecting TCP")
    print(e)
    return
try:
    reactor.run()
except Exception as e1:
    print("Issue with Runnign reactor")
    print(e1)
    return
