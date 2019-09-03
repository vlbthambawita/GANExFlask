from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form
from GANEX.dlexmongo import get_train_settings, set_train_settings

# Blue print
bp = Blueprint('trainsettings', __name__, url_prefix='/run')

# Train settings
@bp.route('/<pid>/<expid>/trainsettings/', methods=('GET',))
def trainsettings(pid, expid):
    db = get_db()
    current_settings = get_train_settings(db, expid)
    print(current_settings)
    return render_template('run/trainsettings.html', pid=pid, expid=expid, current_settings=current_settings)



@bp.route('/<pid>/<expid>/save_general_settings/', methods=('GET',))
def save_general_settings(pid, expid):
    db = get_db()
    print("save button clicked", request.args.to_dict())
    form_dict = request.args.to_dict()
    set_train_settings(db, expid, form_dict)
    
    return redirect(url_for('trainsettings.trainsettings', pid=pid, expid=expid))