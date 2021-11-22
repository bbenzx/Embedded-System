from flask import Flask, render_template, jsonify, request
import datetime
import RPi.GPIO as GPIO
import Adafruit_ADS1x15

Percent = False
app = Flask(__name__)

@app.route('/')
def index():
    print("start webpage")
    return render_template('index.html')

@app.route('/updateTime')
def updateTime():
    print("update time and Pressed Value Input")
    
    global Percent
    value = adc.read_adc(0,gain=GAIN)
    if(value<=0):
        value = 0
    percentValue = value*100/20000
    
    if(Percent):
        Value_Status = str(round(percentValue,4)) +"%"
    else:
        Value_Status = str(value)
    
    now = datetime.datetime.now()
    timeStr = "TIME: " + now.strftime("%H:%M:%S")
    UpdateDataOnweb = {
        'Value' : Value_Status,
        'Time' : timeStr
        }
    return jsonify(**UpdateDataOnweb)

@app.route('/changeValueType')
def changeValueType():
    global Percent
    if(Percent):
        Percent = False
        strWord = "ChangeToPercent"
    else:
        Percent = True
        strWord = "ChangeToNumber"
    return jsonify(word = strWord)


if __name__ == '__main__':
    adc = Adafruit_ADS1x15.ADS1115()
    GAIN = 1;
    app.run(debug=True,host='0.0.0.0', port = 80)
    