from flask import Flask

app = Flask(__name__)

@app.route('/')

def index():
    return 'hello world web server on pi'

if __name__ == '__flaskbenz__':
    app.run(debug=True,host='0.0.0.0')