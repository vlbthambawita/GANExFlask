
# pytorch
import torch
import torch.nn as nn
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils
import torch.optim as optim


#fastGAN
from GANEX.fastGAN.ganNets.ganNets import DCGenerator, DCDiscriminator
from GANEX.fastGAN.ganTrainer.ganTrainer import GanTrainer

from GANEX.dlexmongorecorder import DLExMongoRecorder
import time
import numpy as np


class DCGAN():

    def __init__(self, db, pid, expid):

        self.db = db
        self.pid = pid
        self.expid = expid
        self.recorder = DLExMongoRecorder(self.db, self.pid, self.expid)
        self.gt = GanTrainer(self)
    

    def setsettings(self):
        self.dataroot = self.recorder.get_exp_info("expDataPath")
        self.hyperparams = self.recorder.get_hyper_params()
        print("data roor=", self.dataroot)
        print("hyper param=", self.recorder.get_hyper_params() ) #

        # self.workers = 

    # parepare data
    def prepareData(self):
        
        #hyperparams = self.recorder.get_hyper_params()
        # Create the dataset
       # print("data root:", self.recorder.get_exp_info("expDataPath"))
       # print("Imgae size:", hyperparams["image_size"])
        hyperparams = self.recorder.get_hyper_params()
        dataroot = self.recorder.get_exp_info("expDataPath")

        self.dataset = dset.ImageFolder(root=dataroot,
                                        transform = transforms.Compose([
                                            transforms.Resize(int(hyperparams["image_size"])),
                                            transforms.CenterCrop(int(hyperparams["image_size"])),
                                            transforms.ToTensor(),
                                            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                                        ]))

        # get data set sample only for testing
        #self.dataset_sample = torch.utils.data.Subset(self.dataset, [i for i in range(500)])

        print("Dataset is OK", self.dataset)
        print("Batch size:", hyperparams["batch_size"])
        print("workers:", hyperparams["workers"])

        self.dataloader = torch.utils.data.DataLoader(self.dataset, 
                                                    batch_size=int(hyperparams["batch_size"]),
                                                shuffle=True, 
                                                num_workers=int(hyperparams["workers"]))

        # record dataloader size
        self.recorder.record_exp_info("dataloader_size", len(self.dataloader))

        

    # save image grid
    def generate_input_image_grid(self, path):
        # new updates
        self.prepareData()
        self.setDevice()
        real_data_batch = next(iter(self.dataloader))
        vutils.save_image(real_data_batch[0].to(self.device)[:64], path, nrow=8, padding=2)


                                    
    # setup device 
    def setDevice(self):
        hyperparams = self.recorder.get_hyper_params()
        self.device = torch.device("cuda:0" if (torch.cuda.is_available() and 
                                                int(hyperparams["ngpu"]) > 0) else "cpu")
        print("device:", self.device)

    def weight_init(self, m):
        classname = m.__class__.__name__
        if classname.find('Conv') != -1:
            nn.init.normal_(m.weight.data, 0.0, 0.02)
        elif classname.find('BatchNorm') != -1:
            nn.init.normal_(m.weight.data, 1.0, 0.02)
            nn.init.constant_(m.bias.data, 0)

    def initNets(self):
        hyperparams = self.recorder.get_hyper_params()

        self.netG = DCGenerator(int(hyperparams["ngpu"]), 
                                int(hyperparams["nz"]), 
                                int(hyperparams["ngf"]), 
                                int(hyperparams["nc"]))

        self.netD = DCDiscriminator(int(hyperparams["ngpu"]),
                                    int(hyperparams["nc"]),
                                    int(hyperparams["ndf"])
                                    )

        self.netG.to(self.device)
        self.netD.to(self.device)

        self.netG.apply(self.weight_init)
        self.netD.apply(self.weight_init)

    def initCriterion(self):
        self.criterion = nn.BCELoss()

    def initNoiseAndLabels(self):
        hyperparams = self.recorder.get_hyper_params()
        self.fixed_noise = torch.randn(64, int(hyperparams["nz"]), 1, 1, device=self.device)
        self.real_label = 1
        self.fake_label = 0

    def initOptimizers(self):
        hyperparams = self.recorder.get_hyper_params()
        self.optimizerD = optim.Adam(self.netD.parameters(), lr=float(hyperparams["lr"]), 
                                    betas=(float(hyperparams["beta1"]), 0.999)
                                    )
        self.optimizerG = optim.Adam(self.netG.parameters(), lr=float(hyperparams["lr"]), 
                                    betas=(float(hyperparams["beta1"]), 0.999)
        )

    def run(self):
        train_settings = self.recorder.get_train_settings()

        print("running run method:", self.expid)
        self.setsettings()

        print("prepare data")
        self.prepareData()
        print("Data preparation finished")
        self.setDevice()
        print("Set device is finished")
        self.initNets()
        print("Init Nets finished")
        self.initCriterion()
        print("initialize criterion")
        self.initNoiseAndLabels()
        print("initialized noise and labels")
        self.initOptimizers()
        print("inittialize optimizers")

        #self.gt = GanTrainer(self)
        print("initialized gan trainer")

        #if btn_value=="BTN_TRAIN":
        print("gan trainer started")
        self.gt.train(int(train_settings["num_epochs"]))
        print("gan trainer is working")
        self.recorder.set_exp_state("RETRAIN")

       # elif btn_value == "BTN_RETRAIN":
       #     print("BTN RETRAIN CLICKED")
        #    self.gt.retrain(int(train_settings["num_epochs"]))
        #    self.recorder.set_exp_state("RETRAIN")

    def rerun(self):
        train_settings = self.recorder.get_train_settings()

        print("running run method:", self.expid)
        self.setsettings()

        print("prepare data")
        self.prepareData()
        print("Data preparation finished")
        self.setDevice()
        print("Set device is finished")
        self.initNets()
        print("Init Nets finished")
        self.initCriterion()
        print("initialize criterion")
        self.initNoiseAndLabels()
        print("initialized noise and labels")
        self.initOptimizers()
        print("inittialize optimizers")

        self.gt.retrain(int(train_settings["num_epochs"]))
        self.recorder.set_exp_state("RETRAIN")


       
    def inference(self, model_path):
        self.setsettings()
        self.setDevice()
        self.initNets()
        self.initOptimizers()
        self.initNoiseAndLabels()
        self.gt.load_checkpoint(model_path)
        self.gt.save_inference_output(self.gt.total_epochs)

        #imgpath = self.gan.recorder.add_image("INFERENCED", iter=self.gt.total_epochs)
        print("Running gan inference")

       # self.recorder.getSetting("expDataPath")
        
        #for i in range(5):
          #  print(i)
           # j= i*2
            #self.recorder.recordEpochTrainStat(i, "test_value", np.random.rand(1)[0])
            # self.recorder.recordEpochTrainStat(i, "test_value_2", np.random.rand(1)[0])
          #  time.sleep(1)

        #self.recorder.setExpState("RETRAIN")
        print("Finished........!!!!!!!!!!!!!!!")




