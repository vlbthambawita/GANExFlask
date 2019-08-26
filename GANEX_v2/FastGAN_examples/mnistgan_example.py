
from fastgan.fastganmodels import FastGANBaseModel
from fastgan.fastgannets import SimpleGenerator, SimpleDescriminator 
from fastgan.fastgantrainer import FastGANTrainer

from torchvision import datasets, transforms
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.utils as vutils
from torch.autograd import Variable


class MnistSimpleGAN(FastGANBaseModel):
    
    def __init__(self, db, pid, expid):
        super().__init__(db, pid, expid)

        self.gt = MNIST_trainer(self)
    

    

    def prepare_data(self):
        hyperparams = self.recorder.get_hyper_params()
        dataroot = self.recorder.get_exp_info("expDataPath")

        transform = transforms.Compose([
                    transforms.ToTensor(),
                    transforms.Normalize(mean=(0.5,), std=(0.5,))])

        self.dataset = datasets.MNIST(root=dataroot, train=True, transform=transform, download=True)

        self.dataloader = torch.utils.data.DataLoader(dataset=self.dataset, 
                                        batch_size=int(hyperparams["batch_size"]), 
                                        shuffle=True)

        self.recorder.record_dataloader_size(len(self.dataloader))

    def set_device(self):
        hyperparams = self.recorder.get_hyper_params()
        self.device = torch.device("cuda:0" if (torch.cuda.is_available() and 
                                                int(hyperparams["ngpu"]) > 0) else "cpu")


    
    def generate_input_image_grid(self, path):

        self.prepare_data()
        self.set_device()

        real_data_batch = next(iter(self.dataloader))
        # real_data_batch = real_data_batch.view(real_data_batch.size(0), 1, 28, 28)
        vutils.save_image(real_data_batch[0].to(self.device)[:64], path, nrow=8, padding=2)

    def init_nets(self):
        hyperparams = self.recorder.get_hyper_params()

        self.netG = SimpleGenerator(int(hyperparams["ngpu"]),
                                    int(hyperparams["nz"]))

        self.netD = SimpleDescriminator(int(hyperparams["ngpu"]))

        self.netG.to(self.device)
        self.netD.to(self.device)

    def init_criterion(self):
        self.criterion = nn.BCELoss()

    def init_optimizers(self):
        hyperparams = self.recorder.get_hyper_params()
        self.optimizerD = optim.Adam(self.netD.parameters(), lr=float(hyperparams["lr"]), 
                                    betas=(float(hyperparams["beta1"]), 0.999)
                                    )
        self.optimizerG = optim.Adam(self.netG.parameters(), lr=float(hyperparams["lr"]), 
                                    betas=(float(hyperparams["beta1"]), 0.999)
        )

    


        

class MNIST_trainer(FastGANTrainer):
    def __init__(self, gan):
        super().__init__(gan)

    def train(self, num_epochs):
         # self.total_epochs = int(self.gan.recorder.get_exp_info("total_epochs")) + 1

         hyperparams = self.gan.recorder.get_hyper_params()

         print("Train method is working ...================")

         for epoch in range(num_epochs):

            for i, (images, _) in enumerate(self.gan.dataloader):

                bs = images.shape[0]
                #print(bs)
                images = images.view(bs, -1).cuda()
                images = Variable(images)
                # print("image size =", images.shape)
                # Create the labels which are later used as input for the BCE loss
                real_labels = torch.ones(bs, 1).cuda()
                real_labels = Variable(real_labels)
                fake_labels = torch.zeros(bs, 1).cuda()
                fake_labels = Variable(fake_labels)

                # ================================================================== #
                #                      Train the discriminator                       #
                # ================================================================== #
                self.gan.netD.zero_grad()
                # Compute BCE_Loss using real images where BCE_Loss(x, y): - y * log(D(x)) - (1-y) * log(1 - D(x))
                # Second term of the loss is always zero since real_labels == 1
                outputs = self.gan.netD(images)
                d_loss_real = self.gan.criterion(outputs, real_labels)
                real_score = outputs
                
                # Compute BCELoss using fake images
                # First term of the loss is always zero since fake_labels == 0
                z = torch.randn(bs, int(hyperparams["nz"])).cuda()
                z = Variable(z)
                fake_images = self.gan.netG(z)
                outputs = self.gan.netD(fake_images)
                d_loss_fake = self.gan.criterion(outputs, fake_labels)
                fake_score = outputs
                
                # Backprop and optimize
                # If D is trained so well, then don't update
                d_loss = d_loss_real + d_loss_fake
                
                d_loss.backward()
                self.gan.optimizerD.step()
                # ================================================================== #
                #                        Train the generator                         #
                # ================================================================== #
                self.gan.netG.zero_grad()
                # Compute loss with fake images
                z = torch.randn(bs, int(hyperparams["nz"])).cuda()
                z = Variable(z)
                fake_images = self.gan.netG(z)
                outputs = self.gan.netD(fake_images)
                
                # We train G to maximize log(D(G(z)) instead of minimizing log(1-D(G(z)))
                # For the reason, see the last paragraph of section 3. https://arxiv.org/pdf/1406.2661.pdf
                g_loss = self.gan.criterion(outputs, real_labels)
                
                # Backprop and optimize
                # if G is trained so well, then don't update
                #reset_grad()
                g_loss.backward()
                self.gan.optimizerG.step()
                

                #print("Finisjhed============")
                self.gan.recorder.record_iters(i +1)
                print(i)

                
            
            print("Finished iters")
            # self.gan.recorder.record_exp_info("total_epochs", int(self.total_epochs))
            self.gan.recorder.add_total_epoch()
            print("add total epoch")
            self.gan.recorder.record_iters(0) # reset iters

            current_total_epoch = self.gan.recorder.read_total_epoch()


            # after read total epoch, collect plot data
            # recording stats to plot
            self.gan.recorder.record_train_stat(current_total_epoch, "d_loss", d_loss.item())
            self.gan.recorder.record_train_stat(current_total_epoch, "g_loss", g_loss.item())
            


            self.save_checkpoint(current_total_epoch, "EPOCH") # save model for each epoch
            self.save_generator_progress(current_total_epoch, 64)

            self.gan.recorder.record_exp_info("current_epoch", epoch +1) #update current epoch
         self.gan.recorder.record_exp_info("current_epoch", 0) # reset current epoch to 0


    def save_inference_output(self, iter, num_of_samples):
        """
        To save the output of trained checkpoints
        """
        hyperparams = self.gan.recorder.get_hyper_params()
        
        z = torch.randn(num_of_samples, int(hyperparams["nz"])).cuda()
        z = Variable(z)

        imgpath = self.gan.recorder.add_image("INFERENCED", iter=iter) 
        self.gan.netG.eval()
        fake = self.gan.netG(z).detach().cpu()
        vutils.save_image(fake.view(num_of_samples, 1, 28, 28), imgpath, nrow=8, padding=2)
        print("Inferenced Image saved")

    def save_generator_progress(self, iter, num_of_samples):
        imgpath = self.gan.recorder.add_image("GENDATA", iter=iter)
        hyperparams = self.gan.recorder.get_hyper_params()
        
        z = torch.randn(num_of_samples, int(hyperparams["nz"])).cuda()
        z = Variable(z)
        with torch.no_grad():
            fake = self.gan.netG(z).detach().cpu()
        vutils.save_image(fake.view(num_of_samples, 1, 28, 28), imgpath, nrow=8, padding=2)
    







