from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form

# Blue print
bp = Blueprint('summary', __name__, url_prefix='/run')


# Summary page
@bp.route('/<pid>/<expid>/summary/', methods=('GET',))
def summary(pid, expid):
    return render_template('run/summary.html', pid=pid, expid=expid)