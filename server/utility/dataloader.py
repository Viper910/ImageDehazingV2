import os
import tensorflow as tf
import typing as type
import path

BATCH_SIZE = 4
IMAGE_SIZE = (256,256,3)                            #Resolution 256 X 256 and 3 rgb code

def load_image(img_path:type.AnyStr):
    img = tf.io.read_file(img_path)
    img = tf.io.decode_png(img,channels=3)
    img = tf.image.resize(img,[256,256])
    img = (img / 127.5) - 1.0                       #Normaliztion for effective and fast training of model.
    
    return img

    
    
def load_paired_images(real_img_path:type.AnyStr,fake_img_path:type.AnyStr):
    real_img = load_image(real_img_path)
    fake_img = load_image(fake_img_path)
    
    return real_img, fake_img


def load_dataset(PATH:type.AnyStr,batch_size=type.AnyStr):
    HAZY_IMG_PATH = os.path.join(PATH,'input')
    hazy_images_paths = os.listdir(HAZY_IMG_PATH)
    hazy_images_paths = [os.path.join(HAZY_IMG_PATH,img) for img in hazy_images_paths]
    hazy_images_paths.sort()
    
    
    CLEAR_IMG_PATH = os.path.join(PATH,'target')
    clear_images_paths = os.listdir(CLEAR_IMG_PATH)
    clear_images_paths = [os.path.join(CLEAR_IMG_PATH,img)for img in clear_images_paths]
    clear_images_paths.sort()
    
    
    dataset = tf.data.Dataset.from_tensor_slices((hazy_images_paths, clear_images_paths))
    dataset = dataset.map(load_paired_images, num_parallel_calls = tf.data.AUTOTUNE)   # use thread for fast processing of data 
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    
    
    dataset = dataset.batch(batch_size)
    
    return dataset
    
def prepare_img(PATH:type.AnyStr):
    dataset = tf.data.Dataset.from_tensor_slices([PATH,PATH,PATH,PATH])
    dataset = dataset.map(load_image, num_parallel_calls = tf.data.AUTOTUNE)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    dataset = dataset.batch(4)
    return dataset

def convert_inp_image(PATH:type.AnyStr):
    dataset = tf.data.Dataset.from_tensor_slices([PATH])
    dataset = dataset.map(load_image, num_parallel_calls = tf.data.AUTOTUNE)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    return dataset
    
    