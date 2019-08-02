from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId

import time

from GANEX.db import get_db
from GANEX.forms import CreateProject_form

# Blue print
bp = Blueprint('benchmark', __name__, url_prefix='/run')


# Benchmarking
@bp.route('/<pid>/<expid>/benchmark/', methods=('GET',))
def benchmark(pid, expid):
    
    return render_template('run/benchmark.html', pid=pid, expid=expid)


# progress response event
@bp.route('/progress')
def progress():
    def generate():
        x = 0
        while True:
            yield "data:" + str(x) + "\n\n"
            x = x + 10
            time.sleep(0.5)
            print(x)

    return Response(generate(), mimetype= 'text/event-stream')