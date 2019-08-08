
import pymongo
from bson.objectid import ObjectId

class DLExMongoRecorder():

    def __init__(self, db, pid, expid):
        self.db = db
        self.pid = pid
        self.expid = expid

    def setSetting(self, setting_name, setting_value):

        col = self.db["settings"]
        query = {"_id", self.expid}
        new_vlues = {setting_name: setting_value}
        col.update_one(query, new_vlues, upsert=True)


    def recordEpochTrainStat(self, epoch, stat_name, stat_value ):
        col = self.db.trainstats
        query = {"expid":self.expid, "epoch": epoch }
        new_values = {"$set": {stat_name: stat_value}}
        col.update_one(query, new_values, upsert=True)

        
