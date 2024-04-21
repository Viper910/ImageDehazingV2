from path import DATASET
from tensorflow.keras import Model, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
from utility.dataloader import load_dataset
from inceptionBlock import InceptionBlock
from utility.visualization import subplot
from tensorflow.keras.initializers import RandomNormal
# from tensorflow.keras.utils.vis_utils import plot_model
import os
import tensorflow as tf

image_shape = (256,256,3)

class Generator(Model):
    def __init__(self):
        super(Generator, self).__init__()
        
        self.init = RandomNormal(stddev=0.02, seed=123)
        
        self.conv1 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')
        self.conv2 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')
        self.pool1 = layers.MaxPooling2D(pool_size=(2, 2))
        
        self.conv3 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')
        self.conv4 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')
        self.pool2 = layers.MaxPooling2D(pool_size=(2, 2))

        self.conv5 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')
        self.conv6 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')
        self.pool3 = layers.MaxPooling2D(pool_size=(2, 2))

        self.conv7 = layers.Conv2D(256, (3, 3), activation='relu', padding='same')
        self.conv8 = layers.Conv2D(256, (3, 3), activation='relu', padding='same')
        self.pool4 = layers.MaxPooling2D(pool_size=(2, 2))

        self.conv9 = layers.Conv2D(512, (3, 3), activation='relu', padding='same')
        self.conv10 = layers.Conv2D(512, (3, 3), activation='relu', padding='same')

        self.i1 = InceptionBlock(128, False)
        self.i2 = InceptionBlock(128, True)
        self.i3 = InceptionBlock(128, True)
        self.i4 = InceptionBlock(128, True)

        self.up6 = layers.Concatenate(axis=-1)
        self.conv11 = layers.Conv2D(256, (3, 3), activation='relu', padding='same')
        self.conv12 = layers.Conv2D(256, (3, 3), activation='relu', padding='same')

        self.up7 = layers.Concatenate(axis=-1)
        self.conv13 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')
        self.conv14 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')

        self.up8 = layers.Concatenate(axis=-1)
        self.conv15 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')
        self.conv16 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')

        self.up9 = layers.Concatenate(axis=-1)
        self.conv17 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')
        self.conv18 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')

        self.conv19 = layers.Conv2D(3, (1, 1), activation='tanh')
        
        self.convT1 = layers.Conv2DTranspose(256, (2, 2), strides=(2, 2), padding='same')
        self.convT2 = layers.Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')
        self.convT3 = layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')
        self.convT4 = layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')
        
    def call(self, batch):
        conv1 = self.conv1(batch)
        conv1 = self.conv2(conv1)
        pool1 = self.pool1(conv1)

        conv2 = self.conv3(pool1)
        conv2 = self.conv4(conv2)
        pool2 = self.pool2(conv2)

        conv3 = self.conv5(pool2)
        conv3 = self.conv6(conv3)
        pool3 = self.pool3(conv3)
        
        conv4 = self.conv7(pool3)
        conv4 = self.conv8(conv4)
        pool4 = self.pool4(conv4)

        conv5 = self.conv9(pool4)
        conv5 = self.conv10(conv5)
        print(batch)
        i1 = self.i1(batch)
        i2 = self.i2(i1)
        i3 = self.i3(i2)
        i4 = self.i4(i3)

        up6 = self.up6([self.convT1(conv5), conv4, i4])
        conv6 = self.conv11(up6)
        conv6 = self.conv12(conv6)

        up7 = self.up7([self.convT2(conv6), conv3, i3])
        conv7 = self.conv13(up7)
        conv7 = self.conv14(conv7)

        up8 = self.up8([self.convT3(conv7), conv2, i2])
        conv8 = self.conv15(up8)
        conv8 = self.conv16(conv8)

        up9 = self.up9([self.convT4(conv8), conv1, i1])
        conv9 = self.conv17(up9)
        conv9 = self.conv18(conv9)

        conv10 = self.conv19(conv9)
        return conv10
    
    
    def build_summary(self, input_shape=image_shape):
        inp = Input(shape = input_shape)
        return Model(inputs = [inp], outputs = self.call(inp))
    
    
    
    
generator = Generator()

# plot_model(generator.build_summary(), show_shapes=True, dpi=64)


train_ds =load_dataset(os.path.join(DATASET),4)
haze_image, clear_image  = next(iter(train_ds))
gen_output = generator(haze_image)
# subplot(haze_image, gen_output, 'Haze Image', 'Generated')
