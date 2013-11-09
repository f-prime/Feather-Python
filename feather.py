import socket
import uuid
import thread
import urlparse
import time

class Feather:
    def __init__(self, routes):
        self.header = "HTTP/1.0 {0} {1}\n\r\r\nServer: Feather \r\nContent-type: text/html\r\n Set-Cookie: name=value\r\nSet-Cookie: FUUUCKKK=value2; \r\n\r\n"""
        self.routes = routes

    def run(self, host="127.0.0.1", port=7070):
        print "Feather has started on http://"+host+":"+str(port)
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(5)
        while True:
            obj, conn = self.sock.accept()
            thread.start_new_thread(self._handle, (obj, conn[0]))

    def _handle(self, obj, conn):
        self.obj = obj
        data_ = obj.recv(1024)
        if data_:
            print data_
            data = self._parse(data_)
            if data['url'] not in self.routes:
                self.abort(404)
            self.routes[data['url']]()
        
        print conn + " "+ data['url'] +" "+ data['type'] +" "+str(data) 
        obj.close()

    def abort(self, code):
        page = """

            Page not found.


        """

        header = self.header.format(str(code), "NOT FOUND")
        self._send(header+page)
   
    def requestdata(self):

        return self.out


    def html(self, html):

        header = self.header.format("200", "OK")
        self._send(header+html)

    def _send(self, code):
        self.obj.send(code)

    def _parse(self, data):
        data = data.split("\r\n")
        out = {}
        first = data[0].split()
        out['type'] = first[0]
        if first[0] == "POST":
            post_data = data[len(data)-1].split("&")
            post_d = {}
            for x in post_data:
                x = x.split("=")
                post_d[x[0]] = x[1]
            out['post_data'] = post_d

        out['url'] = urlparse.urlparse(first[1])[2]
        out['version'] = first[2]
        on = 0
        while not data[on].startswith("User-Agent:"):
            on += 1

        agent = data[on].split()
        out['useragent'] = ' '.join(agent[1:])
        try:
            while not data[on].startswith("Cookie:"):
                on += 1

            cookie = data[on].split()
            out['cookie'] = ' '.join(cookie[1:])
        except IndexError:
            pass
        self.out = out
        return out
            



