from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId

import time

from GANEX.db import get_db
from GANEX.forms import CreateProject_form

# Blue print
bp = Blueprint('plots', __name__, url_prefix='/run')

# plots
@bp.route('/<pid>/<expid>/plots/', methods=('GET',))
def plots(pid, expid):
    db = get_db()
    col_trainstat = db["trainstats"].find({"expid":expid})
    return render_template('run/plots.html', pid=pid, expid=expid, trainstat=col_trainstat)



@bp.route('/<pid>/<expid>/update')
def update(pid, expid):

    db = get_db()

    def generate():
        x = 0
        
        while True:

            data = [] 
            for r in db["trainstats"].find({"expid":expid},{"_id": 0, "value": 1}):
                data.append(r["value"])

            #yield "data:" + str(x) + "\n\n"
            yield f"data:{data}\n\n"
            x = x + 1
            time.sleep(0.5)
            print(data)

    return Response(generate(), mimetype= 'text/event-stream')