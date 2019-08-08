
import pymongo
from bson.objectid import ObjectId

class DLExMongoRecorder():

    def __init__(self, db, pid, expid):
        self.db = db
        self.pid = pid
        self.expid = expid

    def getSetting(self, setting_name):

        col = self.db.experiments
        query = {"_id":ObjectId(self.expid)}
        # new_vlues = {"$set": {setting_name: setting_value}}
        # col.update_one(query, new_vlues, upsert=True)
        x =col.find(query)
        print(x.next()[setting_name])

    


    def recordEpochTrainStat(self, epoch, stat_name, stat_value ):
        col = self.db.trainstats
        query = {"expid":self.expid, "epoch": epoch }
        new_values = {"$set": {stat_name: stat_value}}
        col.update_one(query, new_values, upsert=True)

    def setExpState(self, status):
        col = self.db.experiments
        query = {"_id":ObjectId(self.expid)}
        new_value = { "$set": { "status": status } }

        col.update_one(query, new_value, upsert=True)

        
