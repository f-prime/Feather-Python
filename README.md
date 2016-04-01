About
=====

Feather is a Python micro web framework that aims to be as small and simple as possible while still providing a production ready web server.

Hello World
===========

```
from feather import http                                                                                                                                                                             

def hello_world(req, res):
    res.respond("Hello World!")

http.start({
    "/":hello_world
})
```

Other Examples
=======

Sessions
-

```
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
```

Render HTML
-

```
from feather import http

def hello_world(req, res):
    res.respond_template("templates/hello_world.html")

http.start({
    "/":hello_world
})
```


URL Variables
-

```
from feather import http

def hello_name(req, res):
    res.respond("Hello {}!".format(req['params']['name']))

def hello_world(req, res):                                                                                                                                                                           
    res.respond("Hello World!")

http.start({
    "/<name>":hello_name,
    "/":hello_world,
})
```

Specifying Route Method
-

```
from feather import http

def index(req, res):
    res.respond("Hello World!")

def post_test(req, res):
    res.respond_json(req.get("form"))

routes = {
    "/":index, # Accepts all methods
    "/post_test":{ # Only accepts POST method
        "POST":post_test,
    },
}

http.start(routes)

```
