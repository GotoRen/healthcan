import tornado.ioloop
import tornado.web
from tornado.web import MissingArgumentError
import os
import sys
import datetime
import decimal
from decimal import Decimal
from model.user import user
from model.healthcan import healthcan
from db import DBConnector
from controller.AuthenticationHandlers import (
    SigninBaseHandler,
    SigninHandler,
    SignupHandler,
    SignoutHandler,
)
from controller.HealthCanHandlers import (
    HealthcansHandler,
    HealthcanShowHandler,
    HealthcanCreateHandler,
)


class MainHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return

        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))
        _weight = healthcan.weight(_id)
        _bmi = healthcan.bmi(_id)
        self.render("dashboard.html", user=_signedInUser, weight=_weight, bmi=_bmi)


application = tornado.web.Application(
    [
        (r"/", MainHandler),
        (r"/signin", SigninHandler),
        (r"/signup", SignupHandler),
        (r"/signout", SignoutHandler),
        (r"/healthcans", HealthcansHandler),  # データの一覧表示
        (r"/healthcan/new", HealthcanCreateHandler),  # データの新規登録
        (r"/healthcan/show/([0-9]+)", HealthcanShowHandler),  # データの詳細表示
    ],
    template_path=os.path.join(os.getcwd(), "templates"),
    static_path=os.path.join(os.getcwd(), "static"),
    cookie_secret="x-D-#i&0S?R6w9qEsZB8Vpxw@&t+B._$",  # cookieの暗号化キー(システムごとにランダムな文字列を設定する)
)


if __name__ == "__main__":
    application.listen(3000, "0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()
