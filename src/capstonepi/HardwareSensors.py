import serial
import time
import threading


class ArduinoSensors():
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=10)
        self.ser.flush()
        
        self.temp =0
        self.hb =0
        self.k_temp=0
#        self.hb_avg = list()

        #self.temp_mutex= threading.Lock()
        #self.hb_mutex = threading.Lock()

    def set_temp(self, t):

        #self.temp_mutex.acquire()
        self.temp = t
        #print("new temp set == {}".format(t))

        #self.temp_mutex.release()
    
    def set_k_temp(self,k):
        self.k_temp = k

    def get_temp(self):
        r = self.temp
        return r
        
        #print("gettemp end")
    def set_hb(self, h):
        #self.hb_mutex.acquire()
        '''
        print(" +++ set hb start w/ len={}".format(self.hb_avg))
        try:
            if (len(self.hb_avg) == 0):
                print("set_hb() list is empty")
                self.hb_avg.append(h)
                print("appended h={}".format(h))
            else:
                self.hb_avg.insert(0,h)
        except Exception as e:
            print(e)

        print("set_hb after insert = []".format(self.hb_avg))
        self.hb = self.get_rolling_avg()
        '''
        self.hb=h
       # print("new hb set == {} avg={}  list={} ".format(h,self.hb, self.hb_avg ))
        #self.hb_mutex.release()
        #print(" --- set hb end")
    
    def get_k_temp(self):
        return self.k_temp

    def get_rolling_avg(self):
        l = len(self.hb_avg)
        if (l == 0):
            #print("EMPTY LIST")
            return 0
        if (l > 0 and l <10):
            return (sum(self.hb_avg)/l)
        if (l >= 10):
            i=0
            s=0
            while(i<10):
                s+=self.hb_avg[i]
                i+=1
            return (s/10)


    def get_hb(self):
        #self.hb_mutex.acquire()
        r = self.hb
        
        #self.hb_mutex.release()
        return r

    def parse_line(self, line):
               
        #print("-------------")
        #print(line)
        
        vect = line.split(':')
        
        if len(vect) !=  2:
            #print("response is only {} long, couldnt read. ".format(len(vect)))
            return
        
        #print("vect[0]" + vect[0])

        #print("vect[1]" + vect[1])
        #print("---")
        if (vect[0] == "T"):
            #print("new temp = {}".format(vect[1]))
            self.set_temp( float(vect[1])) 
        if (vect[0] == "B"):
            #print("new hb = {}".format(int(vect[1])))
            self.set_hb(vect[1])
        
        if (vect[0] == "K"):
            try:
                if vect[1] == "nan":
                    #print("nan caught")
                    return

                temp_k = float(vect[1])
                if isinstance(temp_k,float):
                    #print("new K = {}".format(temp_k))
                    self.set_k_temp(temp_k)
                else:
                    #print("ktype reading NAN caught")
                    return
            except Exception as ke:
                #print("Error in converting k-type temp: {}".format(ke))
                pass
        #print("no read on:" + line)
        #print("-------------")
        

    def start_reading(self):
        print("STARTING THREAD")
        while True:
            if self.ser.in_waiting == 0:
                #print("wait..")
                #time.sleep(0.1)
                pass
            if self.ser.in_waiting > 0:
                #print("arrived")
                try:
                    #print("reading...")
                    line = self.ser.readline().decode('utf-8').rstrip()
                    #line = str(self.ser.readline().rstrip())
                    
                    #print("read line") 
                    self.parse_line(line)
                except Exception as e :
                    #print("something went wrong.."+ str(e) )
                    pass

    def start(self):
        self.thread = threading.Thread(target=self.start_reading)
        self.thread.start()
        # self.thread.join()
        #print("Arduino thread terminated")
'''
                    
def main():    
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=10)
    ser.flush()

    while True:
        if ser.in_waiting> 0:
            try:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
            except:
                print("something went wrong..")
'''

def main():
    sensors = ArduinoSensors()
    #sensors.start()

#    sensors.start_reading()
    sensors.start()
#    while(True):
#        print("temp main: {}".format(sensors.get_temp()) )



if __name__=='__main__':
   main()




