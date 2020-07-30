from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
app = Flask(__name__)
app.secret_key = "hello"
#Opencvから毎回入ってくるであろう値
input_shape = ["4"]
input_vec = [500, 500]
# global output
# app.permanent_session_lifetime = timedelta(minutes=5)
#　渡すデータ

#メイン画面
@app.route('/', methods = ["POST", "GET"])
def index_render():
    if request.method == "POST":
        # session.permanent = True
        #htmlのidから取得されるoutput名をPythonで取得
        output = request.form["com"]
        # print(output)
        # session["output"] = output
        #output関数をレダイレクトで呼び出している
        return redirect(url_for("output"))
    else:
        # return render_template("index.html")
        return render_template("index.html", input_shape= input_shape, input_vec=input_vec)
        #ここで渡している

#積み木終了時のGANからの結果表示と、ツイッタBOTへの値渡し
@app.route('/output')
def output():
    # input_image = from_opencv
    # gan(input_image)
    # return render_template("output.html", gan_data= gan())
    # if "output" in session:
    #     output = session["output"]
    return render_template("output.html", output=output)
    #ここで渡している

def opencv():
    output_cv_image = None
    #Opencvのプログラムを実行（別ファイル）取得した映像を吐き出す
    return output_cv_image

def gan(input_image):
    output_gan = None
    #GANのプログラムを実行（別ファイル）取得した画像を吐き出す
    return output_gan

def twitter_bot():
    #twitter_botのプログラムを実行（別ファイル）
    return 



# def main():
#     # app.debug = True
#     app.run(debug = True)
    

if __name__ == '__main__':
    app.run(debug = True)