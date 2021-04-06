import RPi.GPIO as IO
import time

#pwm
IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(19,IO.OUT)

p = IO.PWM(19,100)

p.start(0)


dc = 50
while True:
    p.ChangeDutyCycle(dc)
    time.sleep(1)
