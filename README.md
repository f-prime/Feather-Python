About
=====

Feather is a Python micro web framework that aims to be as small and simple as possible while still providing a production ready web server.

Example
=======

```
def index(data):
    method = data.request_data()['method']
    if method == "POST":
        print data.request_data()['form']                                                                                                                                                            
    data.respond_template("a.html")

routes = {
    "/":index,
}

for request in http.http("127.0.0.1", 8080):
    request.router(routes)
```
