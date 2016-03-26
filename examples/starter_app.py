from feather import http


def index(data):
    method = data.request_data()['method']
    if method == "POST":
        print data.request_data()['form']
    data.respond_template("templates/starter_app.html")

routes = {
    "/":index,
}

for request in http.http("127.0.0.1", 8080):
    request.router(routes)
