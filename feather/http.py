import socket
import response
from http_parser.parser import HttpParser

def http(host, port):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    while True:
        obj, conn = sock.accept()
        body = []
        p = HttpParser()
        while True:
            data = obj.recv(1024)
            if not data:
                break

            recved = len(data)
            nparsed = p.execute(data, recved)
            assert nparsed == recved

            if p.is_partial_body():
                body.append(p.recv_body())

            if p.is_message_complete():
                break

        yield response.Response(obj, p, ''.join(body), conn[0])
