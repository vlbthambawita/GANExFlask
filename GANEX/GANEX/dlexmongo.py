from flask_pymongo import ObjectId
from flask import flash
import os

#######################################
# Experiments collection handling
#######################################

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

def addInfoToExp(db, expId, fieldName, fieldValue):
    query ={"_id":ObjectId(expId)}
    new_field = {"$set": {fieldName: fieldValue}}
    x = db["experiments"].update_one(query, new_field)

    print("new field inserted.")


# get given info from the Experiment 
def getInfoExp(db, expId):
    col = db.experiments
    query = {"_id": ObjectId(expId)}
    output = col.find_one(query)
    return output

def get_exp_default_para_info(db, expid):
    col = db.experiments
    query ={"_id":ObjectId(expid)}
    output = col.find_one(query, {"_id": 0})
    print("outputttt", output)
    return output

def update_exp_info(db, expid, new_dict):
    col = db.experiments
    query ={"_id":ObjectId(expid)}
    new_value = {"$set": new_dict}
    col.update_one(query, new_value, upsert=True)
    print("updated exp info")




def addInfoToHWSettings(db, expId, fieldName, fieldValue):
    query ={"_id":ObjectId(expId)}
    new_field = {"$set": {fieldName: fieldValue}}
    x = db["experiments"].update_one(query, new_field)

    print("New feild wad added to hardwaresettings table")


##########################################################
# Default exp para collection
##########################################################

def get_default_exp_para(db, pid):
    col = db.default_exp_para
    query = {"pid": pid}
    list_output =  list(col.find(query, {"_id":0}))
    return list_output

def set_default_exp_para(db, pid, para_name, para_key, para_value):
    
    col = db.default_exp_para

    query = {"pid": pid, "para_key": para_key}
    new_value ={"$set": {"pid": pid, "para_name":para_name, 
                "para_key":para_key, "para_value": para_value}}
    
    x = col.update(query, new_value, upsert=True )

    
def del_default_exp_para(db, pid, para_key):
    col = db.default_exp_para
    query ={"pid": pid, "para_key": para_key}
    col.delete_one(query)
    print("successfullyu deleted")










#####################################################
# gantypes collection handling
######################################################



def addGanTypes(db, name, directory,  filename, classname):

    col = db["gantypes"]
    query = {"name":name, "dir":directory,  "file":filename ,"class": classname}

    x = col.insert_one(query)
    print("Inserted GAN type", x.inserted_id)


def get_gan_types(db):
    col = db.gantypes
    output = col.find({}, {"_id":0})
    return list(output)

def del_gan_type(db, gan_name):
    col = db.gantypes
    query = {"name": gan_name}
    col.delete_one(query)



# get methods

def getGANInfo(db, expid):
    col = db.experiments
    query = {"_id": ObjectId(expid)}

    ganType =  col.find_one(query)["type"]

    ganClass = db.gantypes.find_one({"name": ganType})["class"]

    ganFile = db.gantypes.find_one({"name" : ganType})["file"]

    ganDir = db.gantypes.find_one({"name" : ganType})["dir"]

    print("GAN class:", ganClass)
    print("GAN file:", ganFile)
    print("GAN Dir:", ganDir)

    return (ganDir, ganFile, ganClass)

def getTrainStatsList(db, expid):
    col = db.trainstats 
    query = {"expid":expid}
    result_count = col.count_documents(query)
    x = col.find(query, {"_id": 0, "expid": 0 , "epoch": 0})
    print("xxxx", result_count)

    statList = []
    if result_count > 0:
        for key in iter(x.next()):
            statList.append(key)

    print(statList)
    return statList


# get given train stat values as an array
def getTrainStatAsList(db, expid, stat_name):
    col = db.trainstats
    query = {"expid": expid}
    result = col.find(query, {stat_name: 1})
    print(result)


def delTrainStats(db, expid):
    col = db.trainstats
    query = {"expid": expid}
    col.delete_many(query)
    print("exp info deleted")



###############################################
# plotsettins collection
##################################################

def addPlotStat(db, expid, plotstatName, plotid):
    col = db.plotsetting

    query ={"expid": expid, "plotstat":plotstatName , "plotid": plotid}
    newvalue ={"$set" : {"expid": expid, "plotstat": plotstatName, "plotid": plotid}}
    x = col.update(query, newvalue, upsert=True)

def getPlotStats(db, expid):
    col = db.plotsetting

    query ={"expid": expid}

    output = col.find(query, {"_id": 0, "expid":0})
    plots = []

    for r in output:
        plots.append((r["plotstat"], r["plotid"]))

    print(plots)
    return plots


