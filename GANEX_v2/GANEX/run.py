from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form


# Blue print
bp = Blueprint('run', __name__)


@bp.route('/<pid>/<expid>/index/', methods=('GET',))
def index(pid, expid):
    return render_template('run/index.html', pid=pid, expid=expid)