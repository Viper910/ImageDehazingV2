from tensorflow.keras import Model, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
from utility.dataloader import load_dataset
import tensorflow as tf
import os
from path import DATASET
from generator import gen_output
from utility.visualization import subplot
from tensorflow.keras import Model

class Discriminator(Model):
    def __init__(self):
        super(Discriminator, self).__init__()

        self.init = tf.keras.initializers.RandomNormal(stddev=0.02, seed=123)

        self.concat = layers.Concatenate()

        self.conv1 = layers.Conv2D(64, (4, 4), strides=(2, 2), padding='same', kernel_initializer=self.init)
        self.leaky_relu1 = layers.LeakyReLU(alpha=0.2)

        self.conv2 = layers.Conv2D(128, (4, 4), strides=(2, 2), padding='same', kernel_initializer=self.init)
        self.batch_norm2 = layers.BatchNormalization()
        self.leaky_relu2 = layers.LeakyReLU(alpha=0.2)

        self.conv3 = layers.Conv2D(256, (4, 4), strides=(2, 2), padding='same', kernel_initializer=self.init)
        self.batch_norm3 = layers.BatchNormalization()
        self.leaky_relu3 = layers.LeakyReLU(alpha=0.2)

        self.conv4 = layers.Conv2D(512, (4, 4), strides=(2, 2), padding='same', kernel_initializer=self.init)
        self.batch_norm4 = layers.BatchNormalization()
        self.leaky_relu4 = layers.LeakyReLU(alpha=0.2)

        self.conv5 = layers.Conv2D(512, (4, 4), padding='same', kernel_initializer=self.init)
        self.batch_norm5 = layers.BatchNormalization()
        self.leaky_relu5 = layers.LeakyReLU(alpha=0.2)

        self.conv6 = layers.Conv2D(1, (4, 4), padding='same', kernel_initializer=self.init)
        self.sigmoid = layers.Activation('sigmoid')

    def call(self, inp, tar):
        x = self.concat([inp, tar])

        x = self.conv1(x)
        x = self.leaky_relu1(x)

        x = self.conv2(x)
        x = self.batch_norm2(x)
        x = self.leaky_relu2(x)

        x = self.conv3(x)
        x = self.batch_norm3(x)
        x = self.leaky_relu3(x)

        x = self.conv4(x)
        x = self.batch_norm4(x)
        x = self.leaky_relu4(x)

        x = self.conv5(x)
        x = self.batch_norm5(x)
        x = self.leaky_relu5(x)

        x = self.conv6(x)
        patch_out = self.sigmoid(x)

        return patch_out

    def build_summary(self, input_shape=(256,256,3)):
        inp = Input(shape = input_shape)
        tar = Input(shape = input_shape)
        return Model(inputs = [inp, tar], outputs = self.call(inp, tar))
    
    
discriminator = Discriminator()


# train_ds =load_dataset(os.path.join(DATASET),4)
# haze_image, clear_image  = next(iter(train_ds))
# disc_output = discriminator(gen_output, haze_image)
# subplot(haze_image, disc_output, 'Haze Image', 'Discriminated')
