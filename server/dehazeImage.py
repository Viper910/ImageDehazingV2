import sys
import matplotlib.pyplot as plt
import os
import matplotlib
from utility.dataloader import prepare_img,convert_inp_image
from keras.layers import TFSMLayer
from path import BASE_PATH
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr

matplotlib.use('Agg')

def ssim_evaluation(img1, img2):
    ssim_value = ssim(img1, img2, channel_axis=2, data_range=img2.max() - img2.min())
    return ssim_value

def psnr_evaluation(img1, img2):
    psnr_value = psnr(img1,img2)
    return psnr_value

def generateDehazeImage(PATH,name):
    loaded_generator =  TFSMLayer(os.path.join(BASE_PATH,'generator_model'), call_endpoint='serving_default')
    inp = prepare_img(os.path.join(PATH))
    inp1 = next(iter(inp.take(1)))
    pred = loaded_generator(inp1, training=True)
    pred = pred['output_1'][0].numpy()
    pred = (pred + 1)/2.0
    plt.figure(figsize=(5, 5))
    plt.tight_layout()
    plt.imshow(pred)
    plt.axis('off')
    plt.savefig(f'static/generated/{name}.png',dpi=64) 
    plt.close()
    inpImg = convert_inp_image(os.path.join(PATH))
    inpImg = next(iter(inpImg.take(1)))
    ssim = ssim_evaluation(inpImg.numpy(),pred)
    psnr = psnr_evaluation(inpImg.numpy(),pred)
    print(ssim,psnr)
    return (ssim,psnr)    

def main():
    # Check if there are at least two command-line arguments
    if len(sys.argv) < 3 or sys.argv[1] != "--path":
        print("Usage: python program.py --path <string>")
        return
    # Get the string argument from the command line
    input_string = sys.argv[2]
    generateDehazeImage(input_string)
    return;

if __name__ == "__main__":
    main()
