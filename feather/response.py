import re
import string
import datetime

class Response:
    def __init__(self, obj, received, post_data, ip):
        self.socket_obj = obj
        self.response_obj = received
        self.ip = ip
        self.post_data = post_data
        self.API_ERROR = {
            200:"OK",
            404:"NOT FOUND",
            403:"UNAUTHORIZED",
            302:"MOVED",
        }

    def request_data(self):
        headers = self.response_obj
        query = headers.get_path().split("?")
        if len(query) > 1:
            query = [1]
        else:
            query = ""

        return {        
                "method":headers.get_method(),
                "route":headers.get_path(),
                "form":self.post_data,
                "query":query
            }

    def form_data(self):
        data = self.request_data()

    def router(self, routes):
        route = self.route()
        if route in routes:
            routes[route](self)
        else:
            self.respond("404 Page Not Found", status_code=404)

    def route(self):
        print "[{}] {} - {}".format(datetime.datetime.now(), self.ip, self.request_data()) 
        return self.request_data()['route']
    
    def respond_template(self, file, status_code=200, headers=None):
        self.respond(open(file).read(), status_code=status_code, headers=headers)

    def respond(self, data, status_code=200, headers=None):
        if status_code in self.API_ERROR:
            message = self.API_ERROR[status_code]
        else:
            message = "OK"
        response = {
            "Server":"Feather/0.0.1",
            "Content-Type":"text/html; charset=UTF-8",
        }

        if headers:
            for header in headers:
                response[header] = headers[header]
        headers = "HTTP/1.1 {} {}\n".format(status_code, message)
        for h in response:
            headers += h +": " +response[h] + "\n"
        headers += "\n"
        headers += data + "\r\n\r\n"
        self.socket_obj.send(headers)
        self.socket_obj.close()

