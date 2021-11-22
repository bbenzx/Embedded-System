from flask import Flask, render_template, jsonify, request
import datetime
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)

app = Flask(__name__)

@app.route('/')
def index():
    print("start webpage")
    return render_template('index.html')

@app.route('/updateTime')
def updateTime():
    print("update time")
    now = datetime.datetime.now()
    timestring = "TIME: " + now.strftime("%H:%M:%S")
    return jsonify(timeupdate = timestring)
    
@app.route('/<pin>/<action>')
def LEDControl(pin,action):
    print("control LED")
    if(pin=='3' and action=='ON'):
        GPIO.output(3,GPIO.HIGH)
    else:
        GPIO.output(3,GPIO.LOW)
    return jsonify(status=action)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(3,GPIO.OUT)
    app.run(debug=True,host='0.0.0.0', port = 80)
    