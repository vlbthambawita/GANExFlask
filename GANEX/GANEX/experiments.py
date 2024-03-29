from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId
from flask_socketio import emit

import pymongo
import os
import json
import shutil

from GANEX.db import get_db
from GANEX.forms import CreateExperiment_form
from GANEX.dlexmongo import (set_train_settings, set_default_hyperparam, get_default_hyperparams,
                                addInfoToExp, get_default_exp_para
                            )

# Blue print
bp = Blueprint('experiments', __name__)

# socketio = g.socket
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
    col_exp.create_index([("name", pymongo.ASCENDING), ("pid", pymongo.ASCENDING)], unique=True) # name unique index

    all_exps = col_exp.find({"pid":pid})

    gan_types = []

    for g in col_gans:
        print("gggg=", g)
        gan_types.append((g["name"], g["name"]))
        
    print(gan_types)
    exp_form.ganType.choices = gan_types
    error = None
    #all_projects = col.find({})

    # load default hyper params
    all_hyperparams = list(get_default_hyperparams(db, pid))

    
    default_para_list = list(get_default_hyperparams(db, pid))

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
                print("exp gan=", exp_gan)

                #paths
                exp_path = os.path.join(exp_pro_path, exp_name)
                exp_models_path = os.path.join(exp_pro_path, exp_name + "/models")
                exp_output_path = os.path.join(exp_pro_path, exp_name + "/output")

                os.mkdir(exp_path)
                os.mkdir(exp_models_path)
                os.mkdir(exp_output_path)


                # initialize exp inforamtion
                exp_dict = {"name":exp_name, "type":exp_gan, "pid": pid, "status": "TRAIN", 
                            "path":exp_path, "models_path":exp_models_path, "output_path": exp_output_path , "iters": 0,
                            "current_epoch": 0, "dataloader_size": 0}

                # modify exp_dict with default parameters
                exp_para_list = get_default_exp_para(db, pid)
                print("exp para list=", exp_para_list)

                for exp_para in exp_para_list:
                    print("exp para000=====", exp_para) 
                    exp_dict.update({exp_para["para_key"]: exp_para["para_value"]})

                # insert exp dict
                x = col_exp.insert_one(exp_dict)

                # add additional data to experiments collection

                #addInfoToExp

                # initialize train settings
                dict_settings = {"num_epochs": 0, "checkpoint_interval": 0, "checkpoint_type":"EPOCH"}
                set_train_settings(db, str(x.inserted_id), dict_settings)

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
    
    exp_path = exp_col.find_one(query, {"_id":0, "path": 1})

    print("exp  path", exp_path)
    shutil.rmtree(exp_path["path"]) # remove exp directoty

    x =exp_col.delete_one(query) # delete given expid

    
    print(query)
    #pid = request.id
    print(expid)
    print(x.deleted_count)

    return redirect(url_for('experiments.create', pid=pid))




@bp.route('/<pid>/default_hyperparams/')
def default_hyperparams(pid):
    db = get_db()
    print("para name:", request.args.get("para_name"))
    para_name = request.args.get("para_name")
    para_key = request.args.get("para_key")
    para_value = request.args.get("para_value")

    set_default_hyperparam(db, pid, para_name, para_key, para_value)
    all_hyperparams = list(get_default_hyperparams(db, pid))
    print(all_hyperparams)
    # all_hyperparams = json.dumps(all_hyperparams)
    return jsonify(x= all_hyperparams)




@bp.route('/delete_default_para/')
def delete_default_para():
    
    pass

# data usind socketio


