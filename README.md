About
=====

Feather is a Python micro web framework that aims to be as small and simple as possible while still providing a production ready web server.

Example
=======

```
from feather import http

def index(req, res):
    res.respond("Hello World!")

routes = {
    "/":index,
}

http.start(routes)

```
