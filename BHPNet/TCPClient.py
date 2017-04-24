import socket

class TCPClient:


    def __init__(self):
        self.target_host = "www.google.com"
        self.target_port = 80


    #Create a socket object
    def createClient(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Connect the client
    def connectClient(self):
        self.client.connect((self.target_host, self.target_port))

    #Send some data
    def sendData(self):
        s = "GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n"
        self.client.send(s.encode())

    #Receive some data
    def receiveData(self):
        self.response = self.client.recv(4096)
        print(self.response)

if __name__ == '__main__':
    t = TCPClient()
    t.createClient()
    t.connectClient()
    t.sendData()
    t.receiveData()