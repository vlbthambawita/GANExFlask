from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form
from GANEX.fastGAN.task import run

from GANEX.dlexmongo import getExpState, setExpState, getGANInfo, delTrainStats
import time
import json
import importlib

# Blue print
bp = Blueprint('runexp', __name__, url_prefix='/run')

# RUN experiments using this page
@bp.route('/<pid>/<expid>/runexp/', methods=('GET','POST'))
def runexp(pid, expid):

    db = get_db()
    status = getExpState(db, expid)
    print("status:", status)
    
    
    if status == None:
        flash("status error")

    if request.method == "POST":
        print("POST request received")
        if request.form["runexp_btn"] == "train":

            try:
                # get the GAN class
                (ganFile, ganClass) = getGANInfo(db, expid)
                print("gan file=", ganFile)
                print("gan class=", ganClass)

                # import gan from gan file
                my_module = importlib.import_module("GANEX.fastGAN.{}".format(ganFile))
                gan = eval("my_module.{}(db, pid, expid)".format(ganClass))
                gan.run("BTN_TRAIN")

                #run(get_db(),pid, expid, status)
                print("Training")
                #setExpState(db, expid, "RETRAIN")
                #status = getExpState(db, expid)
            except Exception as e:
                flash(str(e))




        elif request.form["runexp_btn"] == "re-train":
            try:
                # get the GAN class
                (ganFile, ganClass) = getGANInfo(db, expid)
                print("gan file=", ganFile)
                print("gan class=", ganClass)

                # import gan from gan file
                my_module = importlib.import_module("GANEX.fastGAN.{}".format(ganFile))
                gan = eval("my_module.{}(db, pid, expid)".format(ganClass))
                gan.run("BTN_RETRAIN")

                #run(get_db(),pid, expid, status)
                print("Training")
                #setExpState(db, expid, "RETRAIN")
                #status = getExpState(db, expid)
            except Exception as e:
                flash(str(e))
                
            print("Retraining")

        elif request.form["runexp_btn"] == "reset":
            print("Reset")
            delTrainStats(db, expid)
            setExpState(db, expid, "TRAIN")
            status = getExpState(db, expid)

    return render_template('run/runexp.html', pid=pid, expid=expid, status=status)

'''
@bp.route('/<pid>/<expid>/update')
def update(pid, expid):

    db = get_db()
    def updatestatus():
        #x = 0
        
        # print(info)
        while True:
            info ={"status": getExpState(db, expid)}
            #print(info)
            info_json = json.dumps(info)
            yield f"data:{info_json}\n\n"
            time.sleep(0.5)
            

    return Response(updatestatus(), mimetype= 'text/event-stream')

    '''


