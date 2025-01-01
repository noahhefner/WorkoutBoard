from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os
import sys
from pathlib import Path

from db import init_db, get_all_workouts

app = Flask(__name__)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

socketio = SocketIO(app)

with app.app_context():

    init_db()

@app.route('/')
def index():
    return render_template('home.tmpl.html')

@app.route('/control')
def control():

    workouts = get_all_workouts()

    return render_template('control.tmpl.html', workouts = workouts)

@app.route('/board')
def board():
    return render_template('board.tmpl.html')

# websocket
@socketio.on('connect')
def connect():
    print('Client connected!')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected.')

@socketio.on('workoutselected')
def workout_selected(data):
    emit('workoutselected', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=True)
