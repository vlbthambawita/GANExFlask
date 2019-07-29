from flask_pymongo import PyMongo
from flask import current_app, g
from flask.cli import with_appcontext
import click



def get_db():
    if 'db' not in g:
        current_app.config["MONGO_URI"] = "mongodb://localhost:27017/GANEXdb"
        mongo = PyMongo(current_app)
        g.db = mongo.db

    return g.db


# Define schema
def initSchema():
    db = get_db()
    colP = db["projects"]
    testData = {"name":"test name 2", "path":"test path"}
    x = colP.insert_one(testData)
    print(x.inserted_id)
    print("collected created")
    

    

def init_db():
    db = get_db()
    initSchema()
    print(type(db))
    print(db.list_collection_names())



@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Database is OK')

def init_app(app):
    app.cli.add_command(init_db_command)


