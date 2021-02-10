import serial
import time



class ArduinoSensors():
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM1', 9600, timeout=10)
        self.ser.flush()

    def parse_line(self, line):
        print(line)
        
    def start_reading(self):
        while True:
            if self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode('utf-8').rstrip()
                    self.parse_line(line)
                except:
                    print("something went wrong..")
'''                    
def main():    
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=10)
    ser.flush()

    while True:
        if ser.in_waiting> 0:
            try:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
            except:
                print("something went wrong..")
'''

def main():
    sensors = ArduinoSensors()
    sensors.start_reading()

if __name__=='__main__':
   main()




