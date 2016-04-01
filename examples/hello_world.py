from feather import http

def index(req, res):
    res.respond("Hello World!")

def post_test(req, res):
    res.respond_json(req.get("form"))

routes = {
    "/":index,
    "/post_test":{
        "POST":post_test,
    },
}

http.start(routes)
