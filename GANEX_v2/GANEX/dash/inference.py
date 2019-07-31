from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form

#from GANEX import events
# from . import events
#from . import dash
# from .. import socketio

# Blue print
bp = Blueprint('inference', __name__, url_prefix='/run')

# Inference
@bp.route('/<pid>/<expid>/inference/', methods=('GET',))
def inference(pid, expid):
    return render_template('run/inference.html', pid=pid, expid=expid)