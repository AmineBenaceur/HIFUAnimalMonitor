from HardwareSensors import ArduinoSensors

import PID
import time

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
    AB: setup feedback and output pwm 
'''

sensors = ArduinoSensors()
sensors.start()
while True:
    temp = sensors.get_temp() 
    pid.update(temp)
	
    targetPwm = pid.output
    targetPwm = max(min( int(targetPwm), 100 ),0)

    print('Target: {} C | Current: {}  C | PWM: {} '.format(pid.SetPoint, temp, targetPwm ))

	
    # TODO Set PWM 
	
        
        
    time.sleep(1)
