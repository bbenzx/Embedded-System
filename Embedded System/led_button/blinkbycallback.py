import RPi.GPIO as GPIO

mode = 0
def button_callback (channel):
    
	global mode
	buttonstate = GPIO.input(5)

        if(buttonstate == 0):
            if(mode==0):
                GPIO.output(3,GPIO.HIGH)
                mode = 1
            else:
                GPIO.output(3,GPIO.LOW)
                mode = 0
	

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) ## set mode of pin number
GPIO.setup(5,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(3,GPIO.OUT)
GPIO.add_event_detect(5, GPIO.FALLING, callback = button_callback, bouncetime = 300)
messa = input("jhgkhglohlh")




