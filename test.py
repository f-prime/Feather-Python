from feather import Feather

class WebServer:
    def __init__(self):
        routes = {"/":self.index}
        feather = Feather(routes)
        self.feather = feather
        feather.run("", 5000)
    
    def index(self, request):
        if request['id'] in self.feather.session:
            self.feather.html("<b>"+self.feather.session[request['id']], request)
        
        #if self.feather.session_check(request['id']):
            #self.feather.html(self.feather.session[request['id']])
        if request['request'] == "GET":
            self.feather.respond("template/index.html", request)
        elif request['request'] == "POST":
            self.feather.html("<b>YAY</b>", request)
            username = request['post_data']['username']
            self.feather.session_start(username, request)
            redir = """<script>window.location="{0}";""".format("/")
            self.feather.html(redir, request)

WebServer()
