import microgear.client as microgear
import time
import logging

appid = "MyFreeBoard"
gearkey = "Uxky6q2JLXcwD3C"
gearsecret =  "3e2EtCrdnpWHUaktujQpVQoPz"

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})

def connection():
    logging.info("Now I am connected with netpie")

def subscription(topic,message):
    logging.info(topic+" "+message)

def disconnect():
    logging.debug("disconnect is work")

microgear.setalias("pi")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/mails")
microgear.connect(False)
count = 0
while True:
    if(microgear.connected):
        count=count+1
        microgear.chat("/count",count)
        print(count)
    time.sleep(1)