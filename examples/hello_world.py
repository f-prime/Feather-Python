from feather import http

def hello_world(req, res):
    res.respond("Hello World!")

http.start({
    "/":hello_world
})
