'''
2020-02-29 AB:
    a class to control gpio's connected to heating element using PWM. 
    # USE PINS 9 & 11 

'''



import RPi.GPIO as GPIO

#from Hardware_Thermometer import ProbeThermometer

GPIO_PIN_SET = 11

class NichromeHeater():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11,GPIO.OUT)
        
        
    def start(self, freq, duty_cyc):   
        self.pwm = GPIO.PWM(GPIO_PIN_SET ,freq)  #pin 11, 100 hertz
        self.pwm.start(0)
        

    def clean_up(self):
        self.pwm.stop()
        GPIO.cleanup()

    def change_dc(self, new_dc):
        self.pwm.ChangeDutyCycle(int(new_dc))


def main():
    stop = False
    
    heat = NichromeHeater()
    heat.start(100,0) # start at 0 duty cycle and 100 hz
    
#    probe = ProbeThermometer()
 #   probe.start_temp_thread()

    while (stop != True):
        dc = input("Enter % duty cycle: (1 to Quit)" )
        #print("you entered -{}-".format(dc))
        if dc == '1':
            stop = True
        heat.change_dc(dc)
    heat.clean_up()

if __name__ == "__main__":
    main()
