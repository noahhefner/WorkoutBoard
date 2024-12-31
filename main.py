from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os
import sys
from pathlib import Path

from db import init_db

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
    return render_template('control.tmpl.html')

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

if __name__ == '__main__':
    socketio.run(app)
