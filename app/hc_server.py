####################################
### Created by k18039-後藤 廉
### Created by K18009-今泉 宏紀
### Created by k18079-伴 晶樹
####################################
### 内容：サーバ（メインコントローラ）
### ファイル：hc_server.py
####################################

# トルネードライブラリ
import tornado.ioloop
import tornado.web
from tornado.web import MissingArgumentError
# os, sys
import os
import sys
# 親クラス(user.py, healthcan.py)の読み込み
from model.user import user
from model.healthcan import healthcan
# DB接続関連
from db import DBConnector
# 現在日時の取得
import datetime
# 算術演算ライブラリ
import decimal
from decimal import Decimal
# 認証関係コントローラ, ヘルスキャンコントローラの読み込み
from controller.AuthenticationHandlers import SigninBaseHandler, SigninHandler, SignupHandler, SignoutHandler
from controller.HealthCanHandlers import HealthcansHandler, HealthcanShowHandler, HealthcanCreateHandler



class MainHandler(SigninBaseHandler):

    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))
        
        # ダッシュボードを表示
        # 追加
        _weight = healthcan.weight(_id)
        _bmi = healthcan.bmi(_id)
        self.render("dashboard.html", user=_signedInUser, weight=_weight, bmi=_bmi)
        


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/signin", SigninHandler),
    (r"/signup", SignupHandler),
    (r"/signout", SignoutHandler),
    (r"/healthcans", HealthcansHandler),                    # データの一覧表示
    (r"/healthcan/new", HealthcanCreateHandler),            # データの新規登録
    (r"/healthcan/show/([0-9]+)", HealthcanShowHandler),    # データの詳細表示
    ],
    template_path=os.path.join(os.getcwd(),  "templates"),
    static_path=os.path.join(os.getcwd(),  "static"),
    cookie_secret="x-D-#i&0S?R6w9qEsZB8Vpxw@&t+B._$",       # cookieの暗号化キー(システムごとにランダムな文字列を設定する)
)



if __name__ == "__main__":
    args = sys.argv
    if len(args)>1:
        if args[1] == "migrate":
            healthcan.migrate()
            user.migrate()
        if args[1] == "db_cleaner":
            healthcan.db_cleaner()
            user.db_cleaner()
        if args[1] == "help":
            print("usage: python hc_server.py migrate # prepare DB")
            print("usage: python hc_server.py db_cleaner # remove DB")
            print("usage: python hc_server.py # run web server")
    else:
        application.listen(3000, "0.0.0.0")
        tornado.ioloop.IOLoop.instance().start()
