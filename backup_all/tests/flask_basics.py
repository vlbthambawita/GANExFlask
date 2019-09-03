import os
from flask import Flask, render_template, url_for, request, flash, redirect
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
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
    


if __name__ == "__main__":
    
    app.run(debug=True)