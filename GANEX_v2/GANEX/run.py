from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form


# Blue print
bp = Blueprint('run', __name__)

# Summary page
@bp.route('/<pid>/<expid>/summary/', methods=('GET',))
def summary(pid, expid):
    return render_template('run/summary.html', pid=pid, expid=expid)

# datasetup page
@bp.route('/<pid>/<expid>/data/', methods=('GET',))
def data(pid, expid):
    return render_template('run/data.html', pid=pid, expid=expid)

# Hyperparameter setup page
@bp.route('/<pid>/<expid>/hyperparam/', methods=('GET',))
def hyperparam(pid, expid):
    return render_template('run/hyperparam.html', pid=pid, expid=expid)

# Train settings
@bp.route('/<pid>/<expid>/trainsettings/', methods=('GET',))
def trainsettings(pid, expid):
    return render_template('run/trainsettings.html', pid=pid, expid=expid)


# RUN experiments using this page
@bp.route('/<pid>/<expid>/runexp/', methods=('GET',))
def runexp(pid, expid):
    return render_template('run/runexp.html', pid=pid, expid=expid)


# plots
@bp.route('/<pid>/<expid>/plots/', methods=('GET',))
def plots(pid, expid):
    return render_template('run/plots.html', pid=pid, expid=expid)

# plots
@bp.route('/<pid>/<expid>/inference/', methods=('GET',))
def inference(pid, expid):
    return render_template('run/inference.html', pid=pid, expid=expid)

# Benchmarking
@bp.route('/<pid>/<expid>/benchmark/', methods=('GET',))
def benchmark(pid, expid):
    return render_template('run/benchmark.html', pid=pid, expid=expid)

