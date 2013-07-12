from feather import Feather

class WebServer:
    def __init__(self):
        routes = {"/":self.index}
        feather = Feather(routes)
        self.feather = feather
        feather.run("", 5000)
    
    def index(self, request):
        if request['request'] == "GET":
            self.feather.respond("template/index.html", request)
        if request['request'] == "POST":
            self.feather.html("<b>YAY</b>", request)
        print request['post_data']
WebServer()
