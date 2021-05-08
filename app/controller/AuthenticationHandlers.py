####################################
### Created by K18039-後藤 廉
####################################
### 内容：サインイン及び認証ハンドラ（関数）群
### ファイル：AuthenticationHandlers.py
####################################

# トルネードライブラリ
import tornado.web
# パスワード暗号化のためのライブラリ 
import hashlib  
# 親クラス(user.py)の読み込み
from model.user import user 

# 認証を必要とするページは、このクラスを継承する
class SigninBaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

# サインイン後の画面サンプル
class SignedinPageHandler(SigninBaseHandler):
    # サインイン完了後のページ用サンプル(以下のimportが必須)
    # from controller.SigninHandlers import SigninBaseHandler
    # from model.user import user
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = int(tornado.escape.xhtml_escape(self.current_user))
        _signedInUser = user.find(_id)

        # その他必要な処理をここで

        # ダッシュボードを表示
        self.render("dashboard.html", user=_signedInUser)

# サインイン
class SigninHandler(SigninBaseHandler):
    def get(self):
        # パラメータを取得(2つ目の引数は、取得できない場合の初期値を設定できます。)
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None: messages.append(_message)

        # サインイン画面の表示(パラメータにメッセージが設定されていればそれを渡す)
        self.render("signin.html", errors=[], messages=messages)

    def post(self):
        # パラメータの取得
        _email = self.get_argument("form-email", None)
        _raw_pass = self.get_argument("form-password", None)
        
        # エラーメッセージの初期化
        errors = []

        # 入力項目の必須チェック
        if _email == None or _raw_pass == None:    
            if _email == None: errors.append("Sign in ID(Email Address) is required.")
            if _raw_pass == None: errors.append("Password is required.")
            self.render("signin.html", errors=errors, messages=[])
            return

        # 入力されたパスワードをsha224で一方向の暗号化
        _pass = hashlib.sha224(_raw_pass.encode()).hexdigest()

        # メールアドレスでユーザー情報を取得
        u = user.find_by_email(_email)

        # 認証(ユーザーが存在する & パスワードが一致する で認証OK)
        if u == None or _pass != u.attr["password"]:
            # 認証失敗
            errors.append("Sorry, your ID(Email Address) or password cannot be recognized.")
            self.render("signin.html", errors=errors, messages=[])
            return

        # DBに保管されたユーザーIDを文字列化して暗号化Cookieに格納
        self.set_secure_cookie("user", str(u.attr["id"]))
        # 認証が必要なページへリダイレクト
        self.redirect("/")

# サインアウト
class SignoutHandler(SigninBaseHandler):
    def get(self):
        # 認証済みの暗号化Cookieを削除
        self.clear_cookie("user")
        # サインイン画面へリダイレクト(サインアウト完了の旨を添えて)
        self.redirect("/signin?message=%s" % tornado.escape.url_escape("You are now signed out."))

# サインアップ(ユーザー登録)
class SignupHandler(SigninBaseHandler):
    def get(self):
        # サインイン画面の表示
        self.render("signup.html", errors=[], messages=[])

    def post(self):
        # パラメータの取得
        _email = self.get_argument("form-email", None)
        _name = self.get_argument("form-name", None)
        _raw_pass = self.get_argument("form-password", None)
        
        # 入力項目の必須チェック
        errors = []
        if _email == None: errors.append("ID(Email Address) is required.")
        if _name == None: errors.append("Name is required.")
        if _raw_pass == None: errors.append("Password is required.")
        if len(errors) > 0: # エラーはサインイン画面に渡す
            self.render("signup.html", errors=errors, messages=[])
            return

        # 入力されたパスワードをsha224で一方向の暗号化
        _pass = hashlib.sha224(_raw_pass.encode()).hexdigest()

        # メールアドレスでユーザー情報を取得
        u = user.find_by_email(_email)

        # メールアドレスの重複を許可しない
        if u is not None:
            self.render("signup.html", errors=["The ID(Email Address) cannot be used."], messages=[])
            return

        # ユーザー情報を保存
        u = user.build()
        u.attr["email"] = _email
        u.attr["name"] = _name
        u.attr["password"] = _pass
        u.save()
        
        # サインイン画面へリダイレクト(サインイン完了の旨を添えて)
        self.redirect("/signin?message=%s" % tornado.escape.url_escape("Sign up is complete. Please continue to sign in."))
