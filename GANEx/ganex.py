from flask import Flask, render_template
from flask_socketio import SocketIO

import threading
import  time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, async_mode='threading') # this is required to work with threading 


# main folder
@app.route('/')
def sessions():
    return render_template('getProjectPath.html')


if __name__ == "__main__":
    socketio.run(app, debug=True)