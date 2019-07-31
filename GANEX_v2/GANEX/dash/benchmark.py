from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form

# Blue print
bp = Blueprint('benchmark', __name__, url_prefix='/run')


# Benchmarking
@bp.route('/<pid>/<expid>/benchmark/', methods=('GET',))
def benchmark(pid, expid):
    return render_template('run/benchmark.html', pid=pid, expid=expid)