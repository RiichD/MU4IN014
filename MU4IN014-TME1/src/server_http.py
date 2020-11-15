from socket import *
from pathlib import *

serverPort = 1234
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print('server ready')

def handle_client(cs):
   	received = cs.recv(4096)
   	filename = Path(received.decode('utf-8').split("\n",1)[0].split(" ")[1].lstrip("/"))
   	print(f"{filename} was requested...")

   	if not filename.is_file():
   		print("... and not found!")
   		cs.send(b"HTTP/1.1 404 Not Found\nServer: Python HTTP Server\nConnection: close\r\n\r\n")
   	else:
   		print("... and sent!")
   		cs.send(b"HTTP/1.1 200 OK\nServer: Python HTTP Server\nConnection: close\r\n\r\n")
   		with open(filename,"br") as f:
   			cs.send(f.read())
   	cs.close()

while True:
	connectionSocket, address = serverSocket.accept()
	handle_client(connectionSocket)
