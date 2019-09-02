
import os
import json

from flask import Flask, render_template
from flask_socketio import SocketIO

import threading
import  time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, async_mode='threading') # this is required to work with threading 

# project Dictionary
projects_dict = {}

# main folder
@app.route('/')
def sessions():
    return render_template('getProjectPath.html')


if __name__ == "__main__":
  
    if os.path.isfile("projects.json"):

        with open("projects.json") as pf:
            # global projects_dict
            projects_dict = json.load(pf)
            pf.close()
    else:
        with open("projects.json", "w+") as pf:
            # global projects_dict
            json.dump(projects_dict, pf)
            pf.close()

    socketio.run(app, debug=True)