####################################
### Created by k18039-後藤 廉
### Created by k18079-伴 晶樹
####################################
### 内容：ヘルスキャンハンドラ（関数）群
### ファイル：HealthCanHandlers.py
####################################

# トルネードライブラリ
import tornado.ioloop
import tornado.web
from tornado.web import MissingArgumentError
# 現在日時の取得
import datetime
# 算術演算ライブラリ
import decimal
from decimal import Decimal
# 親クラス(user.py, healthcan.py)の読み込み
from model.user import user
from model.healthcan import healthcan
# 認証関係コントローラの読み込み
from controller.AuthenticationHandlers import SigninBaseHandler
# DB接続関連
from db import DBConnector
# os, sys
import os
import sys


### データの一覧表示 
class HealthcansHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # 他の画面からのメッセージを取得
        _message = self.get_argument("message", None)
        messages = []

        if _message is not None: 
            messages.append(_message)

        # 検索項目を取得
        _user_id= self.get_argument("user_id", None)
        _name= self.get_argument("name", None)

        # ユーザーごとのヘルスキャンデータを取得
        if _user_id is not None:
            results = healthcan.user_id(_id, _user_id)
        elif _name is not None:
            results = healthcan.name(_id, _name)
        else:
            results = healthcan.select_by_user_id(_signedInUser.attr["id"])
        self.render("healthcans.html",
            user=_signedInUser,
            healthcans=results,
            messages=messages,
            user_id=_user_id,
            name=_name,
            errors=[])


### データの詳細表示
class HealthcanShowHandler(SigninBaseHandler):
    def get(self, id):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        hc = healthcan.find(id)
        if hc is None: 
            raise tornado.web.HTTPError(404) # データが見つからない場合は404エラーを返す
        if hc.attr["user_id"] != _signedInUser.attr["id"]: 
            raise tornado.web.HTTPError(404) # ユーザーIDが異なる場合も404エラーを返す

        self.render("healthcan_form.html", user=_signedInUser, mode="show", healthcan=hc, messages=[], errors=[])


### データの新規登録
class HealthcanCreateHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        hc = healthcan.build()
        self.render("healthcan_form.html", user=_signedInUser, mode="new", healthcan=hc, messages=[], errors=[])

    def post(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # POSTされたパラメータを取得
        p_user_id = self.get_argument("form-user_id", None)
        p_name = self.get_argument("form-name", None)
        p_height = self.get_argument("form-height", None)
        p_weight = self.get_argument("form-weight", None)
        p_date = self.get_argument("form-date", None)
        p_time = self.get_argument("form-time", None)
        p_bmi = self.get_argument("form-bmi", None)
        p_pro_weight = self.get_argument("form-pro_weight", None)
        p_diff_weight = self.get_argument("form-diff_weight", None)
        
        # ヘルスキャンデータの組み立て
        hc = healthcan.build()

        # パラメータエラーチェック
        errors = []
        ########################################################################################
        # ユーザID
        if p_user_id is None:
            errors.append("ユーザIDは必須です。")
        else:
            hc.attr["user_id"] = int(p_user_id)
        # 名前
        if p_name is None: 
            errors.append("名前は必須です。")
        hc.attr["name"] = p_name
        # 身長
        if p_height is None: 
            errors.append("身長は必須です。")
        hc.attr["height"] = Decimal(p_height)
        # 体重
        if p_weight is None: 
            errors.append("体重は必須です。")
        hc.attr["weight"] = Decimal(p_weight)
        # 日付
        input_day = datetime.datetime.strptime(p_date, '%Y-%m-%d')
        hc.attr["date"] = input_day.date()
        # 時間
        input_time = datetime.datetime.strptime(p_time, '%H:%M:%S')
        hc.attr["time"] = input_time.time()
        # BMI
        hc.attr["bmi"] = Decimal(p_bmi)
        # 適正体重
        hc.attr["pro_weight"] = Decimal(p_pro_weight)
        # 適正体重との差
        hc.attr["diff_weight"] = Decimal(p_diff_weight)
        ########################################################################################

        if len(errors) > 0: # エラーは新規登録画面に渡す
            self.render("healthcan_form.html", user=_signedInUser, mode="new", healthcan=hc, messages=[], errors=[])
            return
        
        # 登録
        # print(vars(hc))
        hc_id = hc.save()
        if hc_id == False:
            self.render("healthcan_form.html", user=_signedInUser, mode="new", healthcan=hc, messages=[], errors=["登録時に致命的なエラーが発生しました。"])
            print('debug-登録失敗')
        else:
            # 登録画面へリダイレクト(登録完了の旨を添えて)
            self.redirect("/healthcans?message=%s" % tornado.escape.url_escape("新規登録完了しました。(ID:%s)" % hc_id))
            print('debug-登録完了')
