import time
import datetime
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

SheetName = "Data logger Online"
GSheet_OAUTH_JSON = "serious-studio-309902-d9737ef4e13d.json"
scope =  ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(GSheet_OAUTH_JSON, scope)
client = gspread.authorize(credentials)
worksheet = client.open(SheetName).sheet1

row = ["Time","Value","Status"]
index = 1
worksheet.insert_row(row,index) # Insert data to the row.

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

while(True):
    now = datetime.datetime.now()
    timestamp = now.strftime("%H:%M:%S")
    
    press = adc.read_adc(0, gain=GAIN)
    
    if press <= 10000:
        status = "LOW"
    elif press <= 25000:
        status = "MEDIUM"
    elif press > 25000:
        status = "HIGH"
        
    button_state = GPIO.input(11)
    
    if(button_state ==0):
        worksheet.delete_rows(2,1000)
        time.sleep(0.1)
    
    try:
        worksheet.append_row([timestamp, str(press), status]) # Append data to the next row.
        print("OK")
    except Exception as ex:
        print("Google sheet login failed with error:", ex)
    time.sleep(1)
