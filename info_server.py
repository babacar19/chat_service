import threading

class server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = None

    def run(self):
        pass
