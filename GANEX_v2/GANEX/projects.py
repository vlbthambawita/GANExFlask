from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId

import pymongo
import os
import shutil

from GANEX.db import get_db
from GANEX.forms import CreateProject_form

from GANEX.dlexmongo import addGanTypes

# Blue print
bp = Blueprint('projects', __name__)


@bp.route('/index')
def index():
    return render_template('projects/index.html')

@bp.route('/', methods=('GET', 'POST'))
@bp.route('/create', methods=('GET', 'POST'))
def create():
    pro_form = CreateProject_form()
    db = get_db()

    col = db["projects"] # projects table
    
    #project name make as unique index
    col.create_index([("name", pymongo.ASCENDING)], unique=True)

    error = None
    all_projects = col.find({})

    print(all_projects)

    #all_projects = list(all_projects)

    # test_project = {"p1":"test1", "p2":"test2"}

    # if this for loop print outputs -
    # web page will not print outputs
    #for p in all_projects:
     #   print(p)

    if pro_form.validate_on_submit():

        try:
            if error is None:
                
                pro_name = pro_form.projectName.data
                pro_path = os.path.join(pro_form.projectPath.data, pro_name) 
                pdict = {"name":pro_name,"path":pro_path}

                # create folder
                os.mkdir(pro_path)

                x = col.insert_one(pdict)
                print(x.inserted_id) #out.inserted_id
                # flash(x.inserted_id) # remove this one, if redirect the page
                
                return redirect(url_for('projects.create'))
                
        except Exception as e:
            flash(e)


    return render_template('projects/create.html', form=pro_form, projects=all_projects)


@bp.route('/<pid>/delete', methods=('GET',))
def delete(pid):

    # clear DB
    db = get_db()

    # Delete the project folder, first
    shutil.rmtree(db.projects.find_one({"_id":ObjectId(pid)})["path"])

    col = db['projects']
    query = {"_id":ObjectId(pid)} # need this Object ID
    x =col.delete_many(query)
    

    #Delete corresponding all experiments
    db.experiments.delete_many({"pid": pid})

    

    print(query)
    #pid = request.id
    print(pid)
    print(x.deleted_count)

    return redirect(url_for('projects.create'))


@bp.route('/setGanTypes', methods=('GET',))
def setGanTypes():
    print('gan type clicked')
    db = get_db()
    addGanTypes(db, request.args.get('name'), request.args.get('file'), request.args.get('class'))



    return jsonify(x=request.args.get('name'))
