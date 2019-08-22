#from GANEX.dlexmongorecorder import DLExMongoRecorder
#from GANEX.fastGAN.ganTrainer.ganTrainer import GanTrainer
from .fastgantrainer import FastGANTrainer
from .delexrecorder.dlexmongorecorder import DLExMongoRecorder


class FastGANBaseModel():

    def __init__(self, db, pid, expid):

        self.db = db
        self.pid = pid
        self.expid = expid
        self.recorder = DLExMongoRecorder(self.db, self.pid, self.expid)
        self.gt = FastGANTrainer(self)

    def prepare_data(self):
        """
        A method to prepare data

        set:
            self.dataset
            self.dataloader
            self.recorder.record --> dataloader_size
        """
        pass

    def generate_input_image_grid(self, path):
        """
        Generate imput image grid using self.dataloader and save to path
        """
        pass

    
    def setDevice(self):
        """
        Set self.device here.
        """
        pass

    def weight_init(self, m):
        """
        Define initial weight initialization method here.
        """
        pass


    def run(self):
        """
        Main compulsory method for training the model
        """
        pass

    def rerun(self):
        """
        Main compulsory method to rerun models
        """
        print("====Rerun method is runing from base model========")
        pass

    def inference(self):
        """
        Main method to do inference form a pre trained model
        """
        pass

