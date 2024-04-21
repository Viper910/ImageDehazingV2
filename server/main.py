import tensorflow as tf
import os
from path import BASE_PATH
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
import statistics
import pandas as pd
import matplotlib.pyplot as plt
from path import MODERATE_DATASET,THICK_DATASET,THIN_DATASET,DEMO_DATASET
from utility.visualization import load_dataset
from utility.dataloader import load_image,prepare_img
from keras.layers import TFSMLayer

moderate_test_ds = load_dataset(MODERATE_DATASET, 4)
thick_test_ds = load_dataset(THICK_DATASET, 4)
thin_test_ds = load_dataset(THIN_DATASET, 4)



loaded_generator =  TFSMLayer(os.path.join(BASE_PATH,'generator_model'), call_endpoint='serving_default')

ssim_list = []
psnr_list = []

def ssim_evaluation(img1, img2):
    ssim_value = ssim(img1, img2, channel_axis=2, data_range=img2.max() - img2.min())
    ssim_list.append(ssim_value)

def psnr_evaluation(img1, img2):
    psnr_value = psnr(img1,img2)
    psnr_list.append(psnr_value)
    
def evaluate_model(model, inp, tar, sno):
    pred = model(inp, training=True)
    plt.figure(figsize=(15, 15))

    inp = inp[0].numpy()
    inp = (inp + 1)/2.0
    tar = tar[0].numpy()
    tar = (tar + 1)/2.0
    pred = pred['output_1'][0].numpy()
    pred = (pred + 1)/2.0

    print(tar.shape)
    print(pred.shape)
    
    # ssim
    ssim_curr = ssim_evaluation(tar, pred)

    ## psnr
    psnr_curr = psnr_evaluation(tar, pred)

    display_list = [inp, tar, pred]
    title = ['Haze Image', 'Ground Truth', 'Predicted Image']

    if sno<=5:
        for i in range(3):
            plt.subplot(1, 3, i+1)
            plt.title(title[i])
            plt.imshow(display_list[i])
            plt.axis('off')
        plt.show()
    plt.close()

skeleton = {
        'SSIM': [],
        'PSNR': []
}


def evaluate_test(test_ds, name):
    for i, (inp, tar) in test_ds.take(len(test_ds)).enumerate():
        evaluate_model(loaded_generator, inp, tar, i)
        break

    ssim_mean = statistics.mean(ssim_list)
    psnr_mean = statistics.mean(psnr_list)

    print('Dataset-{}'.format(name))
    print(ssim_mean)
    print(psnr_mean)


    skeleton['SSIM'].append(ssim_mean)
    skeleton['PSNR'].append(psnr_mean)

    ssim_list.clear()
    psnr_list.clear()

evaluate_test(moderate_test_ds, 'Moderate')
evaluate_test(thick_test_ds, 'Thick')
evaluate_test(thin_test_ds, 'Thin')

df_res = pd.DataFrame(skeleton, index = ["Mod", "Thick", "Thin"])
print(df_res)

print(next(iter(moderate_test_ds))[1].shape)


inp = prepare_img(os.path.join(DEMO_DATASET))
for i, (inp1) in inp.take(len(inp)).enumerate():
    print(inp1.shape)
    pred = loaded_generator(inp1, training=True)
    pred = pred['output_1'][0].numpy()
    pred = (pred + 1)/2.0
    plt.figure(figsize=(15, 15))
    plt.imshow(pred)
    plt.axis('off')
    plt.show()
    plt.close()