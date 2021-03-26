from MonitorLCD import Monitor_LCD
import time
from HardwareSensors import ArduinoSensors


class Monitor_Controller:
    def __init__(self):
        self.screen = Monitor_LCD()
        self.sensors = ArduinoSensors()

        self.current_temp = 0
        self.current_hb = 0
        self.current_set = 0
        
        self.state='main'
    def launch_pid_process(self,set_point):
        print("launched PID for set_point = {}".format(set_point))
        
    def enter_temp_setting_mode(self):
        start_temp = self.sensors.temp
        self.screen.launch_set_menu(start_temp)
        temp_val = start_temp
        
        while True:
            if self.screen.lcd.up_button:
                temp_val += 0.1
                self.screen.update_set_menu(temp_val)
            if self.screen.lcd.down_button:
                temp_val -= 0.1
                self.screen.update_set_menu(temp_val)
            if self.screen.lcd.right_button:
                self.current_set = temp_val
                self.launch_pid_process(self.current_set)
                self.screen.switch_color_red()
                break
            if self.screen.lcd.left_button:
                break

    def run_app(self):
        self.sensors.start()
        self.screen.play_intro()
        self.screen.launch_main_menu()
        time.sleep(1)
        #update initial readings

        while True:
            if self.screen.lcd.up_button:
               self.enter_temp_setting_mode()
            if self.screen.lcd.down_button:
               self.enter_temp_setting_mode()
            if self.screen.lcd.right_button:
                self.screen.set_msg("right")
                time.sleep(0.5)
            if self.screen.lcd.left_button:
                self.screen.set_msg("left")
                time.sleep(0.5)
            if self.screen.lcd.select_button:
                self.screen.set_msg("select")
                time.sleep(0.5)

            self.screen.update_readings(self.sensors.hb,self.sensors.temp, self.current_set)
    '''
    def update_screen_readings(self):
        if(self.state =='main'):
            self.screen.
    '''
'''
s = Monitor_LCD()
s.play_intro()
'''

mc = Monitor_Controller()
mc.run_app()