def del_plt_stat(db, expid, plt_stat_name, plt_id):
    col = db.plotsetting

    query = {"expid": expid, "plotstat":plt_stat_name , "plotid": plt_id}
    col.delete_one(query)





##################################################
# hyperparam collection handling
##################################################

def setHyperparamDict(db, expid, hyperparam_dict):
    col = db.hyperparam

    query = {"expid": expid}
    values = {"$set": hyperparam_dict}
    x = col.update(query, values, upsert=True)
    print("updated hyperparameters")

def getHyperparamDict(db, expid):
    col = db.hyperparam
    query = {"expid": expid}
    output = col.find_one(query, {"_id":0, "expid":0})
    return output


#############################################
# outputdata collection
###############################################

def addImage(db, expid, datatype): # type: INPUTDATA, GENDATA, INFERENCED --> return a path to image
    
    # get new id for new data
    col = db.outputdata
    query ={"expid": expid, "type": datatype}
    x = col.insert_one(query) # x.inserted_id

    col_exp = db.experiments
    query_exp = {"_id": ObjectId(expid)}
    exp_path = col_exp.find(query_exp, {"_id":0,"output_path":1})

    # new image path 
    imgpath = exp_path.next()["output_path"] + "/" + str(x.inserted_id) + ".png"

    # update outputdata collection
    new_value = {"$set": {"imgpath": imgpath}}
    x1 = col.update(query, new_value, upsert=True)


    print(x.inserted_id)
   #  print(exp_path.next())
    return imgpath

def getImagePaths(db, expid, datatype):
    col = db.outputdata
    query = {"expid": expid,  "type": datatype}

    output= col.find(query, {"_id":0, "imgpath": 1})
    print(output)
    img_path_list = []

    for path in output:
        print(path)
        img_path_list.append(path["imgpath"])

    return img_path_list

def get_output_imgs(db, expid, datatype):
    col = db.outputdata
    query = {"expid": expid,  "type": datatype}
    output= col.find(query, {"_id":0 })

    return list(output)

# del img path - old method
def delImgPath(db, expid, path):
    try:
        col = db.outputdata

        query ={"expid": expid, "imgpath": path}
        col.delete_one(query)
        os.remove(path)
    except Exception as e:
        flash(str(e))




# methods for trainsettings

def set_train_settings(db, expid, dict_settings):
    col = db.train_settings
    query = {"expid": expid}
    new_dict = {"expid": expid}
    new_dict.update(dict_settings)
    print("New dict:", new_dict)
    new_values = {"$set": new_dict}
    x = col.update(query, new_values, upsert=True)
    print("inserted settings:", x)

def get_train_settings(db, expid):
    col = db.train_settings
    query = {"expid": expid}

    output = col.find_one(query, {"_id": 0, "expid": 0})
    return output

# set and get default hyper parametersf

def set_default_hyperparam(db, pid, param_name, param_key, param_value):
    col = db.default_hyperparams
    query = {"pid": pid, "para_key": param_key}
    new_value ={"$set": {"pid": pid, "para_name":param_name, 
                "para_key":param_key, "para_value": param_value}}
    
    x = col.update(query, new_value, upsert=True )
    print("Default settings updated")

def get_default_hyperparams(db, pid):
    col = db.default_hyperparams
    query = {"pid": pid}

    output = col.find(query, {"_id": 0, "pid": 0})
    print("output:", output)
    return output

def del_default_hyperpram(db, pid, para_key):
    col = db.default_hyperparams
    query ={"pid": pid, "para_key": para_key}
    col.delete_one(query)
    print("successfullyu deleted")


    




############################################################
# Handling model collection
############################################################

def generate_checkpoint_path(db, pid, expid, checkpoint_iter, checkpoint_type):

    col = db.models
    # checkpoint_type: "BATCH", "EPOCH".. etc.
    query = {"pid": pid, "expid": expid, "iter": checkpoint_iter,  "type": checkpoint_type }
    x = col.insert_one(query)

    col_exp = db.experiments
    query_exp = {"pid": pid, "expid": expid}
    model_dir_path = col_exp.find_one(query_exp)["models_path"]

    # new model path 
    model_path = os.path.join(model_dir_path, str(x.inserted_id) + ".tar")

    # update models table back
    new_value = {"$set": {"path": model_path}}

    x1 = col.update(query, new_value, upsert=True)

    print(model_path)

    return model_path

# get available models data as list
def get_models(db, pid, expid):
    col = db.models
    query = {"pid": pid, "expid": expid}
    outputs = col.find(query, {"_id": 0})
    return list(outputs)

def del_model(db, pid, expid, model_path):
    col = db.models
    query = {"pid": pid, "expid": expid, "path": model_path}
    col.delete_one(query)
    os.remove(model_path)






