import pymongo
import numpy as np
import time

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
