from lossfunctions import generator_loss,discriminator_loss
from generator import generator
from discriminator import discriminator
from optimizers import generator_optimizer,discriminator_optimizer
from tensorflow.keras import Model
import tensorflow as tf

class Pix2Pix(Model):
    def __init__(
        self,
        clear_generator,
        clear_discriminator,
    ):
        super(Pix2Pix, self).__init__()
        self.c_gen = clear_generator
        self.c_disc = clear_discriminator

    def compile(
        self,
        c_gen_optimizer,
        c_disc_optimizer,
        gen_loss_fn,
        disc_loss_fn,
    ):
        super(Pix2Pix, self).compile()
        self.c_gen_optimizer = generator_optimizer
        self.c_disc_optimizer = discriminator_optimizer
        self.gen_loss_fn = generator_loss
        self.disc_loss_fn = discriminator_loss

    def train_step(self, batch_data):
        haze, clear = batch_data

        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
            gen_output = generator(haze, training=True)

            disc_real_output = discriminator(haze, clear, training=True)
            disc_generated_output = discriminator(haze, gen_output, training=True)

            gen_total_loss, gen_gan_loss, gen_l1_loss = generator_loss(disc_generated_output, gen_output, clear)
            disc_loss = discriminator_loss(disc_real_output, disc_generated_output)

        generator_gradients = gen_tape.gradient(
            gen_total_loss, generator.trainable_variables
        )
        discriminator_gradients = disc_tape.gradient(
            disc_loss, discriminator.trainable_variables
        )

        generator_optimizer.apply_gradients(
            zip(generator_gradients, generator.trainable_variables)
        )
        discriminator_optimizer.apply_gradients(
            zip(discriminator_gradients, discriminator.trainable_variables)
        )

        return {
            'gen_total_loss': gen_total_loss,
            'gen_gan_loss' : gen_gan_loss,
            'gen_l1_loss' : gen_l1_loss,
            'disc_loss' : disc_loss
        }
