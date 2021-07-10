from flask import json, request, Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route('/messages/<filename>', methods = ['POST'])
def callback(filename):
    if filename is None or filename=='': filename='image'
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data
    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)
    elif request.headers['Content-Type'] == 'application/octet-stream':
        with open('/tmp/'+filename, 'wb') as f:
            f.write(request.data)
            f.close()
        return "Binary message written to /tmp/"+filename
    else:
        return "415 Unsupported Media Type ;)"

