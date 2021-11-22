from flask import Flask,render_template,jsonify,request
import datetime
import RPi.GPIO as GPIO
import time
import Adafruit_ADS1x15
adc=Adafruit_ADS1x15.ADS1115()
GAIN=1
app=Flask(__name__)

@app.route('/')
def index():
	print('Start Webpage')
	return render_template('index.html')

@app.route('/updateTime')
def updateTime():
    print('update time')
    now = datetime.datetime.now()
    timestring='TIME: '+now.strftime("%H:%M:%S")
    value=adc.read_adc(0,gain=GAIN)
    if(value<0):
        value = 0
    text_value=str(value)
    UpdateDataOnweb={
        'status' : text_value,
        'Time' : timestring
    }
    return jsonify(**UpdateDataOnweb)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)

