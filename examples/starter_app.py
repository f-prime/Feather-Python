from feather import http


def index(response):
    data = response.request_data()
    method = data['method']
    if method == "POST":
        print data['form']
    print data['session']
    data.respond_template("templates/starter_app.html")

routes = {
    "/":index,
}

http.start("localhost", 8080, routes)

