import time

from flask import session
from flask_socketio import emit, join_room, leave_room
#from . import socketio

# socketio = get_socket()

def init_events(socketio):

    
    

    @socketio.on('joined', namespace='/chat')
    def joined(message):
        """Sent by clients when they enter a room.
        A status message is broadcast to all people in the room."""
        print("Joined is running")
        emit('status', {'msg': 'connected from server'})

        for i in range(10):
            time.sleep(1)
            emit('test', {'msg': 'test msg -' + str(i)})
            
        

    
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