import os
#import sys

#sys.path.append("/Users/vajirathambawita/Google Drive/developments/GANExFlask/GANEX_v2/GANEX")

from flask import Flask
# import flask
#import flask_socketio
from flask_socketio import SocketIO, emit

import db
import projects
import experiments
import run

# import config
from config import Config



#def create_app():

# print("FLASK version:", flask.__version__)
# print("FLASK socket:", flask.__version__)
app = Flask(__name__)
app.config.from_object(Config())

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

    #return app


socketio = SocketIO(app, async_mode='threading') # add websocket
socketio.run(app, debug=True)