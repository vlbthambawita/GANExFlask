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

        # initialize required things
        
    def set_train_method(self, train_method):
        self.gt.train =  FastGANTrainer(self)

    def prepare_data(self):
        """
        A method to prepare data

        set:
            self.dataset
            self.dataloader
            self.recorder.record --> dataloader_size
        """
        raise NotImplementedError


    def set_device(self):
        """
        Set self.device here.
        """
        raise NotImplementedError


    

    def generate_input_image_grid(self, path):
        """
        Compulsory method to implement.
        Generate imput image grid using self.dataloader and save to path
        """
        raise NotImplementedError


    
    

    def weight_init(self, m):
        """
        Define initial weight initialization method here.
        """
        raise NotImplementedError

    def init_nets(self):
        """
        Initialize self.netG and self.netD.
        Set nets to self.device.
        Apply self.weight_init
        """
        raise NotImplementedError

    def init_criterion(self):
        """
        Initialize a criterion
        """
        raise NotImplementedError

    def init_optimizers(self):
        """
        Initialize self.optimizerD and self.optimizerG
        """

        raise NotImplementedError


    def run(self):
        """
        Main compulsory method for training the model
        """

        #self.set_gan_trainer()

        print("Getting train settings")
        print("running run method:", self.expid)

        train_settings = self.recorder.get_train_settings()
        
        

        print("prepare data")
        self.prepare_data()
        print("Data preparation finished")

        

        self.set_device()
        print("Set device is finished")
        self.init_nets()
        print("Init Nets finished")
        self.init_criterion()
        print("initialize criterion")
        
        self.init_optimizers()
        print("inittialize optimizers")

        #self.gt = GanTrainer(self)
        print("initialized gan trainer")

       
        print("gan trainer started")
        self.gt.train(int(train_settings["num_epochs"]))
        print("gan trainer is working")
        
        # pass

    def rerun(self):
        """
        Main compulsory method to rerun models
        """
        print("Getting train settings")
        print("running run method:", self.expid)

        train_settings = self.recorder.get_train_settings()

        print("prepare data")
        self.prepare_data()
        print("Data preparation finished")
        self.set_device()
        print("Set device is finished")
        self.init_nets()
        print("Init Nets finished")
        self.init_criterion()
        print("initialize criterion")
        
        self.init_optimizers()
        print("inittialize optimizers")

        #self.gt = GanTrainer(self)
        print("initialized gan trainer")

       
        print("gan trainer started")
        self.gt.retrain(int(train_settings["num_epochs"]))
        print("gan trainer is working")

    def inference(self, model_path):
        
        self.set_device()
        self.init_nets()
        self.init_optimizers()
        
        self.gt.load_checkpoint(model_path)
        self.gt.save_inference_output(self.recorder.read_total_epoch(), 64)

