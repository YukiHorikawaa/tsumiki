from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

#外部カスタムPythonファイルをインポート
import py/opencv_tsumiki, py/gan_tshumiki, py/twitter_bot

opencv_tsumiki = opencv_tsumiki()
gan_tshumiki = gan_tshumiki()
twitter_bot = twitter_bot() 


app = Flask(__name__)
app.secret_key = "hello"
#Opencvから毎回入ってくるであろう値
input_shape = ["4"]
input_vec = [500, 500]


#メイン画面
@app.route('/', methods = ["POST", "GET"])
def index_render():
    if request.method == "POST":
        #htmlのidから取得されるoutput名をPythonで取得
        output = request.form["com"]
        #ganに挿入するための画像を取得
        finish_image = opencv_tsumiki.output()
        #ganの実行
        gan_image = gan(finish_image)
        #output関数をレダイレクトで呼び出している
        return redirect(url_for("output"))
    else:
        #ここの処理をウェブソケットでhtmlを構成？
        #ウェブソケットでOpencvの画像を取得する必要がある
        #opencvからの映像を取得
        #チャットを送っている部分の代わりに画像情報をやり取りする
        image = opencv_tsumiki.load()
        #新しく置かれた積み木の形を取得
        input_shape = opencv_tsumiki.input_shape()
        #新しく置かれた積み木の位置を取得
        input_vec = opencv_tsumiki.input_vec()
        #積み木置いたフラグ
        input_vec = opencv_tsumiki.flag()
        return render_template("index.html", input_shape= input_shape, input_vec=input_vec, image=image, flag=flag)
        #ここで渡している

#積み木終了時のGANからの結果表示と、ツイッタBOTへの値渡し
@app.route('/output')
def output():
    gan_image = gan_tshumiki.out()
    twitter_bot.out(comment, gan_image)
    output = gan_image
    return render_template("output.html", output=output)
    #ここで渡している


# def main():
#     # app.debug = True
#     app.run(debug = True)
    

if __name__ == '__main__':
    app.run(debug = True)