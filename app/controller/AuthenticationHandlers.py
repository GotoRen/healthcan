import tornado.web
import hashlib
from model.user import user 

# Pages that require authentication inherit from this class.
class SigninBaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

# Screen sample after Signin.
class SignedinPageHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return

        _id = int(tornado.escape.xhtml_escape(self.current_user))
        _signedInUser = user.find(_id)

        self.render("dashboard.html", user=_signedInUser)

# Sigin Process.
class SigninHandler(SigninBaseHandler):
    def get(self):
        _message = self.get_argument("message", None)
        messages = []

        if _message is not None: messages.append(_message)

        self.render("signin.html", errors=[], messages=messages)

    def post(self):
        _email = self.get_argument("form-email", None)
        _raw_pass = self.get_argument("form-password", None)
        
        errors = []

        if _email == None or _raw_pass == None:    
            if _email == None: errors.append("Sign in ID(Email Address) is required.")
            if _raw_pass == None: errors.append("Password is required.")
            self.render("signin.html", errors=errors, messages=[])
            return

        _pass = hashlib.sha224(_raw_pass.encode()).hexdigest()
        u = user.find_by_email(_email)

        if u == None or _pass != u.attr["password"]:
            errors.append("Sorry, your ID(Email Address) or password cannot be recognized.")
            self.render("signin.html", errors=errors, messages=[])
            return

        self.set_secure_cookie("user", str(u.attr["id"]))
        self.redirect("/")

# Signout Process.
class SignoutHandler(SigninBaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/signin?message=%s" % tornado.escape.url_escape("You are now signed out."))

# Signup Process.
class SignupHandler(SigninBaseHandler):
    def get(self):
        self.render("signup.html", errors=[], messages=[])

    def post(self):
        _email = self.get_argument("form-email", None)
        _name = self.get_argument("form-name", None)
        _raw_pass = self.get_argument("form-password", None)
        
        errors = []
        if _email == None: errors.append("ID(Email Address) is required.")
        if _name == None: errors.append("Name is required.")
        if _raw_pass == None: errors.append("Password is required.")
        if len(errors) > 0:
            self.render("signup.html", errors=errors, messages=[])
            return

        _pass = hashlib.sha224(_raw_pass.encode()).hexdigest()
        u = user.find_by_email(_email)

        if u is not None:
            self.render("signup.html", errors=["The ID(Email Address) cannot be used."], messages=[])
            return

        u = user.build()
        u.attr["email"] = _email
        u.attr["name"] = _name
        u.attr["password"] = _pass
        u.save()
        
        self.redirect("/signin?message=%s" % tornado.escape.url_escape("Sign up is complete. Please continue to sign in."))
