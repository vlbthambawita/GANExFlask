
from fastgan.fastganmodels import FastGANBaseModel

class MnistSimpleGAN(FastGANBaseModel):
    
    def __init__(self, db, pid, expid):
        super().__init__(db, pid, expid)
    


    def run(self):
        print("run method is runing!!!!!!!!!!!!!!!!")
        self.recorder.set_exp_state("RETRAIN")




