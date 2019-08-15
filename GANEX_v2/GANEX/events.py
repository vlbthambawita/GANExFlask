import time

from flask import session
from flask_socketio import emit, join_room, leave_room
#from . import socketio
from GANEX.fastGAN.task import randnumber
# socketio = get_socket()
from GANEX.updates import updateplot
from GANEX.db import get_db

from GANEX.dlexmongo import set_train_settings, set_default_hyperparam, get_default_hyperparams

import threading

# from . import socketio

def init_events(socketio):

    # global socketio
   # db = get_db()

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
            

    
    # Experiments window handlings           
    @socketio.on('my test', namespace='/experiments')
    def my_test(data, pid):
        db = get_db()
        print("arg1", data)
        print("pid:", pid)

        # update db
        set_default_hyperparam(db, pid, data["para_name"], data["para_key"], data["para_value"])
        all_hyperparams = list(get_default_hyperparams(db, pid))

        emit('get_default_hyperparams', all_hyperparams)

    

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