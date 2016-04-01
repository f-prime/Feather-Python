from feather import http, config

config.set_session_secret("it's a secret, shhhhh")

def check_login(req, res):
    res.respond("Logged in: {}".format(bool(req['session'].get("loggedin"))))

def login(req, res):
    res.set_session("loggedin", "true")
    res.redirect("/")

def logout(req, res):
    res.set_session("loggedin", "")
    res.redirect("/")

http.start({
    "/login":login,
    "/":check_login,
    "/logout":logout,
})
