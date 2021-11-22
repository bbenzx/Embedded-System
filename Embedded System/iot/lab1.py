import microgear.client as microgear
import time
import logging
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.IN)
GPIO.setup(5,GPIO.OUT)

appid = "TestLedRed"
gearkey = "5Faa6Reh1fmrDaY"
gearsecret =  "jDxavnIsvzhfuEabjS9D3Vg66"

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})

def connection():
    logging.info("Now I am connected with netpie")

def subscription(topic,message):
    logging.info(topic+" "+message)

def disconnect():
    logging.debug("disconnect is work")

microgear.setalias("PI")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/mails")
microgear.connect(False)

while True:
    if(microgear.connected):
        buttonstate = GPIO.input(3)
        if(buttonstate == 0):
            GPIO.output(5,True)
            microgear.chat("HTML_web1","LED = ON")
        else:
            microgear.chat("HTML_web1","LED = OFF")
            GPIO.output(5,False)
    time.sleep(0.1)