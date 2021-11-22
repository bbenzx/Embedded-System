import microgear.client as microgear
import time
import logging
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
GPIO.output(3,GPIO.LOW)

appid = "TestLedRed"
gearkey = "5Faa6Reh1fmrDaY"
gearsecret =  "jDxavnIsvzhfuEabjS9D3Vg66"

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})

def connection():
    logging.info("Now I am connected with netpie")
def subscription(topic,message):
    print(message[2])
    if(message[2] == "1"):
        GPIO.output(3,GPIO.HIGH)
        msg = "on"
    elif(message[2] == "0"):
        GPIO.output(3,GPIO.LOW)
        msg = "off"
    if(microgear.connected):
        microgear.chat("HTML_web2",msg)
def disconnect():
    logging.debug("disconnect is work")
    
microgear.setalias("PI")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/mails")
microgear.connect(False)

while True:
    time.sleep(0.5)
