import torch
class GanTrainer():

    def __init__(self, gan):
        self.gan = gan
        self.iters = 0
        self.epoch = 0


    def train(self, num_epochs):
       # iters = 0
        total_epochs = self.gan.recorder.get_exp_info("total_epochs")
     

        for epoch in range(num_epochs):
            
            self.gan.recorder.record_exp_info("current_epoch", epoch +1) #update current epoch
            self.gan.recorder.record_exp_info("total_epochs", total_epochs + epoch +1)  # update total epoch

            for i, data in enumerate(self.gan.dataloader, 0):

                ############################
                # (1) Update D network: maximize log(D(x)) + log(1 - D(G(z)))
                ###########################
                ## Train with all-real batch
                self.gan.netD.zero_grad()
                # Format batch
                real_cpu = data[0].to(self.gan.device)
                b_size = real_cpu.size(0)
                label = torch.full((b_size,), self.gan.real_label, device=self.gan.device)
                # Forward pass real batch through D
                output = self.gan.netD(real_cpu).view(-1)
                # Calculate loss on all-real batch
                errD_real = self.gan.criterion(output, label)
                # Calculate gradients for D in backward pass
                errD_real.backward()
                D_x = output.mean().item()
                print("gan trainer:", D_x)
                


                ## Train with all-fake batch
                # Generate batch of latent vectors
                noise = torch.randn(b_size, int(self.gan.hyperparams["nz"]), 1, 1, device=self.gan.device)
                # Generate fake image batch with G
                fake = self.gan.netG(noise)
                label.fill_(self.gan.fake_label)
                # Classify all fake batch with D
                output = self.gan.netD(fake.detach()).view(-1)
                # Calculate D's loss on the all-fake batch
                errD_fake = self.gan.criterion(output, label)
                # Calculate the gradients for this batch
                errD_fake.backward()
                D_G_z1 = output.mean().item()
                # Add the gradients from the all-real and all-fake batches
                errD = errD_real + errD_fake
                # Update D
                self.gan.optimizerD.step()
                print("error D:", errD.item())
                


                ############################
                # (2) Update G network: maximize log(D(G(z)))
                ###########################
                self.gan.netG.zero_grad()
                label.fill_(self.gan.real_label)  # fake labels are real for generator cost
                # Since we just updated D, perform another forward pass of all-fake batch through D
                output = self.gan.netD(fake).view(-1)
                # Calculate G's loss based on this output
                errG = self.gan.criterion(output, label)
                # Calculate gradients for G
                errG.backward()
                D_G_z2 = output.mean().item()
                # Update G
                self.gan.optimizerG.step()

                print("D_G_z2:", D_G_z2)

                # save stat records
                self.gan.recorder.record_train_stat(self.iters, "D_x", D_x)
                self.gan.recorder.record_train_stat(self.iters, "D_G_z1", D_G_z1)
                self.gan.recorder.record_train_stat(self.iters, "errD", errD.item())
                self.gan.recorder.record_train_stat(self.iters, "D_G_z2", D_G_z2)
                
                self.iters += 1 
            
            self.save_checkpoint(self.gan.recorder.get_exp_info("total_epochs"), "EPOCH")
           
        self.gan.recorder.record_exp_info("current_epoch", 0) # reset current epoch to 0

   
    def retrain(self, num_epochs):
        total_epochs = self.gan.recorder.get_exp_info("total_epochs")


    
    def save_checkpoint(self, checkpoint_iter, checkpoint_type):
        model_path = self.gan.recorder.generate_checkpoint_path(checkpoint_iter, checkpoint_type)
        torch.save({
            'G_state_dict': self.gan.netG.state_dict(),
            'D_state_dict': self.gan.netD.state_dict(),
            'optimizerG_state_dict': self.gan.optimizerG.state_dict(),
            'optimizerD_state_dict': self.gan.optimizerD.state_dict()
        }, model_path)


        print("Model path:", model_path)

    def load_checkpoint(self, checkpoint_iter, checkpoint_type):
        pass




