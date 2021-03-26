import board
import time
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import threading









class Monitor_LCD:
    def __init__(self, c = None):
        self.columns=16
        self.rows = 2
        try:
            self.controller = c
        except:
            print("running w/o Contoller")
        #AB: Initial Values
        self.current_temp = 37.0
        self.set_temp = 00.0
        self.heart_rate = 44
      
        #AB: Initialize LCD
        self.i2c = busio.I2C(board.SCL, board.SDA)
        # Initialise the LCD class
        self.lcd = character_lcd.Character_LCD_RGB_I2C(self.i2c, self.columns, self.rows)
        self.lcd.clear()
      
        # Set LCD color to green
        self.lcd.color = [100,0,0]
    
    def play_intro(self):
        self.lcd.blink = True
        self.switch_color_yellow()
        intro_msg = "AnimalMonitor  \nTeam NeuroFUS"
        self.lcd.message = intro_msg
        time.sleep(2.5)
        rollback_count = len(intro_msg) -5
        for i in range(rollback_count):
            time.sleep(0.15)
            self.lcd.move_left()
        
        
        self.lcd.clear()
        self.lcd.blink = False

    def switch_color_green(self):
        self.lcd.color = [0,0,0]
        self.lcd.color = [0,100,0]
        time.sleep(0.5)
        #time.sleep(1)
    def switch_color_red(self):
        self.lcd.color = [0,0,0]
        self.lcd.color = [100,0,0]
        time.sleep(0.5)
    def switch_color_yellow(self):
        self.lcd.color = [0,0,0]
        self.lcd.color = [100,60,0]
        time.sleep(0.5)

    def turn_off(self):
        self.lcd.clear()
        self.lcd.color = [0,0,0]

    def set_msg(self, m ):
        self.lcd.clear()
        self.lcd.message = m
    def launch_main_menu(self):
        self.lcd.clear()
        self.switch_color_green()
        self.update_readings(0,0,0)
    def update_readings(self, r_hb, r_temp, r_set):
        menu_str = "T= {:.1f}  HR= {:<3d} \nSet Temp: {:.1f} ".format(float(r_temp),int( r_hb), r_set)
       # self.set_msg(menu_str)
        self.lcd.message = menu_str
    def launch_set_menu(self, start_val ):
        self.lcd.clear()
        self.switch_color_green()
        new_temp_string  = "Set Temp: {:.1f}\n<-Cancel   Set->".format(start_val)
        self.set_msg(new_temp_string)

    def update_set_menu(self, update_val):
        
        new_temp_string  = "Set Temp: {:.1f}\n<-Cancel   Set->".format(update_val)
        self.lcd.message = new_temp_string

'''
s = Monitor_LCD()
s.play_intro()
time.sleep(0.5)
s.launch_main_menu()
time.sleep(0.5)
s.update_readings(20,80,0)
time.sleep(1)

s.update_readings(250,50,26)
time.sleep(1)
s.launch_set_menu( 21)
time.sleep(2)
s.update_set_menu(21.5)
time.sleep(1)
s.update_set_menu(22.3)
time.sleep(1)
s.turn_off()
'''
