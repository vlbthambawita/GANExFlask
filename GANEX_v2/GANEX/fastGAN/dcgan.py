
from GANEX.dlexmongorecorder import DLExMongoRecorder

class DCGAN():

    def __init__(self, db, pid, expid):

        self.db = db
        self.pid = pid
        self.expid = expid
        self.recorder = DLExMongoRecorder(self.db, self.pid, self.expid)
    

    def run(self):
        print("running run method:", self.expid)
        self.recorder.getSetting("expDataPath")
        self.recorder.setExpState("RETRAIN")
        for i in range(5):
            print(i)
            j= i*2
            self.recorder.recordEpochTrainStat(i, "test_value", j)
            self.recorder.recordEpochTrainStat(i, "test_value_2", i)

        #self.recorder.setExpState("RETRAIN")




