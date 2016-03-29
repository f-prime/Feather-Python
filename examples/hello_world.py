from feather import http

def index(req, res):
    res.respond("Hello World!")

routes = {
    "/":index,
}

http.start(routes)
