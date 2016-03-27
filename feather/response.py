import datetime
import config
from utils import aes

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
            500:"SOMETHING BROKE",
        }
        self._set_session = None

    def request_data(self):
        headers = self.response_obj
        query = headers.get_path().split("?")
        if len(query) > 1:
            query = [1]
        else:
            query = ""
        cookies = {}
        cookies_header = headers.get_headers().get("Cookie")
        if cookies_header:
            for cookie in cookies_header.split(";"):
                cookie = cookie.strip()
                cookie = cookie.split("=")
                cookies[cookie[0]] = cookie[1]
        
        post_data = {}
        if self.post_data:
            for p in self.post_data.split("&"):
                p = p.strip()
                p = p.split("=")
                post_data[p[0]] = p[1]

        return {        
                "method":headers.get_method(),
                "route":headers.get_path(),
                "form":post_data,
                "query":query,
                "session":cookies
            }

    def set_session(self, key, value):
        self._set_session = "{}={}".format(key, value)#aes.encryptData(config.config['session_secret'], value).encode("base64"))

    def get_session(self, key):
        session = self.request_data()['session'].get(key)
        return session
        # Still working on this
        if session:
            try:
                return aes.decryptData(config.config['session_secret'], session.decode("base64"))
            except Exception, e:
                print e
                return None

    def form_data(self, key):
        data = self.request_data()['form'].get(key)

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

        if self._set_session:
            response['Set-Cookie'] = self._set_session 
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

