import socket
from  multiprocessing import Process
import sys, os, signal
from urlparse import urlparse, parse_qs
import Queue
import thread

def EchoClientThread(queue) :
	while 1:	

		#print queue.qsize()	
		if(queue.qsize() == 0):
			continue

		client_socket = queue.get()

		client_data = client_socket.recv(4096)
        
		request = parse_qs(urlparse(client_data).query)
		
		if ("message" in request):
			message = (request["message"])[0]

			if (message == "KILL_SERVICE\n\n"):
				client_socket.send("Server killed")
				os.kill(os.getpid(), signal.SIGINT)
			else:
				message = message.upper().rstrip()
				client_socket.send(message)
		else:
			client_socket.close()
			return


if __name__ == "__main__":
	print "*** Creating server socket"
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	print "*** Binding to port"
	server_socket.bind(("0.0.0.0", int(sys.argv[1])))

	server_socket.listen(100)
	print "*** Listening"

	maxThreads = int(sys.argv[2]);
	queue = Queue.Queue()

	for i in range(0, maxThreads):
		t = thread.start_new_thread(EchoClientThread, (queue,))

	while 1:
	    print "*** Waiting for client connections"

	    print "*** Adding a new client to the queue"
	    client_socket, address = server_socket.accept()
	    queue.put(client_socket)