from flask import Flask, redirect, url_for, render_template, request, session, flash, Response, stream_with_context
from datetime import timedelta
from camera import VideoCamera 
import py.resize as py_resize
import py.gan as py_gan
from py.twitter_bot import twitter_bot

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
        # return render_template('index.html', input_shape= input_shape, input_vec=input_vec)
        return redirect('/numb')
#リアルタイム処理
def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.disable_buffering()
    return rv


def gene():
    while True:
        py_x = np.random.randint(100, 400)
        time.sleep(1)
        yield str(py_x)

@app.route('/numb')
def numb():
    py_str = gene()
    return Response(stream_with_context(stream_template('index.html',str = py_str)))


@app.route('/output/<name>')
def output(name):
    cap = VideoCamera()
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
        frame=camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/feed')
def feed():
    return Response(generate(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/generategan')
def generategan():
    return render_template("generategan.html", output=output)

if __name__ == '__main__':
    #threaded=Falseに設定するといいとネットでみたが、generategan階層に移動できなかった
    # app.run(debug=True,host='127.0.0.1', threaded=False)
    app.run(debug=True,host='127.0.0.1')