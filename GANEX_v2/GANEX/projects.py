from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_pymongo import ObjectId



from GANEX.db import get_db
from GANEX.forms import CreateProject_form

# Blue print
bp = Blueprint('projects', __name__)




@bp.route('/index')
def index():
    return render_template('projects/index.html')

@bp.route('/create', methods=('GET', 'POST'))
def create():
    pro_form = CreateProject_form()
    db = get_db()

    col = db["projects"] # projects table
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

        if error is None:
            pdict = {"name":pro_form.projectName.data,"path":pro_form.projectPath.data}

            x = col.insert_one(pdict)
            print(x.inserted_id) #out.inserted_id
            # flash(x.inserted_id) # remove this one, if redirect the page
            return redirect(url_for('projects.create'))

    return render_template('projects/create.html', form=pro_form, projects=all_projects)


@bp.route('/<pid>/delete', methods=('GET',))
def delete(pid):
    db = get_db()
    col = db['projects']
    query = {"_id":ObjectId(pid)} # need this Object ID
    x =col.delete_one(query)
    print(query)
    #pid = request.id
    print(pid)
    print(x.deleted_count)

    return redirect(url_for('projects.create'))