import os
from flask import Flask
# import flask
#import flask_socketio
from flask_socketio import SocketIO

from . import db
from . import projects
from . import experiments
#from . import run
from GANEX.dash import summary,data, hyperparam, trainsettings, runexp, plots, inference, benchmark

from . import config
# from . import events

socketio = SocketIO() # add websocket #'async_mode='threading'



def create_app(debug=False):

    # print("FLASK version:", flask.__version__)
    # print("FLASK socket:", flask.__version__)
    app = Flask(__name__)
    app.config.from_object(config.Config)
    app.debug = debug
    
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
    # app.register_blueprint(run.bp)

    # dash board blueprints
    app.register_blueprint(summary.bp)
    app.register_blueprint(data.bp)
    app.register_blueprint(hyperparam.bp)
    app.register_blueprint(trainsettings.bp)
    app.register_blueprint(runexp.bp)
    app.register_blueprint(plots.bp)
    app.register_blueprint(inference.bp)
    app.register_blueprint(benchmark.bp)

    # only for testing purpose
    #app.register_blueprint(events.bp)
    
    

    socketio.init_app(app)

    return app

