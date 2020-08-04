from flask import Flask, redirect, url_for, render_template, request, session, flash, Response
from datetime import timedelta
from camera import VideoCamera 

import py.resize as py_resize
# import py.gan as py_gan

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping
from tensorflow.keras import backend

#AttributeError: ‘_thread._local’ object has no attribute ‘value’の解決策以下
import keras.backend.tensorflow_backend as tb
tb._SYMBOLIC_SCOPE.value = True
#-------------------------------学習modelのロード-------------------------------
# model and backend graph must be created on global
import keras.models
import tensorflow as tf
global model, graph

def autoencoder_model(encoder, decoder):
    model = Sequential()
    model.add(encoder)
    model.add(decoder)
    return model
#学習済みモデルの読込
encoder=keras.models.load_model('py/AE_para/encoder_250.h5')
decoder=keras.models.load_model('py/AE_para/decoder_250.h5')
autoencoder = autoencoder_model(encoder, decoder)
autoencoder.summary()
graph = tf.compat.v1.get_default_graph()

input_dir = 'py/output/'
pred_dir = 'py/pred/'

app = Flask(__name__)
app.secret_key = "hello"
#Opencvから毎回入ってくるであろう値
input_shape = ["4"]
input_vec = [500, 500]

#imageのなまえ
img_name = 'shapes8'

@app.route('/', methods = ["POST", "GET"])
def index():
    if request.method == "POST":
        name = request.form['com']
        return redirect(url_for("output" ,name = name))
    else:
        return render_template('index.html', input_shape= input_shape, input_vec=input_vec)

@app.route('/output/<name>')
def output(name):
    return render_template("output.html",output=name)

def generate(camera):
    while True:
        frame=camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/feed')
def feed():
    return Response(generate(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/generategan')
def generategan():
    py_resize.resize_image(img_name)
    file_name = input_dir + img_name + '.JPG'
    img = Image.open(file_name).convert("RGB"); img.close
    img = np.array(img)
    img = (img - 127.5) / 127.5
    img = img[np.newaxis, ...]
    pred = autoencoder.predict(img)
    # pred = np.squeeze(pred)
    with graph.as_default(): # use the global graph
        pred = autoencoder.predict(img)
    img = Image.fromarray(np.uint8(pred * 127.5 + 127.5))
    file_name = pred_dir + img_name + '.JPG' 
    img.save(file_name)
    print('finidh gan')
    return render_template("generategan.html", output=output)



if __name__ == '__main__':
    #threaded=Falseに設定するといいとネットでみたが、generategan階層に移動できなかった
    # app.run(debug=True,host='127.0.0.1', threaded=False)
    app.run(debug=True,host='127.0.0.1')