'''
AB: A threaded PID controller module, used to heat up an expiremental bed for a small animal (Mouse).
'''


from HardwareSensors import ArduinoSensors
import time
import PID
import RPi.GPIO as IO
from datetime import datetime
import yaml

'''
AB: Config file w/ constants
'''
CONFIG_FILE = 'constants.yaml'

class Monitor_PID:

    def __init__(self, arduino_sensors):
        self.sensors = arduino_sensors
        #constants
        '''
        TODO: Read from yaml
        '''
        
        self.config = self.read_config(CONFIG_FILE)
        '''
        print(self.config['PID']['Probe']['P'])
        print(self.config['PID']['Probe']['I'])
        print(self.config['PID']['Probe']['D'])
        
        self.P = 1.4
        self.I = 1
        self.D = 0.001
        '''
        #ab time % run params
        start_time = 0
        end_time  = 0
        self.flag_stop_pid = False
        self.flag_confirmed_stop = False

       
        self.sensors = arduino_sensors
        
        #AB: Setup GPIO module
        IO.setwarnings(False)
        IO.setmode(IO.BCM)
        IO.setup(19,IO.OUT)

        self.pwm_out = IO.PWM(19,100)



    def read_config(self, filename):
        with open(filename) as f:
            config = yaml.safe_load(f)
        print (config)
        return config

    def start_pid_thread(self, set_point, probe_ref = True, save_output=False):
        pass

    def pid_process(self,set_point,probe_ref =True, save_output=False ):
        '''
        AB: Start the PID pocess, if probe ref= True use probe temp, else use surface temp (K-type)
        '''
        
        # AB: load PID, depending on Surface or Probe based heating
        if probe_ref:
            P = float(self.config['PID']['Probe']['P']) 
            I = float(self.config['PID']['Probe']['I'])
            D = float(self.config['PID']['Probe']['D']) 
        else:
            P = float(self.config['PID']['Surface']['P'])
            I = float(self.config['PID']['Surface']['I'])
            D = float(self.config['PID']['Surface']['D']) 

        #AB: load sample time
        sample_time = float(self.config['PID']['Sample_time'])
        
        # AB: Instantiate PID, start pwm at 0 dutycycle, set the temp setpoint and sampletime
        self.pid = PID.PID(P,I,D)
        self.pid.SetPoint = set_point
        self.pid.setSampleTime(sample_time)

        self.pwm_out.start(0) 
        
        # AB: Set start time 
        start_time = time.time()
        
        if probe_ref:
            print("Started PID process for setpoint= {} w/  Constants [P,I,D] = [{},{},{}] for Internal heating".format(set_point,P,I,D) )
        else: 
            print("Started PID process for setpoint= {} w/ Constants [P,I,D] = [{},{},{}] for Surface heating".format(set_point,P,I,D) )
        
        while (self.flag_stop_pid == False):
            #AB load the temperature source from probe or k-type
            if probe_ref: 
                temp = self.sensors.get_temp()
            else:
                temp = self.sensors.get_k_temp()

            # AB: update pid w/temp and get target PWM, convert to 0-100 Duty cycle 
            self.pid.update(temp)
            targetPWM = self.pid.output
            targetPWM = max(min(int(targetPWM),100),0) # cant go under 0, or over 100

            #AB: change the dutycyle based on PID output
            self.pwm_out.ChangeDutyCycle(targetPWM) 
            time.sleep(sample_time)

            print(" Target: {} | Current: {} | PWM: {} |  Time {:.2f} ".format(self.pid.SetPoint, temp, targetPWM, (time.time()-start_time) ))

        self.flag_confirmed_stop = True


     
s = ArduinoSensors()
s.start()
p = Monitor_PID(s)
p.pid_process(30, probe_ref=False,save_output=False)  
