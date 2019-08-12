import torch
import torch.nn as nn
import torch.nn.functional as F


##############################################################
# These are simple generator and descriminator
##############################################################
# Simple Generator
class SimpleGenerator(nn.Module):
    def __init__(self, ngpu, nz):
        super(SimpleGenerator, self).__init__()

        self.ngpu = ngpu

        self.fc1 = nn.Linear(nz, 256)
        self.fc2 = nn.Linear(256, 512)
        self.fc3 = nn.Linear(512, 1024)
        self.fc4 = nn.Linear(1024, 784)

    def forward(self, x):
        x = F.leaky_relu(self.fc1(x), negative_slope=0.2)  # fc1 --> leak_relu()
        x = F.leaky_relu(self.fc2(x), negative_slope=0.2)  # fc2 --> leak_relu()
        x = F.leaky_relu(self.fc3(x), negative_slope=0.2)  # fc3 --> leak_relu()
        x = torch.tanh(self.fc4(x))
        return x


# Simple Descriminator
class SimpleDescriminator(nn.Module):
    def __init__(self, ngpu):
        super(SimpleDescriminator, self).__init__()

        self.ngpu = ngpu

        self.fc1 = nn.Linear(28 * 28, 1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc3 = nn.Linear(512, 256)
        self.fc4 = nn.Linear(256, 1)

    def forward(self, x):
        x = F.leaky_relu(self.fc1(x), negative_slope=0.2)  # x--> fc1 --> leak_relu(0.2) --> x
        x = F.dropout(x, 0.3)  # x --> dropout(0.3) --> x
        x = F.leaky_relu(self.fc2(x), negative_slope=0.2)
        x = F.dropout(x, 0.3)
        x = F.leaky_relu(self.fc3(x), negative_slope=0.2)
        x = F.dropout(x, 0.3)
        x = torch.sigmoid(self.fc4(x))
        return x

#####################################################################
# These are DCGAN generator and Descriminator
# Source: Pytorch Documentation
# Link: https://pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html
#####################################################################

# Generator Code
class DCGenerator(nn.Module):
    def __init__(self,ngpu:int, nz:int, ngf:int, nc:int):
        super(DCGenerator, self).__init__()
        self.ngpu = ngpu
        self.main = nn.Sequential(
            # input is Z, going into a convolution
            nn.ConvTranspose2d(nz, ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # state size. (ngf*8) x 4 x 4
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            # state size. (ngf*4) x 8 x 8
            nn.ConvTranspose2d( ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            # state size. (ngf*2) x 16 x 16
            nn.ConvTranspose2d( ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
            # state size. (ngf) x 32 x 32
            nn.ConvTranspose2d( ngf, nc, 4, 2, 1, bias=False),
            nn.Tanh()
            # state size. (nc) x 64 x 64
        )

    def forward(self, input):
        return self.main(input)


# Descriminator code
class DCDiscriminator(nn.Module):
    def __init__(self, ngpu,  nc, ndf):
        super(DCDiscriminator, self).__init__()
        self.ngpu = ngpu
        self.main = nn.Sequential(
            # input is (nc) x 64 x 64
            nn.Conv2d(nc, ndf, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf) x 32 x 32
            nn.Conv2d(ndf, ndf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*2) x 16 x 16
            nn.Conv2d(ndf * 2, ndf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*4) x 8 x 8
            nn.Conv2d(ndf * 4, ndf * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 8),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*8) x 4 x 4
            nn.Conv2d(ndf * 8, 1, 4, 1, 0, bias=False),
            nn.Sigmoid()
        )

    def forward(self, input):
        return self.main(input)

#################################################
# Start Simple Conditional Gan
# source 1: https://github.com/znxlwm/pytorch-MNIST-CelebA-cGAN-cDCGAN
# soruce 2: https://github.com/znxlwm/pytorch-generative-model-collections/blob/master/CGAN.py
# source 3: https://github.com/malzantot/Pytorch-conditional-GANs

# These two networks are based on source 1.
#################################################
# Simple Conditional Generator
class SimpleConditionalGenerator(nn.Module):
    def __init__(self, ngpu, nz, nclass):
        super().__init__()

        self.ngpu = ngpu

        self.fc1 = nn.Linear(nz, 256)
        self.fc1_1 = nn.Linear(nclass, 256)
        self.fc2 = nn.Linear(512, 512)
        self.fc3 = nn.Linear(512, 1024)
        self.fc4 = nn.Linear(1024, 784)

    def forward(self, x, y):
        # Generate from input noise
        x = F.leaky_relu(self.fc1(x), negative_slope=0.2)  # fc1 --> leak_relu()
        # Generate from labels
        y = F.leaky_relu(self.fc1_1(y), negative_slope=0.2)

        x = torch.cat([x, y], 1)

        x = F.leaky_relu(self.fc2(x), negative_slope=0.2)  # fc2 --> leak_relu()
        x = F.leaky_relu(self.fc3(x), negative_slope=0.2)  # fc3 --> leak_relu()
        x = torch.tanh(self.fc4(x))
        return x

# Simple Conditional Descriminator
class SimpleConditionalDescriminator(nn.Module):
    def __init__(self, ngpu, nclass): # nclass: number of classes
        super().__init__()

        self.ngpu = ngpu

        self.fc1 = nn.Linear(28 * 28, 1024)
        self.fc1_1 = nn.Linear(nclass, 1024)
        self.fc2 = nn.Linear(2048, 512)
        self.fc3 = nn.Linear(512, 256)
        self.fc4 = nn.Linear(256, 1)

    def forward(self, x, y):
        x = F.leaky_relu(self.fc1(x), negative_slope=0.2)  # x--> fc1 --> leak_relu(0.2) --> x
        x = F.dropout(x, 0.3)  # x --> dropout(0.3) --> x
        y = F.leaky_relu(self.fc1_1(y), negative_slope=0.2)
        y = F.dropout(y, 0.3)

        x = torch.cat([x, y], 1)

        x = F.leaky_relu(self.fc2(x), negative_slope=0.2)
        x = F.dropout(x, 0.3)
        x = F.leaky_relu(self.fc3(x), negative_slope=0.2)
        x = F.dropout(x, 0.3)
        x = torch.sigmoid(self.fc4(x))
        return x