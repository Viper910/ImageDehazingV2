import matplotlib.pyplot as plt 
from path import MODERATE_DATASET,CSV_LOGGER_PATH
from utility.dataloader import load_dataset
from architecture.generator import generator
from tensorflow.keras.callbacks import CSVLogger
import tensorflow as tf

moderate_test_ds = load_dataset(MODERATE_DATASET,4)
inp_img, tar_img = next(iter(moderate_test_ds))

def save_images(gen, test_input, name, step):
    pred_by_gen = gen(test_input)

    test_input = (test_input[0]+ 1)/2.0
    pred_by_gen = (pred_by_gen[0]+1)/2.0

    plt.figure(figsize=(12, 12))

    display_list = [test_input, pred_by_gen]
    title = ['Input Image', 'Generated Image']

    for i in range(2):
        plt.subplot(1, 2, i+1)
        plt.title(title[i])
        plt.imshow(display_list[i])
        plt.axis('off')

    filename = '%s_generated_plot_%06d.png' % (name, (step+1))
    plt.savefig(filename)
    plt.close()
    
class ReportCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if (epoch+1)%5 == 0:
            save_images(generator, inp_img, 'CtoH', epoch)
            

callbacks = [
    CSVLogger(CSV_LOGGER_PATH),
    ReportCallback()
]