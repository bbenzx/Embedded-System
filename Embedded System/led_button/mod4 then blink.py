import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) ## set mode of pin number
GPIO.setup(3,GPIO.IN)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(5,GPIO.LOW)

GPIO.output(5,GPIO.LOW)
time.sleep(0.5)

count = 0
while(1):
    
    buttonstate = GPIO.input(3)

    if(buttonstate == 0):
        count+=1
        if(count%4 == 0):
            GPIO.output(5,GPIO.HIGH)
            time.sleep(0.5)
        else:
            GPIO.output(5,GPIO.LOW)
            time.sleep(0.5)

