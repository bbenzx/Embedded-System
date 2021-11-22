import microgear.client as microgear
import time
import logging

appid = "TestLedRed"
gearkey = ""
gearsecret =  ""

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
count = 1
while True:
    if(microgear.connected):
        microgear.chat("HTML_web",str(count))
        print(count)
        count=count+1
    time.sleep(1)