'''
2020-01-28 AB: 
    controller class to respond to keyboard, update temperature and launch PID thread.
'''

from Hardware_Adafruit import Hardware_Adafruit
from Hardware_Thermometer import ProbeThermometer

class Controller():



    def __init__(self):
        
        #self.thermometer = ProbeThermometer()
        pass


    def run_app(self):
        pass


c = Controller()
ui = Hardware_Adafruit(c)
print("init")
ui.demo_buttons()
print("finished")


