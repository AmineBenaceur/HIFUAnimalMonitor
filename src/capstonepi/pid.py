from HardwareSensors import ArduinoSensors

import PID
import time
import RPi.GPIO as IO

'''
    AB : set constants & Target
'''
targetT = 37
P = 10
I = 1
D = 1

pid = PID.PID(P, I, D)
pid.SetPoint = targetT
pid.setSampleTime(1)

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

    print('Target: {} C | Current: {}  C | PWM: {}% | Time:{}s '.format(pid.SetPoint, temp, targetPwm, time.time()-start_time ))

	
    # AB: Change PWM duty cycle
    p.ChangeDutyCycle(targetPwm)
    time.sleep(1)
