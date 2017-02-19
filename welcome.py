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

TOTAL_LEN = 40
NUM_TICKS = 9

c = []
between = ()
tick = 0
total_votes = 0
correct_votes = 0

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

socketio = SocketIO(app)

def obj(e):
    return {'person': e[0], 'txt': e[1]}

def make_between(between):
    p1, p2 = between
    return p1.name.lower(), p2.name.lower()

@socketio.on('connect')
def new_client():
    getIndex = min(tick % NUM_TICKS, 6)
    print('<--- connect')
    emit('uptd', {'logs': [obj(e) for e in c[:getIndex]]})

@socketio.on('vote')
def on_vote(vote):
    global total_votes, correct_votes
    total_votes += 1
    if vote['left'] == between[0].name and vote['right'] == between[1].name:
        correct_votes += 1
    print('<--- vote:', vote)

def run_convos():
    start_time = time.time()
    def t():
        return time.time() - start_time

    def reset():
        global c
        global between, total_votes, correct_votes
        total_votes = correct_votes = 0
        between = get_between()

        c = convo(between)
        i = 0
        while len(c) < 8 and i < 50:
            print('running regen')
            c = convo(between)
            i += 1
        if i == 50:
            reset()
    reset()
    def do_tick(i):
        global tick
        if (i % NUM_TICKS) <= 5:
            print('--->', c[i % NUM_TICKS])
            emit('message', obj(c[i % NUM_TICKS]), namespace='/', broadcast=True)
        elif (i % NUM_TICKS) == 6:
            print('---> vote')
            a, b = between
            left = [p.name for p in pick_including(a)]
            right = [p.name for p in pick_including(b)]
            emit('vote', {'left': left, 'right': right}, namespace='/', broadcast=True)
        elif (i % NUM_TICKS) == 8:
            print('---> reveal', between)
            emit('reveal', {'between': make_between(between),
                            'totalVotes': total_votes,
                            'correctVotes': correct_votes}, namespace='/', broadcast=True)
            reset()
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
