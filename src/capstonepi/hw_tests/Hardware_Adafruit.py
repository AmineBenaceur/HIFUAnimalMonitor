import board
import time
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
#from Hardware_Thermometer import ProbeThermometer
import threading


'''
2020-12-05 AB: A Hardware interface file witht the adafruit 16x2 RBG Keypad, using i2c communication

to run file for testing:
    sudo python3 Hardware_Adafruit.py
'''




class Hardware_Adafruit:
   def __init__(self, c):
   
       self.columns=16
       self.rows = 2
       
       self.controller = c
       self.current_temp = 37.0;
       self.set_temp = 00.0;
       self.heart_rate = 44;

       self.mutex = threading.Lock()
       
       self.state='main'
       self.monitor_string = "T= {:.1f}   HR= {:.0f} \nSet Temp: {:.1f} ".format(self.current_temp, self.heart_rate, self.set_temp) 
        
        
      #print(monitor_string)
       # Initialise I2C bus.
       self.i2c = busio.I2C(board.SCL, board.SDA)
       
       # Initialise the LCD class
       self.lcd = character_lcd.Character_LCD_RGB_I2C(self.i2c, self.columns, self.rows)
       self.lcd.clear()

       # Set LCD color to green
       self.lcd.color = [0, 0, 100]
    
   def clear(self):
       '''
       2020-12-05 AB: clear the screen
       '''
       self.lcd.clear()
       self.message = ""
   
   def playIntro(self):
       self.lcd.color = [0,100,00]
       # Print intro message
       self.lcd.message = "AnimalMonitor\n500-NS-1-NeuroFUS"
       time.sleep(2.5)

 
   def dec_temp(self):
       self.set_temp = self.set_temp - 0.1;

   def inc_temp(self):
       self.set_temp = self.set_temp + 0.1;
 

   def printToLCD(self, str):
       #self.clear()
       self.lcd.message=str
       return

   def enter_temp_setting_mode(self):
       self.state='ts'
       temp_initial = self.current_temp
       set_temp_initial = self.set_temp
       self.clear()
         #:wself.lcd.blink = True
       new_temp_string  = "Set Temp: {:.1f}\n<-Cancel   Set->".format(set_temp_initial)
       self.lcd.message = new_temp_string
       first= True
       while(True):
          if first:
             print("inner loop")
             first=False

          if self.lcd.up_button:
              #self.inc_temp()
             set_temp_initial += 0.1
             new_temp_string = "Set Temp: {:.1f}\n<-Cancel   Set->".format(set_temp_initial)
             self.lcd.message = new_temp_string

          if self.lcd.down_button:
            #self.inc_temp()
            set_temp_initial -= 0.1
            new_temp_string = "Set Temp: {:.1f}\n<-Cancel   Set->".format(set_temp_initial)
            self.lcd.message = new_temp_string

          if self.lcd.right_button:
             self.set_temp = set_temp_initial
             
             self.state='main'
             break
        
          if self.lcd.left_button:
             self.state='main'
             break
       if self.set_temp > self.current_temp:
          self.lcd.color = [100,0,0]
       if self.set_temp < self.current_temp:
           #self.lcd.color = [0,0,100]
           pass
   def update_vals(self):
       print("update vals")

   def demo_buttons(self):
       self.playIntro()
       self.clear()
       self.update()
       self.controller.sensors.start()
       self.run_ui_thread()
       temp_initial = self.current_temp
       set_temp_initial = self.set_temp
       while(True):
    
           if self.lcd.down_button:
               self.enter_temp_setting_mode()

           if self.lcd.left_button:
              # self.clear
              # self.lcd.message= "LEFT"
              self.update()
        
           if self.lcd.right_button:
              # self.clear()
              # self.lcd.message="RIGHT"
              # break
              self.update()
           if self.lcd.up_button:
              self.enter_temp_setting_mode()
  
           if self.lcd.select_button:
               self.clear()
               #self.lcd.color = [50,0,50]
               self.lcd.message="Status:\n  Disconnected"
               while(True):
                   if self.lcd.select_button:
                      # self.lcd.color=[0,0,100]
                      # self.lcd.backlight = True
                       break
               # self.lcd.clear()
               #self.lcd.color = [0,0,100] #green
               #time.sleep(1)
               self.update()
               #self.lcd.color = [10,0,100] 
           else:
               print("loop: tmp->{} hb->{}".format(self.controller.sensors.get_temp(), self.controller.sensors.get_hb()))
           
           self.current_temp = self.controller.sensor.get_temp()
           self.heart_rate = self.controller.sesnsor.get_hb()
           
    
   
   
   def update(self):
      print("update start")
      #self.mutex.acquire()
      
      #self.heart_rate = self.controller.sensors.get_hb()
      #self.current_temp = self.controller.sensors.get_temp()
      print("updated temp={} and hb= {}".format(self.current_temp,self.heart_rate))
      # self.clear();
      self.monitor_string = "T= {:.1f}   HR= {:.0f} \nSet Temp: {:.1f} ".format(float(self.current_temp),int( self.heart_rate), self.set_temp) 
      self.printToLCD(self.monitor_string)
      #self.mutex.release()
      print("update end")
   
   def update_t(self):
       while(True):
           if self.state=='main':
               print("update t before read")
               self.heart_rate = self.controller.sensors.get_hb()
               self.current_temp = self.controller.sensors.get_temp()
               print("updating")
               self.update()
           print("...")
           time.sleep(0.5)
   
   def run_ui_thread(self):
       print("starting ui thread")
       self.ui_thread = threading.Thread(target = self.update_t ) 
       self.ui_thread.start()


def main():
    af = Hardware_Adafruit()
    af.playIntro()
    time.sleep(1)
    af.clear()
    #af.inc_temp()
    #af.update()
    #af.inc_temp()
    #time.sleep(1)
    #af.update()
    #time.sleep(1)
    af.demo_buttons()

    #key_read = prev_key = af.i2c.scan()
    #while(True):
     #   if 


     #   key_read = af.i2c.scan()
      #  if key_read == prev_key:
       #     time.sleep(0.1)
       # else:
        #    print(key_read)
         #   prev_key=key_read

    af.i2c.deinit()

if __name__ == "__main__":
    main()
