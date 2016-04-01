from feather import http

def hello_name(req, res):
    res.respond("Hello {}!".format(req['params']['name']))

def hello_world(req, res):
    res.respond("Hello World!")

http.start({
    "/<name>":hello_name,
    "/":hello_world,
})
