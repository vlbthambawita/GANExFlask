from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form
from GANEX.fastGAN.task import run
from GANEX.triggers import init_triggers

# Blue print
bp = Blueprint('runexp', __name__, url_prefix='/run')

# RUN experiments using this page
@bp.route('/<pid>/<expid>/runexp/', methods=('GET','POST'))
def runexp(pid, expid):

    if request.method == "POST":
        print("POST request received")
        run(get_db(),pid, expid)

    return render_template('run/runexp.html', pid=pid, expid=expid)
