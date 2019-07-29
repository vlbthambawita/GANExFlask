import os
from flask import Flask
from . import db
from . import projects
from . import config



def create_app():

    app = Flask(__name__)
    app.config.from_object(config.Config)
    # app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
    # mongo = PyMongo(app)

    # a simple page to test the app
    @app.route('/hello')
    def hello():
        return 'Hello GANEX...!'

    # initializations
    db.init_app(app)
    app.register_blueprint(projects.bp)

    return app