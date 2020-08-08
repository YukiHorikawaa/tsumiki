from flask import Flask, redirect, url_for, render_template, request, session, flash, Response
from datetime import timedelta
from camera import VideoCamera 
import py.resize as py_resize
import py.gan as py_gan
from py.twitter_bot import twitter_bot

import os
import numpy as np
from PIL import Image
import datetime
import random
import json

global op_flag, op_shape, op_vec, list_flag, list_shape, list_vec
list_flag = []
list_shape = []
list_vec = []

image_dir = 'py/input/'
input_dir = 'py/output/'
pred_dir = 'py/pred/'
#imageのなまえ
img_name = str(datetime.datetime.now())

app = Flask(__name__)
app.secret_key = "hello"

#Opencvから毎回入ってくるであろう値
input_shape = ["4"]
# input_vec = [500, 500]

#camera.pyのクラス
global cap
cap = VideoCamera()
input_vec = cap.frame_size()

@app.route('/', methods = ["POST", "GET"])
def index():
    if request.method == "POST":
        name = request.form['com']
        return redirect(url_for("output" ,name = name))
    else:
        input_vec = cap.frame_size()
        return render_template('index.html', input_shape= input_shape, input_vec=input_vec)

@app.route('/output/<name>')
def output(name):
    # cap = VideoCamera()
    cap.video_cap(img_name, image_dir)
    py_resize.resize_image(img_name)
    py_gan.gan_image(img_name)
    image_name = os.path.join(pred_dir, img_name) + '.JPG'
    input_name = os.path.join(input_dir, img_name) + '.JPG'
    twitter = twitter_bot()
    twitter.output('変換前', input_name)
    twitter.output(name, image_name)
    return render_template("output.html",output=name)

def generate(camera):
    while True:
        global frame, op_flag, op_shape, op_vec
        frame, op_flag, op_shape, op_vec = camera.get_frame()
        print(len(list_flag))
        # list_flag.append(op_flag)
        # list_shape.append(op_shape)
        # list_vec.append(op_vec)

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/feed')
def feed():
    return Response(generate(cap), mimetype='multipart/x-mixed-replace; boundary=frame')


def gene():
    # data = {"flag": list_flag[-1], "shape": list_shape[-1], "vec": list_vec[-1]}
    data = {"flag": op_flag, "shape": op_shape, "vec": op_vec}
    print(cap.flag())
    yield json.dumps(data)
   
@app.route('/numb')
def numb():
    return Response(gene(),mimetype='application/json')

if __name__ == '__main__':
    #threaded=Falseに設定するといいとネットでみたが、generategan階層に移動できなかった
    # app.run(debug=True,host='127.0.0.1', threaded=False)
    app.run(debug=True,host='127.0.0.1')