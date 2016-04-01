import datetime
import config
from utils import aes
import json
import re

class Response:
    def __init__(self, obj, received, post_data, ip):
        self.socket_obj = obj
        self.response_obj = received
        self.ip = ip
        self.post_data = post_data
        self.HTTP_ERROR = {100: 'Continue',
         101: 'Switching',
         102: 'Processing',
         200: 'OK',
         201: 'Created',
         202: 'Accepted',
         203: 'Non-Authoritative',
         204: 'No',
         205: 'Reset',
         206: 'Partial',
         207: 'Multi-Status',
         208: 'Already',
         226: 'IM',
         300: 'Multiple',
         301: 'Moved',
         302: 'Found',
         303: 'See',
         304: 'Not',
         305: 'Use',
         306: 'Reserved',
         307: 'Temporary',
         308: 'Permanent',
         400: 'Bad',
         401: 'Unauthorized',
         402: 'Payment',
         403: 'Forbidden',
         404: 'Not',
         405: 'Method',
         406: 'Not',
         407: 'Proxy',
         408: 'Request',
         409: 'Conflict',
         410: 'Gone',
         411: 'Length',
         412: 'Precondition',
         413: 'Request',
         414: 'Request-URI',
         415: 'Unsupported',
         416: 'Requested',
         417: 'Expectation',
         422: 'Unprocessable',
         423: 'Locked',
         424: 'Failed',
         425: 'Reserved',
         426: 'Upgrade',
         427: 'Unassigned',
         428: 'Precondition',
         429: 'Too',
         430: 'Unassigned',
         431: 'Request',
         500: 'Internal',
         501: 'Not',
         502: 'Bad',
         503: 'Service',
         504: 'Gateway',
         505: 'HTTP',
         506: 'Variant',
         507: 'Insufficient',
         508: 'Loop',
         509: 'Unassigned',
         510: 'Not',
         511: 'Network'}

        self._set_session = []

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
                "session":self.parse_cookies(cookies),
                "params":{},
            }

    def set_session(self, key, value):
        self._set_session.append("{}={}".format(key, aes.encryptData(config.config['session_secret'], value).encode("base64").replace("=", "|").replace("\n",'')))

    def parse_cookies(self, cookies):
        """
            Checks for sessions created by Feather and decrypts them with the session_secret.
        """
        session_secret = config.config['session_secret']
        out_cookies = {}
        for c in cookies:
            if "|" in cookies[c]:
                cookies[c] = cookies[c].replace("|", "=")
                try:
                    out_cookies[c] = aes.decryptData(session_secret, cookies[c].decode("base64"))
                except: # This happens if the session cookies was not created by Feather.
                    pass
        return out_cookies

    def respond_json(self, dictionary, status_code=200, headers=None):
        try:
            return self.respond(json.dumps(dictionary), status_code=status_code, headers={"Content-Type":"text/plain"})
        except:
            return self.respond("500 Internal Error", status_code=500)


    def redirect(self, location):
        try:
            return self.respond("", status_code=302, headers={"Location":location})
        except:
            return self.respond("500 Internal Error", status_code=500)

    def router(self, routes):
        route = self.route()
        req = self.request_data()
        isOkay = False
        if route in routes:
            isOkay = True
        elif route.startswith("/static"):
            self.respond_template("static/{}".format(route.replace("/static/", '')))
            return
        else:
            for r in routes: # Parses URL for variables
                if "<" in r:
                    r_s = r.split("/")
                    rou_s = route.split("/")
                    if len(r_s) == len(rou_s):
                        match = True
                        while len(r_s) > 0:
                            r_set, r_req =  r_s.pop(0), rou_s.pop(0)
                            if r_set == r_req or "<" in r_set:
                                continue
                            match = False
                            break
                        if match:
                            params = {}
                            r_s = r.split("/")
                            rou_s = route.split("/")
                            while len(r_s) > 0:
                                r_set, r_req = r_s.pop(0), rou_s.pop(0)
                                if "<" in r_set:
                                    variable = re.findall("<([a-zA-Z0-9]+)>", r_set)
                                    params[variable[0]] = r_req
                            req['params'] = params
                            isOkay = True
                            route = r
                            break
        if isOkay:
            if type(routes[route]) == dict:
                if req.get("method") in routes[route]:
                    routes[route][req.get("method")](req, self)
                else:
                    self.respond("403 Method Not Allowed", status_code=403)
            else:
                routes[route](req, self)
        else:
            self.respond("404 Page Not Found", status_code=404)

    def route(self):
        print "[{}] {} - {} {}".format(datetime.datetime.now(), self.ip, self.request_data()['route'], self.request_data()['method']) 
        return self.request_data()['route']
    
    def respond_template(self, file, status_code=200, headers=None):
        try:
            self.respond(open(file).read(), status_code=status_code, headers=headers)
        except:
            self.respond("500 Internal Error", status_code=500)

    def respond(self, data, status_code=200, headers=None):
        if status_code in self.HTTP_ERROR:
            message = self.HTTP_ERROR[status_code]
        else:
            message = "OK"
        response = {
            "Server":"Feather/0.0.1",
            "Content-Type":"text/html; charset=UTF-8",
        }

        if self._set_session:
            response['Set-Cookie'] = '&'.join(self._set_session)
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

