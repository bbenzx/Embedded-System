import time
import datetime
import random
import microgear.client as microgear
import logging
import RPi.GPIO as GPIO
from flask import Flask, request, make_response, jsonify
import os
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(3,GPIO.IN)
GPIO.output(5,GPIO.LOW)

#datalog online---------------------------------------------
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SheetName = "Data logger Online"
GSheet_OAUTH_JSON = "serious-studio-309902-d9737ef4e13d.json"
scope =  ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(GSheet_OAUTH_JSON, scope)
client = gspread.authorize(credentials)
worksheet = client.open(SheetName).sheet1

row = ["AQI","Temperature(Celsius)","Time"]
index = 1
worksheet.insert_row(row,index) # Insert data to the row.

#netpie----------------------------------------------------------
appid = "FinalEmbedded"
gearkey = "ISZ8DfjbaYrbdHG"
gearsecret =  "OOwnDj72Z2t3IYvWvICgHJCUZ"

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

#chatbot-----------------------------------------------------
# create flask app
app = Flask(__name__)
log = app.logger
# recieve request from webhook
@app.route("/", methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(req)
    try:
       # action = req.get('queryResult').get('action')
        action = req.get('queryResult').get('intent').get('displayName')
        param = req.get('queryResult').get('parameters').get('time')
    except AttributeError:
        return 'json error'
    # action switcher 
    if action == 'AQI':
        res = Requestaqi(req)
    elif action == 'Temperature':
        res = Requesttemperature(req)
    else:
        log.error('Unexpected action.')

    print('Action: ' + str(action))
    print('Response: ' + res)

    # return response
    return make_response(jsonify({'fulfillmentText': res}))

def Requestaqi(req):
        lastestrow = len(worksheet.get_all_records())+1
        returnaqi = "Latest AQI is : "+str(worksheet.cell(latestrow,1).value) 
        return returnaqi

def Requesttemperature(req):
        lastestrow = len(worksheet.get_all_records())+1
        returntemp = "Latest Temperature is : "+str(worksheet.cell(latestrow,2).value) 
        return returntemp
                                                    
# run flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','5000')))
    
    
while True:
    
    now = datetime.datetime.now()
    timestamp = now.strftime("%H:%M:%S")
    
    aqi = random.randint(0,200)
    tempcel = random.randint(0,45)
    
    if(microgear.connected):
        microgear.publish("/aqi",aqi)
        
        buttonstate = GPIO.input(3)
        if(buttonstate == 0):
            print("button is pressed")
            temp = (tempcel*9/5)+32
            tempfrombutton = str(temp) + " Fahrenheit"
            microgear.publish("/temp",tempfrombutton)
        else:
            temp = tempcel+0
            tempfrombutton = str(temp) + " Celcius"
            microgear.publish("/temp",tempfrombutton)
                
    print("aqi : "+str(aqi))
    print("temperature : "+tempfrombutton)
    print("timestamp: "+str(timestamp))
    
    try:
        worksheet.append_row([aqi, tempcel, timestamp]) # Append data to the next row.
        print("OK\n")
    except Exception as ex:
        print("Google sheet login failed with error:\n", ex)
    
    if(aqi>=100):
        GPIO.output(5,GPIO.HIGH)
    else:
        GPIO.output(5,GPIO.LOW)
    
    time.sleep(5)
    
    
