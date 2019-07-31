from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



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