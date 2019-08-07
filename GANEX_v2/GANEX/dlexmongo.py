from flask_pymongo import ObjectId

# get the experiment state
def getExpState(db, expid):
    
    status = None

    # get expetiment state
    query = {"_id":ObjectId(expid)}
    output = db["experiments"].find(query, {"_id":0, "status": 1})

    for s in output:
        status = s["status"]

    return status

def setExpState(db, expid, status):

    # get expetiment state
    query = {"_id":ObjectId(expid)}
    new_value = { "$set": { "status": status } }

    db["experiments"].update_one(query, new_value)


def addGanTypes(db, name, classname):

    col = db["gantypes"]
    query = {"name": name, "run": classname}

    x = col.insert_one(query)
    print("Inserted GAN type", x.inserted_id)