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
from mark import *

app = Flask(__name__)

TOTAL_LEN = 30
NUM_TICKS = 7

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

socketio = SocketIO(app)

def run_convos():
    start_time = time.time()
    def t():
        return (time.time() - start_time)
    c = []
    def reset():
        nonlocal c
        c = convo(trump, obama)
        while len(c) < 7:
            print('running regen')
            c = convo(trump, obama)
    tick = 0
    reset()
    def do_tick(i):
        nonlocal tick
        if (i % NUM_TICKS) <= 5:
            print('--->', c[i % NUM_TICKS])
            person, txt = c[i % NUM_TICKS]
            emit('message', {'person': person, 'txt': txt}, namespace='/', broadcast=True)
        elif (i % NUM_TICKS) == 6:
            print('----> reset')
            reset()
            emit('reset', namespace='/', broadcast=True)
        tick += 1
    while True:
        socketio.sleep(0.1)
        with app.app_context():
            cur_time = t()
            while tick < cur_time * (NUM_TICKS / TOTAL_LEN):
                do_tick(tick)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    socketio.start_background_task(run_convos)
    socketio.run(app, host='0.0.0.0', port=int(port))
