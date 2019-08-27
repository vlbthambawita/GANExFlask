import torch
import torchvision.utils as vutils

class FastGANTrainer():
    """
    GAN training methods
    """

    def __init__(self, gan):
        self.gan = gan
        self.iters = 0
        self.epoch = 0
        self.total_epochs = 0

    
    def train(self, num_epochs):
        """
        Main training method for a GAN
        """
        pass

    def retrain(self, num_epochs, checkpoint_path):
        """
        Main retrain method
        """

       # self.total_epochs = int(self.gan.recorder.get_exp_info("total_epochs")) 
       # checkpoint_path_to_load = self.gan.recorder.load_checkpoint_path(self.total_epochs,"EPOCH")

        self.load_checkpoint(checkpoint_path)
        print("Retraining started")
        self.train(num_epochs)
        print("Retainign stopped")

        


    def save_checkpoint(self, checkpoint_iter, checkpoint_type):
        """
        Save checkpoint for given iter and type
        """

        model_path = self.gan.recorder.generate_checkpoint_path(checkpoint_iter, checkpoint_type)
        torch.save({
            'epoch': checkpoint_iter,
            'G_state_dict': self.gan.netG.state_dict(),
            'D_state_dict': self.gan.netD.state_dict(),
            'optimizerG_state_dict': self.gan.optimizerG.state_dict(),
            'optimizerD_state_dict': self.gan.optimizerD.state_dict()
        }, model_path)


    def load_checkpoint(self, checkpoint_path):
        """
        Load checkpoint from given path
        """
        
        checkpoint = torch.load(checkpoint_path)
        self.total_epochs = checkpoint['epoch']
        self.gan.recorder.set_total_epoch(self.total_epochs) # set total epoch to checkppoint epoch

        self.gan.netG.load_state_dict(checkpoint['G_state_dict'])
        self.gan.netD.load_state_dict(checkpoint['D_state_dict'])
        self.gan.optimizerG.load_state_dict(checkpoint['optimizerG_state_dict'])
        self.gan.optimizerD.load_state_dict(checkpoint['optimizerD_state_dict'])

        print("path to load:", checkpoint_path)


    def save_generator_progress(self, iter, num_of_samples):
        """
        Save generator progress with given key word arguments
        """
        hyperparams = self.gan.recorder.get_hyper_params()
        noise = torch.randn(num_of_samples, int(hyperparams["nz"]), 1, 1, device=self.gan.device)
        imgpath = self.gan.recorder.add_image("GENDATA", iter=iter) # can add any number of keywork args
        
        with torch.no_grad():
            fake = self.gan.netG(noise).detach().cpu()

        vutils.save_image(fake, imgpath, nrow=8, padding=2)
        print("generator progress saved")

    
    def save_inference_output(self, iter, num_of_samples):
        """
        To save the output of trained checkpoints
        """
        hyperparams = self.gan.recorder.get_hyper_params()
        
        z = torch.randn(num_of_samples, int(hyperparams["nz"])).cuda()

        imgpath = self.gan.recorder.add_image("INFERENCED", iter=iter) 
        self.gan.netG.eval()
        fake = self.gan.netG(z).detach().cpu()
        vutils.save_image(fake, imgpath, nrow=8, padding=2)
        print("Inferenced Image saved")
        