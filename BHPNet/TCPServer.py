import socket
import threading

class TCPServer:

    def __init__(self):
        self.bind_ip = "0.0.0.0"
        self.bind_port = 9999
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectServer(self):
        self.server.bind((self.bind_ip, self.bind_port))
        self.server.listen(5)
        print("[*] Listening on %s:%d" %(self.bind_ip, self.bind_port))

    #This is our client-handling thread
    def handle_client(self, client_socket):
        #print out what the client sends
        request = client_socket.recv(1024)
        print ("[*] Received %s" %request)

    #send back a packet
    def sendBack(self):
        self.client_socket.send("ACK!")
        self.client_socket.close()

    def ejecutar(self):
        while True:
            self.client, self.addr = self.server.accept()

            print("[*] Accepted connection from: %s:%d" %(self.addr[0], self.addr[1]))

            #spin up our client thread to handle incoming data
            self.client_handler = threading.Thread(target=self.handle_client(), args=self.client)
            self.client_handler.start()

if __name__ == '__main__':
    t = TCPServer()
    t.connectServer()
    t.handle_client(t.server)
    t.sendBack()
    t.ejecutar()