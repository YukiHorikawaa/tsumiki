#-------------------------------Resize-------------------------------
import os
import numpy as np
from PIL import Image
from copy import deepcopy
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, BatchNormalization, Conv2DTranspose, Activation, Flatten, Dropout, Reshape, GlobalAveragePooling2D, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from keras.callbacks import EarlyStopping



#======================================
#画像を保存してあるフォルダ名
f = 'py/input/'
#リサイズした画像を保存するフォルダ名
f_resize = 'py/output/'
#リサイズ後のサイズ
size = 128
#======================================

#処理
#======================================
def resize_image(image_name):
    open_name = f + image_name + '.JPG'
    img = Image.open(open_name).convert("RGBA")
    img.close

    tmp = np.array(img)

    mask = tmp[:,:,3] < 240
    tmp[mask, 0] = 255
    tmp[mask, 1] = 255
    tmp[mask, 2] = 255

    img = Image.fromarray(tmp[:,:,0:3])

    width, height = img.size
    if width == height:
        tmp = img
    elif width > height:
        tmp = Image.new('RGB', (width, width), (255, 255, 255))
        tmp.paste(img, (0, (width - height) // 2))
    else:
        tmp = Image.new('RGB', (height, height), (255, 255, 255))
        tmp.paste(img, ((height - width) // 2, 0))
    img_resize = tmp.resize((size, size), Image.BICUBIC)

    fin_name = f_resize + image_name + '.JPG'
    img_resize.save(fin_name)

    print("リサイズ完了")
    print("finish")