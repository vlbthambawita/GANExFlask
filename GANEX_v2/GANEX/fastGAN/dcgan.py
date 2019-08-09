
from GANEX.dlexmongorecorder import DLExMongoRecorder
import time
import numpy as np


class DCGAN():

    def __init__(self, db, pid, expid):

        self.db = db
        self.pid = pid
        self.expid = expid
        self.recorder = DLExMongoRecorder(self.db, self.pid, self.expid)
    

    def setsetting(self):
        self.dataroot = self.recorder.getSetting("expDataPath")
        print("data roor=", self.dataroot)
        print("hyper param=", self.recorder.getHyperParams() ) #

    def run(self):
        print("running run method:", self.expid)
        self.setsetting()
       
        self.recorder.getSetting("expDataPath")
        self.recorder.setExpState("RETRAIN")
        for i in range(5):
            print(i)
           # j= i*2
            self.recorder.recordEpochTrainStat(i, "test_value", np.random.rand(1)[0])
            self.recorder.recordEpochTrainStat(i, "test_value_2", np.random.rand(1)[0])
            time.sleep(2)

        #self.recorder.setExpState("RETRAIN")




