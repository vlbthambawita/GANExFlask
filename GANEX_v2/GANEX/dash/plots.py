from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response, jsonify
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId

import time
import json

from GANEX.db import get_db
from GANEX.forms import CreateProject_form
from GANEX.plots import training_plots
from GANEX.dlexmongo import getTrainStatsList, addPlotStat, getPlotStats, addPlotStat

# Blue print
bp = Blueprint('plots', __name__, url_prefix='/run')

# plots
@bp.route('/<pid>/<expid>/plots/', methods=('GET',))
def plots(pid, expid):
    db = get_db()
    #col_trainstat = db["trainstats"].find({"expid":expid})
    statlist = getTrainStatsList(db, expid)

    return render_template('run/plots.html', pid=pid, expid=expid, statlist=statlist) #trainstat=col_trainstat



@bp.route('/<pid>/<expid>/updateplot', methods=('GET',))
def updateplot(pid, expid):

    db = get_db()
    # print("plot update method")
    # print("statItem===",request.args.get("statItem"))

    def generate():
        #x = 0
        statlist = getPlotStats(db, expid)
        print("getplotruning")
        
        while len(statlist) > 0:
            
            scat_plot = training_plots.trainLossPlot(db, expid, statlist)
            #data = [] 
            #for r in db["trainstats"].find({"expid":expid},{"_id": 0, "value": 1}):
             #   data.append(r["value"])
            # plots = json.dumps({"plot1":scat_plot, "plot2": scat_plot})

            #yield "data:" + str(x) + "\n\n"
            # yield f"data:{data}\n\n"
            yield f"data:{scat_plot}\n\n"
            

            #x = x + 1
            time.sleep(0.5)
            #print(scat_plot)

    return Response(generate(), mimetype= 'text/event-stream')


@bp.route("/<pid>/<expid>/updatePlotStatType", methods=('GET',))
def updatePlotStatType(pid, expid):
    db = get_db()
    print("update plot stat type")
    plot_stat_name= request.args.get("statName")
    print(plot_stat_name)
    addPlotStat(db, expid, plot_stat_name)

    # addPlotStat(db, expid)
    return jsonify(x=5)