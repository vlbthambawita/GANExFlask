from GANEX.dlexmongorecorder import DLExMongoRecorder
from GANEX.fastGAN.ganTrainer.ganTrainer import GanTrainer

class FastGANBaseModel():

    def __init__(self, db, pid, expid):

        self.db = db
        self.pid = pid
        self.expid = expid
        self.recorder = DLExMongoRecorder(self.db, self.pid, self.expid)
        self.gt = GanTrainer(self)

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

    def init_nets(self):
        """
        Initialize networks:
        self.netG
        self.netD
        
        """

