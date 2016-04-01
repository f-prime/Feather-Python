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
