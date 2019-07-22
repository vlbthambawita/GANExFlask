import os
import json
from flask import Flask, render_template, url_for, request, flash, redirect
from werkzeug.utils import secure_filename
from flask import jsonify

#My classes
from config import Config
from app.forms import CreateProject_form
from app.projects import Project

app_dict = {} # main dictionary file to keep project info

#UPLOAD_FOLDER = '/path/to/the/uploads'
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config.from_object(Config)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods = ["GET" , "POST"])
def projects_window():
    form = CreateProject_form()

    init_app()
    print(app_dict)

    if form.validate_on_submit():
        
        project = Project(form.projectName.data, form.projectPath.data)
        app_dict[project.name] = project.full_path
        print("Added project path and created a project in", project.json_file)
        save_app_json(app_dict)

        #return redirect(url_for('projects_window', form = form))
        return render_template('projects.htm', form = form, app_dict = app_dict)

    return render_template('projects.htm', form = form, app_dict = app_dict)


@app.route("/home")
def hello():
    return render_template('home.htm')

@app.route("/about")
def about():
    return render_template("about.htm", title= "About")



## access file of the OS
@app.route("/upload")
def upload_file():
    return render_template("upload.htm")

@app.route("/train")
def train_tab():
    return render_template("train.htm")

@app.route("/interactive")
def interactive():
    print("This is working")
    return render_template("interactive.htm")
    
@app.route("/run_test_task", methods=['POST'])
def test_task():
    print("Test task is OK...")
    return render_template("train.htm")


@app.route('/background_process_1')
def background_process_1():
    try:
        print("Test")
        lang = request.args.get('proglang', 0, type=str)
        if lang.lower() == 'python':
            return jsonify(result='You are ggod')

        else:
            return jsonify(result='test')
    except Exception as e:
        return str(e)


@app.route('/background_process')
def background_process():
    
    try:
        lang = request.args.get('proglang', 0, type=str)
       # print("Test")
        if lang.lower() == 'python':
            return jsonify(result='You are wise')
        else:
            return jsonify(result='Try again.')
    except Exception as e:
        return str(e)

######### Init app and save app dictionary #########
def init_app():
    global app_dict

    if os.path.isfile("json/app.json"):

        print("Json file found")
        with open("json/app.json") as pf:
            # global projects_dict
            app_dict = json.load(pf)
            pf.close()
            print(app_dict)
    else:
        with open("json/app.json", "w+") as pf:
            # global projects_dict
            json.dump(app_dict, pf)
            pf.close()

def save_app_json(app_dict):
    with open("json/app.json", "w+") as pf:
            # global projects_dict
            json.dump(app_dict, pf)
            pf.close()

if __name__ == "__main__":
    
    app.run(debug=True)
    