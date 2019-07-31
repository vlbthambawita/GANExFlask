


from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form

from GANEX import socketio

# socketio = get_socket()

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