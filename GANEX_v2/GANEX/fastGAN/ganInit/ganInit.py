
import torch
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils

from GANEX.dlexmongorecorder import DLExMongoRecorder
import matplotlib.pyplot as plt



def createDataLoader(db, pid, expid):
    # Create the dataset
    recorder = DLExMongoRecorder(db, pid, expid)
    hyperparams = recorder.getHyperParams()
    dataroot = recorder.getSetting("expDataPath")

    dataset = dset.ImageFolder(root=dataroot,
                                        transform = transforms.Compose([
                                            transforms.Resize(int(hyperparams["image_size"])),
                                            transforms.CenterCrop(int(hyperparams["image_size"])),
                                            transforms.ToTensor(),
                                            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                                        ]))

    dataloader = torch.utils.data.DataLoader(dataset, 
                                batch_size=int(hyperparams["batch_size"]),
                                shuffle=True, 
                                num_workers=int(hyperparams["workers"]))

    return dataloader

def initDevice(db, pid, expid):
    # Create the dataset
    recorder = DLExMongoRecorder(db, pid, expid)
    hyperparams = recorder.getHyperParams()
    device = torch.device("cuda:0" if (torch.cuda.is_available() and int(hyperparams["ngpu"]) > 0) else "cpu")
    return device



def generateInputImageGrid(dataloader, imgpath, device):
    real_batch = next(iter(dataloader))
    vutils.save_image(real_batch[0].to(device)[:64], imgpath, nrow=8, padding=2)
    print("grid saved")
