from flask import Flask, render_template, redirect, url_for
from random import randint
import tasks
import threading
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'
socketio = SocketIO(app, async_mode='threading')

@app.route("/", methods=['GET'])
def index():
    return render_template('index.htm')


@app.route("/runTask", methods=['POST'])
def long_task():
    print("Hello")
    # n = randint(0, 100)
    #tsk = tasks.long_task.delay(n=10)
    #handleMessage("Testing message")
    # emit('my response', {'data': 'Connected'})
    
    threading.Thread(target=tasks.long_task, args=(socketio, )).start()
    return redirect(url_for("index"))

# @socketio.on('connect')
# @socketio.on('my event')
#def test_connect():
 #   print("connected")
 #   emit('my response', {'data': 'Connected'})
    # emit('my response 2', {'data': 'Connected 2'})

@socketio.on('message')
def handleMessage(msg):
    print("Message:", msg)
    send(msg, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)
