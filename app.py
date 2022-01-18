

# Start with a basic flask app webpage.
import eventlet
eventlet.monkey_patch()
from flask_socketio import SocketIO, emit
from flask import Flask, render_template
from threading import Thread


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
async_mode = "eventlet"

socketio = SocketIO(app, async_mode=async_mode, logger=True, engineio_logger=True)

thread = Thread()

size = 10
def get_message():
    with open("demo.txt", 'r') as f:
        current_read = f.readlines()
    return current_read

def helper():
	global size
	while True:
   		data = get_message()
   		if len(data) != size:
   			x = len(data)-size
   			size = len(data)
   			socketio.emit('response', {'data': data[-x:]}, namespace='/test')
   		socketio.sleep(1)


@app.route('/')
def index():
	data = get_message()
	return render_template('index.html',data = data[-10:])

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if not thread.isAlive():
        thread = socketio.start_background_task(helper)


if __name__ == '__main__':
    socketio.run(app)
