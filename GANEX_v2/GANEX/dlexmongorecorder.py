
import pymongo
from bson.objectid import ObjectId
import os

class DLExMongoRecorder():

    def __init__(self, db, pid, expid):
        self.db = db
        self.pid = pid
        self.expid = expid

    def get_exp_info(self, setting_name):

        col = self.db.experiments
        query = {"_id":ObjectId(self.expid)}
        # new_vlues = {"$set": {setting_name: setting_value}}
        # col.update_one(query, new_vlues, upsert=True)
        x =col.find(query)
        return x.next()[setting_name]

    def get_hyper_params(self):
        print("started get hyper param")
        col = self.db.hyperparam
        query = {"expid": self.expid}
        x = col.find(query, {"_id": 0, "expid": 0})
        # print("xxx next=", x.next())
        return x.next()

    def get_train_settings(self):
        col = self.db.train_settings
        query = {"expid": self.expid}
        output = col.find_one(query, {"_id": 0, "expid": 0})
        return output

    

    # Recording training stat values.
    def record_train_stat(self, iteration, stat_name, stat_value ):
        col = self.db.trainstats
        query = {"expid":self.expid, "iteration": iteration }
        new_values = {"$set": {stat_name: stat_value}}
        col.update_one(query, new_values, upsert=True)


    # record information about experiment (to track progress of the experiment)
    def record_exp_info(self, info_name, info_value):
        col = self.db.experiments
        query = {"_id":ObjectId(self.expid) }
        new_value = {"$set": {info_name: info_value}}
        col.update_one(query, new_value, upsert=True)


    def set_exp_state(self, status):
        col = self.db.experiments
        query = {"_id":ObjectId(self.expid)}
        new_value = { "$set": { "status": status } }

        col.update_one(query, new_value, upsert=True)


    # Handling models

    def generate_checkpoint_path(self, checkpoint_iter, checkpoint_type):

        col = self.db.models
        # checkpoint_type: "BATCH", "EPOCH".. etc.
        query = {"pid": self.pid, "expid": self.expid, "iter": checkpoint_iter,  "type": checkpoint_type }
        x = col.insert_one(query)

        print("x=",str(x.inserted_id))

        col_exp = self.db.experiments
        query_exp = {"_id": ObjectId(self.expid), "pid": self.pid}
        model_dir_path = col_exp.find_one(query_exp)["models_path"]
        print("model dir path:", model_dir_path)

        # new model path 
        model_path = os.path.join(model_dir_path, str(x.inserted_id) + ".tar")

        # update models table back
        new_value = {"$set": {"path": model_path}}

        x1 = col.update(query, new_value, upsert=True)

        print(model_path)

        return model_path

    
        
