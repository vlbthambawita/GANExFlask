from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.utils import create_gan_object
from GANEX.forms import CreateProject_form
from GANEX.fastGAN.task import run

from GANEX.dlexmongo import getExpState, setExpState, getGANInfo, delTrainStats, get_default_exp_para, update_exp_info

import time
import json
import importlib
import os
import sys

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
                (ganDir, ganFile, ganClass) = getGANInfo(db, expid)
                print("gan Dir=", ganDir)
                print("gan file=", ganFile)
                print("gan class=", ganClass)

                # import gan from gan file
                #* my_module = importlib.import_module("GANEX.fastGAN.{}".format(ganFile))
                #* gan = eval("my_module.{}(db, pid, expid)".format(ganClass))
                gan = create_gan_object(db, pid, expid, ganDir, ganFile, ganClass)
                # gan.run("BTN_TRAIN")
                gan.run()

                setExpState(db, expid, "RETRAIN")

                #run(get_db(),pid, expid, status)
                print("Training")
                #setExpState(db, expid, "RETRAIN")
                #status = getExpState(db, expid)
            except Exception as e:
                flash(str(e))




        elif request.form["runexp_btn"] == "re-train":
            try:
                # get the GAN class
                (ganDir, ganFile, ganClass) = getGANInfo(db, expid)
                print("gan file=", ganFile)
                print("gan class=", ganClass)

                # import gan from gan file
                #* my_module = importlib.import_module("GANEX.fastGAN.{}".format(ganFile))
                #* gan = eval("my_module.{}(db, pid, expid)".format(ganClass))
                gan = create_gan_object(db, pid, expid, ganDir, ganFile, ganClass)
                # * gan.run("BTN_RETRAIN")
                gan.rerun()
                setExpState(db, expid, "RETRAIN")

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

            # reset default exp para
            exp_para_list = get_default_exp_para(db, pid)
            for exp_para in exp_para_list:
                temp_dict = {exp_para["para_key"]: exp_para["para_value"]}
                update_exp_info(db, expid, temp_dict)
                print("exp para :", exp_para )


    return render_template('run/runexp.html', pid=pid, expid=expid, status=status)

