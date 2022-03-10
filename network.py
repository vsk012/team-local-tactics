import socket
import pickle
import random as random
#from server import rand_num



class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
    
    #rand_num = random.randint(0,99)
        

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)

    def recieve(self):
        try:
            return self.client.recv(2048).decode()
        except:
            pass
    
    def sending(self, data):
        try:
            return self.client.send(str(data)).encode()
        except:
            pass