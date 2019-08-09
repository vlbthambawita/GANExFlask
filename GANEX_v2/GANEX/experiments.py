from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId

import pymongo
import os

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
    col_exp = db["experiments"] # experiments table
    col_exp.create_index([("name", pymongo.ASCENDING)], unique=True) # name unique index

    all_exps = col_exp.find({"pid":pid})

    gan_types = []

    for g in col_gans:
        gan_types.append((g["name"],g["class"]))
        
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

     
    if exp_form.validate_on_submit():

        try:
            if error is None:
                exp_name = exp_form.expName.data
                exp_gan = exp_form.ganType.data
                exp_pro_path = db.projects.find_one({"_id":ObjectId(pid)})["path"]
                print(exp_pro_path)

                #paths
                exp_path = os.path.join(exp_pro_path, exp_name)
                exp_models_path = os.path.join(exp_pro_path, exp_name + "/models")
                exp_output_path = os.path.join(exp_pro_path, exp_name + "/output")

                os.mkdir(exp_path)
                os.mkdir(exp_models_path)
                os.mkdir(exp_output_path)


                exp_dict = {"name":exp_name, "type":exp_gan, "pid": pid, "status": "TRAIN", 
                            "path":exp_path, "models_path":exp_models_path, "output_path": exp_output_path }

                x = col_exp.insert_one(exp_dict)
                print(x.inserted_id) #out.inserted_id
                # flash(x.inserted_id) # remove this one, if redirect the page
                #return redirect(url_for('experiments.create'))

        except Exception as e:
            flash(e)

    return render_template('experiments/create.html', form=exp_form, pid=pid, exps=all_exps)
    

@bp.route('/<pid>/<expid>/deleteExp', methods=('GET',))
def deleteExp(pid, expid):
    db = get_db()
    exp_col = db['experiments']
    query = {"_id":ObjectId(expid)} # need this Object ID
    
    

    x =exp_col.delete_one(query) # delete given expid

    
    print(query)
    #pid = request.id
    print(expid)
    print(x.deleted_count)

    return redirect(url_for('experiments.create', pid=pid))