'''
2020-01-28 AB: 
    controller class to respond to keyboard, update temperature and launch PID thread.
'''

from Hardware_Adafruit import Hardware_Adafruit
from Hardware_Thermometer import ProbeThermometer
from HardwareSensors import ArduinoSensors
class Controller():



    def __init__(self):
        
        self.sensors = ArduinoSensors()



    def run_app(self):
        self.sensors.start()


c = Controller()
ui = Hardware_Adafruit(c)
print("init")
#c.run_app()
print("here we go..")
ui.demo_buttons()
print("finished")


