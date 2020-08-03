from flask import Flask, redirect, url_for, render_template, request, session, flash, Response
from datetime import timedelta
from camera import VideoCamera 

import py.resize as py_resize
import py.gan as py_gan

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
        # session.permanent = True
        #htmlのidから取得されるoutput名をPythonで取得
        output = request.form["nm"]
        session["output"] = output
        # print(output)
        # session["output"] = output
        #output関数をレダイレクトで呼び出している
        return redirect(url_for("output"))
    else:
        return render_template('index.html', input_shape= input_shape, input_vec=input_vec)

@app.route('/output')
def output():
    # input_image = from_opencv
    # gan(input_image)
    # return render_template("output.html", gan_data= gan())
    # if "output" in session:
    #     output = session["output"]
    return render_template("output.html", output=output)
    #ここで渡している

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
    py_gan.gan_image(img_name)
    return render_template("generategan.html", output=output)

if __name__ == '__main__':
    #threaded=Falseに設定するといいとネットでみたが、generategan階層に移動できなかった
    # app.run(debug=True,host='127.0.0.1', threaded=False)
    app.run(debug=True,host='127.0.0.1')