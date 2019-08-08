
from GANEX.dlexmongorecorder import DLExMongoRecorder

class DCGAN():

    def __init__(self, db, pid, expid):

        self.db = db
        self.pid = pid
        self.expid = expid
        self.recorder = DLExMongoRecorder(self.db, self.pid, self.expid)
    

    def run(self):
        print("running run method:", self.expid)

        for i in range(5):
            print(i)
            self.recorder.recordEpochTrainStat(i, "test_value", i)




