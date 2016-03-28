from feather import http

def index(request):
    request.respond("Hello World!")

routes = {
    "/":index,
}

http.start("localhost", 8080, routes)
