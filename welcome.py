# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify, Blueprint
from flask_socketio import SocketIO, emit
import time
from threading import Thread

app = Flask(__name__)

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

socketio = SocketIO(app)

@socketio.on('my event')
def test_message(message):
    print('[GOT]', message)
    socketio.emit('my response', {'data': 'got it!'})

def run_convos():
    start_time = time.time()
    print(start_time)
    socketio.sleep(2)
    while True:
        print('hi', time.time())
        socketio.sleep(0.5)
        with app.app_context():
            emit('my response', {'data': 'time is now: ' + str(time.time())},
                broadcast=True, namespace='/')

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    socketio.start_background_task(run_convos)
    socketio.run(app, host='0.0.0.0', port=int(port))
