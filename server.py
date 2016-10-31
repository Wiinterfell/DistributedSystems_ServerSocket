import socket
from  multiprocessing import Process
import sys
from urlparse import urlparse, parse_qs

def EchoClientThread(client_socket, address) :
        while 1:
                client_data = client_socket.recv(4096)
                
                request = parse_qs(urlparse(client_data).query)

                if ("message" in request):
                        message = (request["message"])[0]
                        message = message.upper().rstrip()
                        client_socket.send(message)
                else:
                        client_socket.close()
                        return


#main part
print "*** Creating server socket"
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print "*** Binding to port"
server_socket.bind(("0.0.0.0", int(sys.argv[1])))

server_socket.listen(10)
print "*** Listening"

processes = []

while 1:
        print "*** Waiting for client connections"

        print "*** Starting a new thread for client"
        client_socket, address = server_socket.accept()
        process = Process(target=EchoClientThread, args= (client_socket, address))

        process.start()
        processes.append(process)