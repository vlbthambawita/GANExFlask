
# pytorch
import torch
import torch.nn as nn
import torchvision.datasets as dset
import torchvision.transforms as transforms
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
    

    def setsettings(self):
        self.dataroot = self.recorder.getSetting("expDataPath")
        self.hyperparams = self.recorder.getHyperParams()
        print("data roor=", self.dataroot)
        print("hyper param=", self.recorder.getHyperParams() ) #

        # self.workers = 

    # parepare data
    def prepareData(self):
        
        # Create the dataset
        print("data root:", self.dataroot)
        print("Imgae size:", self.hyperparams["image_size"])

        self.dataset = dset.ImageFolder(root=self.dataroot,
                                        transform = transforms.Compose([
                                            transforms.Resize(int(self.hyperparams["image_size"])),
                                            transforms.CenterCrop(int(self.hyperparams["image_size"])),
                                            transforms.ToTensor(),
                                            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                                        ]))

        # get data set sample only for testing
        self.dataset_sample = torch.utils.data.Subset(self.dataset, [i for i in range(500)])

        print("Dataset is OK", self.dataset)
        print("Batch size:", self.hyperparams["batch_size"])
        print("workers:", self.hyperparams["workers"])

        self.dataloader = torch.utils.data.DataLoader(self.dataset_sample, 
                                                    batch_size=int(self.hyperparams["batch_size"]),
                                                shuffle=True, 
                                                num_workers=int(self.hyperparams["workers"]))

        

            
                                    
    # setup device 
    def setDevice(self):
        self.device = torch.device("cuda:0" if (torch.cuda.is_available() and 
                                                int(self.hyperparams["ngpu"]) > 0) else "cpu")

    def weight_init(self, m):
        classname = m.__class__.__name__
        if classname.find('Conv') != -1:
            nn.init.normal_(m.weight.data, 0.0, 0.02)
        elif classname.find('BatchNorm') != -1:
            nn.init.normal_(m.weight.data, 1.0, 0.02)
            nn.init.constant_(m.bias.data, 0)

    def initNets(self):
        self.netG = DCGenerator(int(self.hyperparams["ngpu"]), 
                                int(self.hyperparams["nz"]), 
                                int(self.hyperparams["ngf"]), 
                                int(self.hyperparams["nc"]))

        self.netD = DCDiscriminator(int(self.hyperparams["ngpu"]),
                                    int(self.hyperparams["nc"]),
                                    int(self.hyperparams["ndf"])
                                    )

        self.netG.to(self.device)
        self.netD.to(self.device)

        self.netG.apply(self.weight_init)
        self.netD.apply(self.weight_init)

    def initCriterion(self):
        self.criterion = nn.BCELoss()

    def initNoiseAndLabels(self):
        self.fixed_noise = torch.randn(64, int(self.hyperparams["nz"]), 1, 1, device=self.device)
        self.real_label = 1
        self.fake_label = 0

    def initOptimizers(self):
        self.optimizerD = optim.Adam(self.netD.parameters(), lr=float(self.hyperparams["lr"]), 
                                    betas=(float(self.hyperparams["beta1"]), 0.999)
                                    )
        self.optimizerG = optim.Adam(self.netG.parameters(), lr=float(self.hyperparams["lr"]), 
                                    betas=(float(self.hyperparams["beta1"]), 0.999)
        )

    def run(self):
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

        self.gt = GanTrainer(self)
        print("initialized gan trainer")

        self.gt.train(1)
        print("gan trainer is working")
       
        self.recorder.getSetting("expDataPath")
        self.recorder.setExpState("RETRAIN")
        #for i in range(5):
          #  print(i)
           # j= i*2
            #self.recorder.recordEpochTrainStat(i, "test_value", np.random.rand(1)[0])
            # self.recorder.recordEpochTrainStat(i, "test_value_2", np.random.rand(1)[0])
          #  time.sleep(1)

        #self.recorder.setExpState("RETRAIN")
        print("Finished........!!!!!!!!!!!!!!!")




