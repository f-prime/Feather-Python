from feather import http

def index(request):
    print request.form_data("test")
    request.set_session("Frankie", "")
    print bool(request.get_session("Frankie"))
    request.respond("Hello")

routes = {
    "/":index,
}

http.start("localhost", 8080, routes)
