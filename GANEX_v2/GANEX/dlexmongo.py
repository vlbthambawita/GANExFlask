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


def addGanTypes(db, name, filename, classname):

    col = db["gantypes"]
    query = {"name": name, "file":filename ,"class": classname}

    x = col.insert_one(query)
    print("Inserted GAN type", x.inserted_id)

def addInfoToExp(db, expId, fieldName, fieldValue):
    query ={"_id":ObjectId(expId)}
    new_field = {"$set": {fieldName: fieldValue}}
    x = db["experiments"].update_one(query, new_field)

    print("new field inserted.")

def addInfoToHWSettings(db, expId, fieldName, fieldValue):
    query ={"_id":ObjectId(expId)}
    new_field = {"$set": {fieldName: fieldValue}}
    x = db["experiments"].update_one(query, new_field)

    print("New feild wad added to hardwaresettings table")


# get methods

def getGANInfo(db, expid):
    col = db.experiments
    query = {"_id": ObjectId(expid)}

    ganType =  col.find_one(query)["type"]

    ganClass = db.gantypes.find_one({"name": ganType})["class"]

    ganFile = db.gantypes.find_one({"name" : ganType})["file"]

    print("GAN class:", ganClass)
    print("GAN file:", ganFile)

    return (ganFile, ganClass)

def getTrainStatsList(db, expid):
    col = db.trainstats 
    query = {"expid":expid}
    x = col.find(query, {"_id": 0, "expid": 0 , "epoch": 0})

    statList = []
    for key in iter(x.next()):
        statList.append(key)

    print(statList)
    return statList

def addPlotStat(db, expid, plotstatName):
    col = db.plotsetting

    query ={"expid": expid, "plotstat":plotstatName }
    x = col.insert_one(query)
