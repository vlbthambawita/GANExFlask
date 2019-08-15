import time

from flask import session
from flask_socketio import emit, join_room, leave_room
#from . import socketio
from GANEX.fastGAN.task import randnumber
# socketio = get_socket()
from GANEX.updates import updateplot
from GANEX.db import get_db

import threading

# from . import socketio

def init_events(socketio):

    # global socketio
    

    @socketio.on('joined', namespace='/chat')
    def joined(message):
        """Sent by clients when they enter a room.
        A status message is broadcast to all people in the room."""
        print("Joined is running")
        emit('status', {'msg': 'connected from server'})

        x = threading.Thread(target=randnumber, args=(socketio,))
        x.start()

    # plot sta handle - near real time
    @socketio.on('plotting', namespace='/plot')
    def plotting(msg):
        updateplot(socketio, get_db())

            # x = threading.Thread(target=updateplot, args=(socketio,get_db()))
            
            #if (msg["status"] == "connected") and (x.is_alive() != True):
            #    print("plot tab connected")
            #    x.start()
            
                
    @socketio.on('my test', namespace='/experiments')
    def my_test(arg1):
        print("arg1", arg1)

    @socketio.on('my event')
    def handle_my_custom_event(json):
        print('received json: ' + str(json))
       

    #def testEmit():
    # socketio.emit('test', {'msg': 'socket emit working'}, namespace='/chat')
# Blue print
#bp = Blueprint('events', __name__)

# Inference
#@bp.route('/events/', methods=('GET',))
#def inference():
#    return render_template('run/events.html')

#@socketio.on('connect', namespace='/test')
#def test_connect():
    # need visibility of the global thread object
    # global thread
#    print('Client connected')