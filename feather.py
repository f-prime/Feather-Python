import socket
import threading


class Feather:
    global sessions
    sessions = {}
    def __init__(self, routes):
        self.response_header = "HTTP/1.0 200 OK\r\nServer: Feather HTTP\r\nContent-type: text/html\r\n\r\n"
        self.routes = routes

    def run(self, host, port):
        print "Feather has started on port", str(port)
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(5)
        while True:
            obj,conn = self.sock.accept()
            ip = conn[0]
            threading.Thread(target=self.handle, args=(obj, ip)).start()

    def handle(self, obj, ip):
        request = obj.recv(1024)
        if request:
            request = request.split("\r\n")
            req_type = request[0].split()
            print ip, request[0]

            if req_type[0] == "GET":
                page = req_type[1]
                if page in self.routes:
                    
                    self.routes[page]({"request":"GET", "page":page, "ip":ip, "obj":obj})
                else:
                    obj.send(self.response_header+"Page does not exist."+"\r\n")
            
            if req_type[0] == "POST":
                page = req_type[1]
                if page in self.routes:
                    post_data = request[len(request)-1]
                    if "&" not in post_data:
                        post_data = post_data+"&"
                    post_data = post_data.split("&")
                    return_data = {}
                    for x in post_data:
                        x = x.split("=")
                        return_data[x[0]] = x[1]
                    self.routes[page]({"request":"POST", "ip":ip, "page":page, "obj":obj, "post_data":return_data})
            obj.close()
        else:
            obj.close()

    def respond(self, page, request):
        with open(page, 'rb') as file:
            request['obj'].send(self.response_header+file.read()+"\r\n")

    def html(self, html, request):
        request['obj'].send(self.response_header+"\n"+html+"\r\n")

    def session_start(self, name, request):
        sessions[request['ip']] = name

    def session_stop(self, name, request):
        del sessions[request['ip']]

    def session_check(self, request):
        ip = request['ip']
        if ip in sessions:
            return True
        else:
            return False
    
    def session(self):
        return sessions

