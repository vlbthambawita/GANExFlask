from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form

# Blue print
bp = Blueprint('data', __name__, url_prefix='/run')


# datasetup page
@bp.route('/<pid>/<expid>/data/', methods=('GET',))
def data(pid, expid):
    return render_template('run/data.html', pid=pid, expid=expid)

# get data folder
@bp.route('/<pid>/<expid>/setDataFolder', methods=('GET', 'POST'))
def setDataFolder(pid, expid):
    print("test")
    print(request.args.get('path'))
    return jsonify(x=5)

