import pymongo
import numpy as np
import time
from flask_socketio import emit
# from GANEX import socketio

def run(db, pid, expid):
    print("RUN method is running")
    print(db)
    print("PROJECT ID:", pid)
    print("EXP ID:", expid)

    trainstats_col = db["trainstats"]
    trainstats_col.delete_many({})

    for epoch in range(100):
        rand_value = np.random.rand(1)
        query = {"expid":expid, "epoch": epoch, "value": rand_value[0]}
        #print(rand_value)
        #print(query)
        trainstats_col.insert_one(query)


    print(list(trainstats_col.find({})))

def randnumber(socketio):
    for i in range(10):
        number = np.random.rand(1)
        print(number)
        socketio.emit('test',{'msg': 'from thread' + str(number)}, namespace='/chat')
        time.sleep(1)

