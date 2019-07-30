from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateExperiment_form

# Blue print
bp = Blueprint('experiments', __name__)


@bp.route('/<pid>/index')
def index(pid):
    return render_template('experiments/index.html', pid=pid)


@bp.route('/<pid>/create', methods=('GET', 'POST'))
def create(pid):
    exp_form = CreateExperiment_form()
    db = get_db()

    #
    col_gans = (db["gantypes"].find({},{"_id":0}))
    #col = db["experiment"] # projects table
    gan_types = []

    for g in col_gans:
        gan_types.append((g["name"],g["run"]))
        
    print(gan_types)
    exp_form.ganType.choices = gan_types
    error = None
    #all_projects = col.find({})

    #print(all_projects)

    #all_projects = list(all_projects)

    # test_project = {"p1":"test1", "p2":"test2"}

    # if this for loop print outputs -
    # web page will not print outputs
    #for p in all_projects:
     #   print(p)

    #if pro_form.validate_on_submit():

        #if error is None:
            #pdict = {"name":pro_form.projectName.data,"path":pro_form.projectPath.data}

            #x = col.insert_one(pdict)
            #print(x.inserted_id) #out.inserted_id
            # flash(x.inserted_id) # remove this one, if redirect the page
            #return redirect(url_for('experiments.create'))

    return render_template('experiments/create.html', form=exp_form, pid=pid)