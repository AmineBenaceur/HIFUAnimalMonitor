import sys,os
import time
import matplotlib.pyplot as plt
import numpy as np
#from scipy.interpolate import spline
from scipy.interpolate import BSpline, make_interp_spline

class calibration_plotter:
    '''
    This class is responsible for parsing Heating system data from a user specified log file and plotting it.
    '''
    def __init__(self):
        self.feedback_list = []
        self.time_list = []
        self.setpoint_list= []
        self.pwm_list = []

        self.P = 0
        self.I = 0
        self.D = 0

    def parse_input(self, line):
        '''
        Parse a raw line from txt and pass it to proper function
        '''

        raw_vect = line.split('|')
        print(len(raw_vect))

        if len(raw_vect) == 3:
            self.parse_pid( raw_vect)
        if len(raw_vect) == 4:
            self.parse_data_vect(raw_vect)

    def parse_pid(self, pid_vect):
        '''
        AB: parse a data line for the PID constants and store them
        '''
        for constant in pid_vect:
            constant.strip()
            const_vect = constant.split(':')
            if const_vect[0].strip() == 'P':
                self.P = float(const_vect[1].strip())
                print("P set as {}".format(self.P))
            if const_vect[0].strip() == 'I':
                self.I = float(const_vect[1].strip())
                print("I set as {}".format(self.I))
            if const_vect[0].strip() == 'D':
                self.D = float(const_vect[1].strip())
                print("D set as {}".format(self.D))

    def parse_data_vect(self, data_vect):
        '''
        AB: parse a data line from the log and store target temp, current, pwm and time for the data_point
        '''
        for data in data_vect:
            data.strip()
            data_pairs = data.split(':')
            if data_pairs[0].strip() == 'Target':
                self.setpoint_list.append( float(data_pairs[1].strip()) )
                #print("setpoint added as {}".format(float(data_pairs[1].strip())))
            if data_pairs[0].strip() == 'Current':
                self.feedback_list.append( float(data_pairs[1].strip()) )
                #print("temp added as {}".format(float(data_pairs[1].strip())))
            if data_pairs[0].strip() == 'PWM':
                self.pwm_list.append( float(data_pairs[1].strip()) )
                #print("pwm added as {}".format(float(data_pairs[1].strip())))
            if data_pairs[0].strip() == 'Time':
                self.time_list.append( float(data_pairs[1].strip()) )
                #print("time added as {}".format(float(data_pairs[1].strip())))

    def plot_data(self):
        '''
        AB: Plot current data
        '''

        # print(len(self.setpoint_list))
        # print(len(self.feedback_list))
        # print(len(self.pwm_list))
        # print(len(self.time_list))

        time_sm = np.array(self.time_list)
        time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)

        # feedback_smooth = spline(time_list, feedback_list, time_smooth)
        # Using make_interp_spline to create BSpline
        helper_x3 = make_interp_spline(self.time_list, self.feedback_list)
        feedback_smooth = helper_x3(time_smooth)

        plt.plot(time_smooth, feedback_smooth, "g")
        plt.plot(self.time_list, self.setpoint_list, "r")
        plt.plot(self.time_list, self.pwm_list, "m")



        plt.xlim((0, max(self.time_list) +0.5 ))
        plt.ylim((20, 40))
        plt.xlabel('time (s)')
        plt.ylabel('PID (PV)')
        plt.title('AnimalMonitor: P.I.D test \n Constants: P={} I={} D={}  log file = {} '.format(str(self.P),str(self.I),str(self.D), str(sys.argv[1])))

        # plt.ylim((1-0.5, 1+0.5))

        plt.grid(True)
        plt.show()


if len(sys.argv) != 2:
    print("Usage: \n \t python plot_test.py [log_test.txt] \n")
    sys.exit(0)
else:
    filename = os.path.join('test_logs', sys.argv[1])
    print(filename)

#AB : read filename
try:
    with open(filename) as f:
        content = f.readlines()
except:
    print("couldnt read file: {}".format(filename))
    print("make sure this is the correct filename with the .txt type")
    sys.exit(0)

cal_plot = calibration_plotter()


for line in content:
    cal_plot.parse_input(line)


cal_plot.plot_data()


# # you may also want to remove whitespace characters like `\n` at the end of each line
# content = [x.strip() for x in content]
