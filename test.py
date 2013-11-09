from feather import Feather

class Site:
    def __init__(self):
        self.routes = {'/':self.index}
        self.feath = Feather(self.routes)
        self.feath.run()

    def index(self):
        
            self.feath.html("asd")


Site()
