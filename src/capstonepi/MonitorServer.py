from twisted.spread import pb
from twisted.internet import reactor
import time
import random
from HardwareSensors import ArduinoSensors

'''
#2020-02-28 AB: Animal monitor server class to be run on the Raspberry Pi
'''
HOST_PORT = 8800
HOST_IP = '10.0.0.126'


class SensorData(pb.Referenceable):
    def remote_print(self, arg):
        print("two.print was given", arg)

class MonitorServer(pb.Root):
    def __init__(self, sd, arduino_sensors):
        #pb.Root.__init__(self)   # pb.Root doesn't implement __init__
        self.sensor_data = sd
        self.status = {}
        self.sensors = arduino_sensors
        self.set_t = -1
        
    def start_server_thread(self):
        #Todo start server in thread
        pass

    def run_server(self):
        #Run server 
        pass 

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
        self.status['data_probe'] = self.sensors.get_temp()
        self.status['data_hb'] = self.sensors.get_hb()
        self.status['data_bed'] = self.sensors.get_k_temp()

        return self.status
    def remote_setTemp(self, stat,nt):
        if nt != self.set_t:
            self.status['set_temp'] = 'success'
            self.set_t = nt
            print("new temp setting request Tnew= {}".format(self.set_t))
        else:
            print("Failed to recieved new set temp")
            self.status['set_temp'] = 'fail'

        return self.status

sd = SensorData()
s = ArduinoSensors()
s.start()
root_obj = MonitorServer(sd,s)
reactor.listenTCP(HOST_PORT, pb.PBServerFactory(root_obj))
reactor.run()
