from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId

from GANEX.db import get_db
from GANEX.forms import CreateProject_form
from GANEX.plots import dashplot

import time




# Blue print
bp = Blueprint('summary', __name__, url_prefix='/run')


# Summary page
@bp.route('/<pid>/<expid>/summary/', methods=('GET',))
def summary(pid, expid):
    # bar = dashplot.create_plot()

    # get corresponding experiments details
    db = get_db()
    col = db["experiments"]
    query = {"_id":ObjectId(expid)}
    print("pid-", pid)
    print("expid", expid)
    output = col.find(query)

    project = db["projects"].find({"_id":ObjectId(pid)})

    for p in project:
        pinfo_dict = p
        print(pinfo_dict)
    
    for r in output:
        expinfo_dict = r
        print(expinfo_dict)


    return render_template('run/summary.html', pid=pid, expid=expid, pinfo=pinfo_dict, expinfo=expinfo_dict)

'''
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
'''