import socket, threading
import sys

class Feather:
    def __init__(self):
        self.requests = {'GET':self.get, "POST": self.post}
        self.files_dir = "templates"
        if sys.argv[2]:
            if sys.argv[2] == "debug":
                self.debug = True
    def main_loop(self, port):
        print "Feather has started on port "+str(sys.argv[1])
        while True:
            self.port = int(sys.argv[1])
            sock = socket.socket()
            sock.bind(('', self.port))
            sock.listen(1)
            while True:
                try:
                    obj, conn = sock.accept()
                except KeyboardInterrupt:
                    sock.close()
                    exit()
                data = obj.recv(1024).split()
                if self.debug:
                    print data
                else:
                    print conn[0], data[0], data[1]
                for request in self.requests:
                    if data[0] == request:
                        threading.Thread(self.requests[request](data, obj)).start()
    def get(self, data, obj):
        if data[1] == "/":
            data[1] = 'index.html'
        else:
            data[1] = data[1].replace("/", '')
        try:
            with open(self.files_dir+"/"+data[1], 'rb') as file:
                obj.send("""HTTP/1.1 200 OK
            Server: Feather HTTP v0.01

            """+file.read()+"\r\n\r\n")
                obj.close()
        except:
            print "No such file "+data[1]

    def post(self, data, obj):
        print data[29]
        self.get(data, obj)
if __name__ == "__main__":
    Feather().main_loop(5000)
