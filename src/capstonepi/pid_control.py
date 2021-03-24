'''
AB: A threaded P.I.D Controller
'''

from HardwareSensors import ArduinoSensors
import time
import PID

def main():
    print("hello")
    sensors = ArduinoSensors()
    sensors.start()
    
    #Constants
    P=1.4
    I=1
    D=0.001

    targetT = 35.0
    L=120

    pid = PID.PID(P,I,D)
    pid.SetPoint = targetT
    pid.setSampleTime(.5)
    
    feedback = 0
    output = 0
    END = L


    print("SETPOINT" + str(pid.SetPoint))

    # run pid
    for i in range(1,END):
        # AB: read and display temp
        temp = sensors.get_temp()
        print("T={}".format(temp))
        
      
        # AB: update the controller
        pid.update(feedback)
        output = pid.output
        pwm = min(max(int(output),0),100)
        #print(output)
        print("PWM={}".format(pwm))
        feedback +=(output-(1/i))


        time.sleep(1)

if __name__ == "__main__":
    main()
