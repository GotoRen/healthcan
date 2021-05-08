import tornado.ioloop
import tornado.web
from tornado.web import MissingArgumentError
import datetime
import decimal
from decimal import Decimal
import os
import sys
from model.user import user
from model.healthcan import healthcan
from controller.AuthenticationHandlers import SigninBaseHandler
from db import DBConnector

# HealthcansHandler is index page display.
class HealthcansHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return

        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))
        _message = self.get_argument("message", None)
        messages = []

        if _message is not None: 
            messages.append(_message)

        _user_id= self.get_argument("user_id", None)
        _name= self.get_argument("name", None)

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

# HealthcanShowHandler is detailed display of data.
class HealthcanShowHandler(SigninBaseHandler):
    def get(self, id):
        if not self.current_user:
            self.redirect("/signin")
            return

        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))
        hc = healthcan.find(id)

        if hc is None: 
            raise tornado.web.HTTPError(404)
        if hc.attr["user_id"] != _signedInUser.attr["id"]: 
            raise tornado.web.HTTPError(404)

        self.render("healthcan_form.html", user=_signedInUser, mode="show", healthcan=hc, messages=[], errors=[])

# HealthcanCreateHandler is registration healthcan data.
class HealthcanCreateHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return

        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))
        hc = healthcan.build()

        self.render("healthcan_form.html", user=_signedInUser, mode="new", healthcan=hc, messages=[], errors=[])

    def post(self):
        if not self.current_user:
            self.redirect("/signin")
            return

        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        p_user_id = self.get_argument("form-user_id", None)
        p_name = self.get_argument("form-name", None)
        p_height = self.get_argument("form-height", None)
        p_weight = self.get_argument("form-weight", None)
        p_date = self.get_argument("form-date", None)
        p_time = self.get_argument("form-time", None)
        p_bmi = self.get_argument("form-bmi", None)
        p_pro_weight = self.get_argument("form-pro_weight", None)
        p_diff_weight = self.get_argument("form-diff_weight", None)
        
        hc = healthcan.build()
        errors = []
        
        # UserID
        if p_user_id is None:
            errors.append("ユーザIDは必須です。")
        else:
            hc.attr["user_id"] = int(p_user_id)
        # Name
        if p_name is None: 
            errors.append("名前は必須です。")
        hc.attr["name"] = p_name
        # Height
        if p_height is None: 
            errors.append("身長は必須です。")
        hc.attr["height"] = Decimal(p_height)
        # Weight
        if p_weight is None: 
            errors.append("体重は必須です。")
        hc.attr["weight"] = Decimal(p_weight)
        # Date
        input_day = datetime.datetime.strptime(p_date, '%Y-%m-%d')
        hc.attr["date"] = input_day.date()
        # Time
        input_time = datetime.datetime.strptime(p_time, '%H:%M:%S')
        hc.attr["time"] = input_time.time()
        # BMI
        hc.attr["bmi"] = Decimal(p_bmi)
        # PropriateWeight
        hc.attr["pro_weight"] = Decimal(p_pro_weight)
        # DifferenceWeight
        hc.attr["diff_weight"] = Decimal(p_diff_weight)
        
        if len(errors) > 0:
            self.render("healthcan_form.html", user=_signedInUser, mode="new", healthcan=hc, messages=[], errors=[])
            return
        
        hc_id = hc.save()
        if hc_id == False:
            self.render("healthcan_form.html", user=_signedInUser, mode="new", healthcan=hc, messages=[], errors=["登録時に致命的なエラーが発生しました。"])
            print('[DEBUG] 登録失敗')
        else:
            self.redirect("/healthcans?message=%s" % tornado.escape.url_escape("新規登録完了しました。(ID:%s)" % hc_id))
            print("新規登録完了しました。(ID: %s)", hc_id)
            print('[DEBUG] 登録完了') 
