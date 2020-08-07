from flask import Flask, render_template, Response, stream_with_context, jsonify
from camera import VideoCamera
from time import sleep
import numpy as np
import json
from datetime import datetime
# from time import sleep
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate(camera):
    while True:
        frame = camera.get_frame()
        
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        #if()   積み木を検知したら、以下の処理を実行
        #積み木の形(int型)と位置情報(x座標,y座標)を送る

@app.route('/feed')
def feed():
    return Response(generate(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

def gene():
    while True:
        x = np.random.randint(100, 400)
        sleep(1)
        data = {"id": "aaa", "title": x}
        yield json.dumps(data)
   
@app.route('/numb')
def numb():
    return Response(gene(),mimetype='application/json')
        
@app.route('/j')
def j():
    return jsonify(hello='world') # Returns HTTP Response with {"hello": "world"}

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1')