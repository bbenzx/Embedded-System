from flask import Flask, request, make_response, jsonify
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
GPIO.output(3,GPIO.LOW)
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
    except AttributeError:
        return 'json error'
    # action switcher 
    if action == 'TurnOn':
        GPIO.output(3,GPIO.HIGH)
        res = turn_on(req)
    elif action == 'TurnOff':
        GPIO.output(3,GPIO.LOW)
        res = turn_off(req)
    else:
        log.error('Unexpected action.')

    print('Action: ' + str(action))
    print('Response: ' + res)

    # return response
    return make_response(jsonify({'fulfillmentText': res}))

def turn_off(req):
        return 'Finish off'

def turn_on(req):
        location = req.get('queryResult').get('parameters').get('location')
        print(location)
        return 'Finish on'

# run flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','5000')))
