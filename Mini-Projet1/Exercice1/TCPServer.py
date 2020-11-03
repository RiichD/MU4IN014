from socket import *
from threading import *

serverPort = 5678
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

def handle_request(connectionSocket):
	"""
	Fonction gérant toutes les requêtes que reçoit le serveur provenant du proxy.
	La réponse à la requête est envoyée au proxy.
	"""
	messageClient = connectionSocket.recv(2048)
	message = messageClient.decode('utf-8')
	if message[0:4] != 'GET ':
		print("HTTP/1.1 400 Bad Request\nServer: Python HTTP Server\nConnection: close\r\n\r\nBad request\n")
		connectionSocket.send("HTTP/1.1 400 Bad Request\nServer: Python HTTP Server\nConnection: close\r\n\r\nBad request\n".encode('utf-8'))
	else:
		messageSplitted = message.split(' ')
		if len(messageSplitted) < 3:
			connectionSocket.send("HTTP/1.1 400 Bad Request\nServer: Python HTTP Server\nConnection: close\r\n\r\nBad request\n".encode('utf-8'))
		elif messageSplitted[2][0:4] != "HTTP":
			#print(messageSplitted[2][0:4]) #DEBUG
			connectionSocket.send("HTTP/1.1 400 Bad Request\nServer: Python HTTP Server\nConnection: close\r\n\r\nBad request\n".encode('utf-8'))
		else:
			#print(messageSplitted) #DEBUG
			try:
				files = open(messageSplitted[1][1:], 'rb')
				response = files.read()
				connectionSocket.sendall(response)
				print('\n'+response.decode("utf-8")+'\n')
				files.close()
			except Exception as exc:
				response = "HTTP/1.1 404 Not Found\nServer: Python HTTP Server\nConnection: close\r\n\r\nFile not found\n"
				connectionSocket.send(response.encode('utf-8'))
				print('\n'+response+exc+'\n')
			finally:
				connectionSocket.close()
	return None

print('Server running')

while True:
	connectionSocket, address = serverSocket.accept()
	Thread(target=handle_request, args=(connectionSocket,)).start()
