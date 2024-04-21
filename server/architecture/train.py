from architecture.pix2pix import Pix2Pix
from architecture.generator import generator
from architecture.discriminator import discriminator
from architecture.lossfunctions import generator_loss,discriminator_loss
from architecture.optimizers import generator_optimizer,discriminator_optimizer
from utility.dataloader import load_dataset
from path import SMALL_DATASET
from saveimage import callbacks
import os

pix2pix_gan = Pix2Pix(generator, discriminator)

pix2pix_gan.compile(c_gen_optimizer=generator_optimizer,
                  c_disc_optimizer=discriminator_optimizer,
                  gen_loss_fn=generator_loss,
                  disc_loss_fn=discriminator_loss)

train_ds = load_dataset(os.path.join(SMALL_DATASET),4)
haze_image, clear_image  = next(iter(train_ds))

hist = pix2pix_gan.fit(train_ds, epochs=200,batch_size = 4, callbacks=callbacks,verbose=1)
generator.save('generator_model')
