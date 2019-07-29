from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


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

    if pro_form.validate_on_submit():
        pdict = {"name":pro_form.projectName.data,"path":pro_form.projectPath.data}

        x = col.insert_one(pdict)
        print(x.inserted_id) #out.inserted_id
        flash(x.inserted_id)
        # return redirect(url_for('projects.create'))

    return render_template('projects/create.html', form=pro_form)