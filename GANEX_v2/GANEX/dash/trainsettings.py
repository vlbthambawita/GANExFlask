from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form

# Blue print
bp = Blueprint('trainsettings', __name__, url_prefix='/run')

# Train settings
@bp.route('/<pid>/<expid>/trainsettings/', methods=('GET',))
def trainsettings(pid, expid):
    return render_template('run/trainsettings.html', pid=pid, expid=expid)