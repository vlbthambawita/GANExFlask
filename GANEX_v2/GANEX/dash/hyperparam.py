from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form

from GANEX.dlexmongo import setHyperparamDict, getHyperparamDict, get_default_hyperparams

# Blue print
bp = Blueprint('hyperparam', __name__, url_prefix='/run')

# Hyperparameter setup page
@bp.route('/<pid>/<expid>/hyperparam/', methods=('GET',))
def hyperparam(pid, expid):

    db = get_db()
    hyperdict = getHyperparamDict(db, expid)
    default_params = list(get_default_hyperparams(db, pid))

    return render_template('run/hyperparam.html', pid=pid, expid=expid, hyperdict=hyperdict, default_params=default_params)

@bp.route('/<pid>/<expid>/saveparam/', methods=('GET', 'POST'))
def saveparam(pid, expid):
    db = get_db()
    hyperdict = {}
    print("save param")
    if request.method == 'POST':
        print("POSTED")
        form_data_dict = request.form.to_dict()
        current_dict = getHyperparamDict(db, expid)

        if current_dict != None:
            updated_current_dict = getDifferenceDict(current_dict, form_data_dict)


            setHyperparamDict(db, expid, updated_current_dict)

        else:
            updated_current_dict = form_data_dict
            setHyperparamDict(db, expid, updated_current_dict)
        
        #for k, v in request.form:
        #    print(k)

    return redirect(url_for('hyperparam.hyperparam', pid=pid, expid=expid, hyperdict=updated_current_dict))


def getDifferenceDict(originalDict, newDict):

    for key,value in newDict.items():
        if (value != "") and (value != originalDict[key]) :
            originalDict[key] = newDict[key]

    return originalDict
