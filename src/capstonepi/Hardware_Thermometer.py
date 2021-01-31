'''
# 2020-01-27 AB: Hardware interface for the MCP9600 thermometer amp


'''




'''



import board
import busio
import adafruit_mcp9600
i2c = busio.I2C(board.SCL, board.SDA, frequency=10000)
mcp = adafruit_mcp9600.MCP9600(i2c)
print(mcp.temperature)

'''
import time
import board
import busio
import adafruit_mcp9600
i2c = busio.I2C(board.SCL, board.SDA, frequency=10000)

from threading import Thread, Lock


class ProbeThermometer():

    def __init__(self):
        
       self.i2c = busio.I2C(board.SCL, board.SDA, frequency = 100000)
       self.mcp = adafruit_mcp9600.MCP9600(i2c)
       
    
       self.probe_temp = 0
       self.ambient_temp = 0
       self.delta_Temp = 0
       
       self.mutex= Lock()

    def set_temp(self, probe, ambient, delta):
        self.mutex.acquire()

        self.probe_temp = probe
        self.ambient_temp = ambient
        self.delta_temp = delta
        
        self.mutex.release()

    def get_reading(self):
        reading = {}
        self.mutex.acquire()
        try:
            reading['probe'] = self.mcp.temperature
            reading['ambient'] = self.mcp.ambient_temperature
            reading['delta'] = self.mcp.delta_temperature
        except:
            print("Error in getting reading from probe")

        self.mutex.release()
        return reading



        '''
        self.probe_temp = self.mcp.temperature
    
        
        '''
    def print_temp():
        while True:
            read=self.get_reading()
            print("TEMP= {} \t AMBIENT={} \t DELTA={}".format(read['probe'], read['ambient'], read['delta']))
            time.sleep(1)

    def start_temp_thread(self):
        thread = Thread(target = self.print_temp )
        thread.start()


probe = ProbeThermometer()
while True:
    read = probe.get_reading()

    print("TEMP= {}\tAMBIENT={}\tDELTA={}".format(read['probe'], read['ambient'], read['delta']))
    

    time.sleep(1)



# frequency must be set for the MCP9600 to function.
# If you experience I/O errors, try changing the frequency.

'''
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
mcp = adafruit_mcp9600.MCP9600(i2c)
while True:
    print((mcp.ambient_temperature, mcp.temperature, mcp.delta_temperature))
    time.sleep(1)

'''
