import pymongo
import time
from flask_socketio import emit

def updateplot(socketio, db):
    # array to pass to plot window
    while(True): # is this running untile tab chnage?
        data = [] 

        #print("infinite loop")
        for r in db["trainstats"].find({},{"_id": 0, "value": 1}):
             data.append(r["value"])
        print(data)
        socketio.emit('plotdata', {"data": data}, namespace='/plot')
        time.sleep(1)
