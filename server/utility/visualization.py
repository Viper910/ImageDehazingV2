import matplotlib.pyplot as plt
from utility.dataloader import load_dataset
from path import DATASET
import os


def subplot(img1, img2, title1, title2):
    fig, axes = plt.subplots(nrows=1, ncols=2)
    img1 = (img1[0] + 1) / 2.0
    img2 = (img2[0] + 1) / 2.0

    axes[0].imshow(img1)
    axes[0].set_title(title1)
    axes[0].axis('off')

    axes[1].imshow(img2)
    axes[1].set_title(title2)
    axes[1].axis('off')
    plt.show()
    
    

# train_ds =load_dataset(os.path.join(DATASET),4)
# haze_image, clear_image  = next(iter(train_ds))
# print(haze_image.shape)
# subplot(haze_image, clear_image, 'Hazy Image', 'Clear Image')