import twitter
import tweepy

class twitter_bot:
    def __init__(self):
        #キーとアクセストークンを設定する
        self.consumer_key="oopQ1xJEGTpUfkydRz3lrmwBL"
        self.consumer_secret="NkhdWpvFrgl4UYw8NxaoafXDTGdXAO379xRO8dK46CTYF6dL8i"
        self.token="1278276822455578624-aHWTyOeDJBmu8FmRa5H2kRCoB98lHx"
        self.token_secret="TEa8ZwI3lHTNwkOeIcSFdaPF3VXUCIPko65dif7YuaRNK"
        self.auth = tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
        self.auth.set_access_token(self.token,self.token_secret)

    def output(self, message, path):
        # twitterへメッセージを投稿する
        # path 写真のパス
        # message ツイート内容
        api = tweepy.API(self.auth)
        api.update_with_media(filename=path,status=message)
