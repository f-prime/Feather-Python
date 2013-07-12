from feather import Feather

class WebServer:
    def __init__(self):
        routes = {"/":self.index, "/login/":self.login,}
        feather = Feather(routes)
        self.feather = feather
        feather.run("", 5001)
    
    def index(self, request):
        if request['ip'] not in self.feather.session():
            self.feather.html("<script>window.location='/login/';</script>", request)
        elif request['request'] == "GET":
            self.feather.html("<h1>Hey "+self.feather.session()[request['ip']]+"</h1>", request)

    def login(self, request):
        if request['request'] == "GET":
            self.feather.html("<form method='post'><input type='text' name='name' value='Name'><input type='submit' name='submit'></form>", request)
        if request['request'] == "POST":
            username = request['post_data']['name']
            self.feather.session_start(username, request)
            self.feather.html("<script>window.location='/';</script>", request)
WebServer()
