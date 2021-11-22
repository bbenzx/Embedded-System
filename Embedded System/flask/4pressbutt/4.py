from flask import Flask, render_template, jsonify, request
import datetime
import RPi.GPIO as GPIO

app = Flask(__name__)

@app.route('/')
def index():
    print("start webpage")
    return render_template('index.html')

@app.route('/updateTime')
def updateTime():
    print("update time and button Input")
    
    if(GPIO.input(5)==0):
        Button_Status = "Pressed"
    
    else:
        Button_Status = "Released"
    
    now = datetime.datetime.now()
    timeString = "TIME: " + now.strftime("%H:%M:%S")
    UpdateDataOnweb = {
        'ButtonStatus' : Button_Status,
        'Time' : timeString
        }
    
    return jsonify(**UpdateDataOnweb)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(5,GPIO.IN)
    app.run(debug=True,host='0.0.0.0', port = 80)
    