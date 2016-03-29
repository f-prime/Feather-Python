import socket
import response
from http_parser.parser import HttpParser
import thread

def start(routes, host="127.0.0.1", port=5050, threads=5):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    for t in range(threads):
        print "Number {} thread started".format(t) 
        thread.start_new_thread(thread_func, (sock,routes))
    print "Feather Server Started at http://{}:{}".format(host, port)
    while True:pass # This keeps the threads alive

def thread_func(sock, routes):
    for request in http(sock):
        request.router(routes)


def http(sock):
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
