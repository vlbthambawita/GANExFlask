from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form

# Blue print
bp = Blueprint('hyperparam', __name__, url_prefix='/run')

# Hyperparameter setup page
@bp.route('/<pid>/<expid>/hyperparam/', methods=('GET',))
def hyperparam(pid, expid):
    return render_template('run/hyperparam.html', pid=pid, expid=expid)