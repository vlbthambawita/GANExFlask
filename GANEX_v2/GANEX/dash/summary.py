from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId

from GANEX.db import get_db
from GANEX.forms import CreateProject_form
from GANEX.dashapps import dashplot

import time




# Blue print
bp = Blueprint('summary', __name__, url_prefix='/run')


# Summary page
@bp.route('/<pid>/<expid>/summary/', methods=('GET',))
def summary(pid, expid):
    bar = dashplot.create_plot()
    return render_template('run/summary.html', pid=pid, expid=expid, plot=bar)

@bp.route('/updatplots')
def updatplots():
    def generate():
        x = 0
        while True:
            bar = dashplot.create_plot()
            print(bar)
            #yield "data:" + str(x) + "\n\n"
            yield f"data:{bar}\n\n"
            x = x + 10
            time.sleep(0.5)
            print(x)

    return Response(generate(), mimetype= 'text/event-stream')