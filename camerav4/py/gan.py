#-------------------------------Resize-------------------------------
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as k

from tensorflow.keras.models import Sequential, load_model
# from tensorflow.keras import backend


#AttributeError: ‘_thread._local’ object has no attribute ‘value’の解決策以下
# import keras.backend.tensorflow_backend as tb
# tb._SYMBOLIC_SCOPE.value = True
#-------------------------------学習modelのロード-------------------------------
# model and backend graph must be created on global

#AttributeError: ‘_thread._local’ object has no attribute ‘value’の解決策以下
import tensorflow as tf
# sess = tf.compat.v1.Session(graph=tf.import_graph_def(), config=session_conf)
# sess = tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph(), config=session_conf)

# tf.compat.v1.keras.backend.set_session(sess)

global model, graph
k.clear_session()

def autoencoder_model(encoder, decoder):
    model = Sequential()
    model.add(encoder)
    model.add(decoder)
    return model
#学習済みモデルの読込モデルを実行したいだけであれば、compile=False
encoder=load_model('py/AE_para/encoder_250.h5', compile=False)
decoder=load_model('py/AE_para/decoder_250.h5', compile=False)
autoencoder = autoencoder_model(encoder, decoder)
autoencoder.summary()
graph = tf.get_default_graph()

input_dir = 'py/output/'
pred_dir = 'py/pred/'

def gan_image(img_name):
    file_name = input_dir + img_name + '.JPG'
    img = Image.open(file_name).convert("RGB"); img.close
    img = np.array(img)
    img = (img - 127.5) / 127.5
    img = img[np.newaxis, ...]
    pred = autoencoder.predict(img)
    pred = np.squeeze(pred)
    with graph.as_default(): # use the global graph
        pred = autoencoder.predict(img)
    img = Image.fromarray(np.uint8(pred * 127.5 + 127.5))
    file_name = pred_dir + img_name + '.JPG' 
    img.save(file_name)
    print('finidh gan')