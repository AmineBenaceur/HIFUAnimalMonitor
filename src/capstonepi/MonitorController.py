from MonitorLCD import Monitor_LCD
import time
from HardwareSensors import ArduinoSensors
from MonitorPID import Monitor_PID
from MonitorServer import MonitorServer, MockController
import threading
'''
    AB: Class responsible for handling application logic, starting the servers and making all work together. 
'''

class Monitor_Controller:
    def __init__(self):
        #AB : Initilize screen
        self.screen = Monitor_LCD()
        
        #AB : Initialize sensors from arduino
        self.sensors = ArduinoSensors()
        
        #AB : Initilize PID controller
        self.heater = Monitor_PID(self.sensors)

        self.current_temp = 0
        self.current_hb = 0
        self.current_set = 0
        self.client_temp_set = False
        self.mutex = threading.Lock()
        self.state='main'
    def launch_pid_process(self,set_point):
        print("launched PID for set_point = {}".format(set_point))
    def new_set_value(self, val):
        self.current_set = val
        self.heater.start_pid_thread(self.current_set)
        #self.screen.clear()
        self.screen.switch_color_red()
        #self.client_set_temp = False
    def set_remote_temp_flag(self,bFlag):
	self.mutex.acquire()
	self.client_temp_set = bFlag
	self.mutex.release()

    def get_remote_temp_flag(self):
	self.mutex.acquire()
	b = self.client_temp_set 
	self.mutex.release()
	return b

    def enter_temp_setting_mode_T(self):
        start_temp = self.sensors.temp
        self.screen.launch_set_menu(start_temp)
        temp_val = start_temp
        self.screen.switch_color_yellow()
        up_counter = 0
        down_counter= 0
        while True:
            if self.screen.lcd.up_button:
                down_counter = 0
                up_counter += 1
                if (up_counter >=10):
                    temp_val += 1
                elif((up_counter >= 7) and (up_counter <10)):
                    temp_val += 0.5
                else:
                    temp_val += 0.1
                self.screen.update_set_menu(temp_val)
            if self.screen.lcd.down_button:
                up_counter = 0
                down_counter += 1
                if (down_counter >= 10):
                    temp_val -= 1
                elif((down_counter >= 7) and (down_counter < 10)):
                    temp_val -= 0.5
                else:
                    temp_val -=0.1
                
                self.screen.update_set_menu(temp_val)
            if self.screen.lcd.right_button:
                #self.current_set = temp_val
                #self.heater.start_pid_thread(self.current_set)
                #self.screen.clear()
                #self.screen.switch_color_red()
                self.screen.clear()
                self.new_set_value(temp_val)
                break
            if self.screen.lcd.left_button:
                if self.heater.is_running():
                    self.screen.switch_color_red() #Added here
                    self.screen.clear()
                    break
                else:
                    self.screen.switch_color_green()
                    self.screen.clear()
                    break

    def set(self, set_val):
        #print("must set:")
        #print(set_val)
        self.current_set = set_val
        #self.client_temp_set = True
        self.set_remote_temp_flag(True)
	#self.heater.start_pid_thread(self.current_set)
        #self.screen.clear()
        #self.screen.switch_color_red()
        return True
   
    def run(self):
        #ms = MonitorServer(self.sensors, MockController())
        ms = MonitorServer(self.sensors, self)
        ms.start_server_threaded([(self._main_loop, tuple(), {}, )])

    def enter_surface_temp_mode(self):
	pass
    def stop_heating_mode(self):
	if (self.heater.thread != None):
            self.heater.stop_pid_thread()
	    self.current_set = 0
	    self.screen.switch_color_green()
    def enter_network_mode(self):
	pass
    def _main_loop(self):
        self.sensors.start()
        self.screen.play_intro()
        self.screen.launch_main_menu()
        #time.sleep(1)
        #update initial readings

        while True:
            if self.screen.lcd.up_button:
               self.enter_temp_setting_mode_T()
            if self.screen.lcd.down_button:
               self.enter_temp_setting_mode_T()
            if self.screen.lcd.right_button:
                self.screen.set_msg("right")
                time.sleep(0.5)
            if self.screen.lcd.left_button:
                self.screen.set_msg("left")
                time.sleep(0.5)
            if self.screen.lcd.select_button:
                #self.screen.set_msg("select")
                #time.sleep(0.5)
		self.stop_heating_mode()
            if self.get_remote_temp_flag():
		self.set_remote_temp_flag(False)
                self.new_set_value(self.current_set)
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

if __name__ == "__main__":
    mc = Monitor_Controller()
    mc.run()
