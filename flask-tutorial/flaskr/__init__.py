# application factory
# and making flasker as a package

import os
from flask import Flask
from . import db
from . import auth


# application factory function

def create_app(test_config = None):
    
    # creaet and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flasker.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page to test the app
    @app.route('/hello')
    def hello():
        return 'Hello World...!'

    db.init_app(app) # call the function
    app.register_blueprint(auth.bp) # Register the blueprint

    return app