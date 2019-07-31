import os
from flask import Flask
# import flask
#import flask_socketio
from flask_socketio import SocketIO, emit

from . import db
from . import projects
from . import experiments
from . import run

from . import config



def create_app():

    # print("FLASK version:", flask.__version__)
    # print("FLASK socket:", flask.__version__)
    app = Flask(__name__)
    app.config.from_object(config.Config)
    
    # app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
    # mongo = PyMongo(app)

    # a simple page to test the app
    #@app.route('/hello')
    #def hello():
    #    return 'Hello GANEX...!'

    # initializations
    db.init_app(app)
    app.register_blueprint(projects.bp)
    app.register_blueprint(experiments.bp)
    app.register_blueprint(run.bp)

    return app

