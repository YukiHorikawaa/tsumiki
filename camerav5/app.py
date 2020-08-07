from flask import Flask, redirect, url_for, render_template, request, session, flash, Response
from datetime import timedelta
from camera import VideoCamera 
import py.resize as py_resize
import py.gan as py_gan

import os
import numpy as np
from PIL import Image
import datetime

image_dir = 'py/input/'
input_dir = 'py/output/'
pred_dir = 'py/pred/'
#imageのなまえ
img_name = str(datetime.datetime.now())

app = Flask(__name__)
app.secret_key = "hello"

#Opencvから毎回入ってくるであろう値
input_shape = ["4"]
input_vec = [500, 500]

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
    cap = VideoCamera()
    cap.video_cap(img_name, image_dir)
    py_resize.resize_image(img_name)
    py_gan.gan_image(img_name)
    return render_template("generategan.html", output=output)

if __name__ == '__main__':
    #threaded=Falseに設定するといいとネットでみたが、generategan階層に移動できなかった
    # app.run(debug=True,host='127.0.0.1', threaded=False)
    app.run(debug=True,host='127.0.0.1')