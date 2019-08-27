import os
from flask import Flask, g

from dash import Dash
import dash_html_components as html

# import flask
#import flask_socketio
from flask_socketio import SocketIO

from . import db
from . import projects
from . import experiments
#from . import run
from GANEX.dash import summary,data, hyperparam, trainsettings, runexp, plots, inference, benchmark

from . import config
from .events import init_events
#from . import events

# from GANEX.plots import dashplot

socketio = SocketIO(async_mode='threading') # add websocket #'async_mode='threading'


'''
def register_dashapps(app):
    # add plotlydash apps
    dashapp1 = Dash( __name__,
                server=app,
                routes_pathname_prefix='/dash/'
            )

    dashapp1.layout = html.Div("My Dash app")

    dashapp2 = Dash( __name__,
                server=app,
                routes_pathname_prefix='/dash2/'
            )

    #dashapp2.layout = dashplot.dashapp1()

'''

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
    init_events(socketio)

    # add socket to app context
    #g.socket = socketio
    
    
    #register_dashapps(app)
    # dashplot.dashapp1(app)
    # dashplot.dashapp2(app)
    

    
    

    return app

