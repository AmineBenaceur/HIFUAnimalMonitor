from HardwareSensors import ArduinoSensors
import os
import PID
import time
import RPi.GPIO as IO
from datetime import datetime

'''
    AB : set constants & Target
'''
targetT = 37
P = 10
I = 1
D = 2

pid = PID.PID(P, I, D)
pid.SetPoint = targetT
pid.setSampleTime(1)

'''
AB: create file to write to
'''
# datetime object containing current date and time
now = datetime.now()

#filename = str(P) + '-' + str(I) + '-' + str(D) + '___' + now.strftime("%d/%m/%Y %H:%M:%S") + '.txt'
filename = "test_1.txt"
#os.system( 'touch ' + filename )
f = open(filename, "w")
f.write("------------------------------------------------ \n ")
f.write("AB: Instrumentation test W/ AnimalMonitor System  \n   ")
f.write(" Test W/ P.I.D = [{} , {}, {} ] \n  ".format(P,I,D))
f.write("------------------------------------------------\n  ")


'''
    AB: setup sensor feedback and output pwm 
'''

#sensors
sensors = ArduinoSensors()
sensors.start()


#pwm pin
IO.setwarnings(False)
IO.setmode (IO.BCM)
IO.setup(19,IO.OUT)

p = IO.PWM(19,100)

# AB: Generate PWM with 0% duty cycle
p.start(0) 

# start timer
start_time = time.time()
while True:
    temp = sensors.get_temp() 
    pid.update(temp)
	
    targetPwm = pid.output
    targetPwm = max(min( int(targetPwm), 100 ),0)

    print('Target: {} C | Current: {}  C | PWM: {}% | Time:{:.2f} '.format(pid.SetPoint, temp, targetPwm, time.time()-start_time ))
    
    f.write('Target: {} C | Current: {}  C | PWM: {}% | Time:{}s \n '.format(pid.SetPoint, temp, targetPwm, time.time()-start_time ))
	
    # AB: Change PWM duty cycle
    p.ChangeDutyCycle(targetPwm)
    time.sleep(1)
