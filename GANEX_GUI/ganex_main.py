import os
from flask import Flask, render_template, url_for, request, flash, redirect
from werkzeug.utils import secure_filename
from flask import jsonify


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def projects_window():
    return render_template('projects.htm')


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



if __name__ == "__main__":
    
    app.run(debug=True)
    