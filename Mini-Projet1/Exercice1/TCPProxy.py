from socket import *
from threading import *
import re

#Proxy config
proxyPort = 1234
proxyName = ''
proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
proxySocket.bind((proxyName,proxyPort))
proxySocket.listen(1)
bufferSize = 2048

#Server config
serverName = '127.0.0.1'
serverPort = 80 #80 pour le serveur Apache
serverTimeout = 2 #Assure la déconnexion au serveur s'il y a un problème

def handle_request(connSocket):
	"""
	Fonction qui gère toutes les requêtes que reçoit le proxy.
	connSocket correspond à la connexion sur le socket du client.
	"""
	reqClient = connSocket.recv(bufferSize)
	if not reqClient.decode('utf-8') == '':
		print("Client request:\n", reqClient, "\n")
		request_to_server(connSocket, reqClient)
	else:
		connSocket.sendall(b"HTTP/1.1 400 Bad Request\nServer: Python HTTP Proxy\nConnection: close\r\n\r\nBad Request\n")
	connSocket.close()

def request_to_server(connSocket, req):
	"""
	Fonction envoyant les requêtes que reçoit le proxy au server.
	Le proxy reçoit la réponse du serveur sous plusieurs paquets et les envoie au client.
	req correspond à la requête du client.
	"""
	try:
		#Connexion au serveur
		serverSocket = socket(AF_INET,SOCK_STREAM)
		serverSocket.connect((serverName,serverPort))
		serverSocket.send(req)
		serverSocket.settimeout(serverTimeout)
		
		content = ''.encode('utf-8') #Conserve toutes les données provenant du serveur
		
		#Récupèration des données provenant du serveur
		respLength = 0
		while True:
			data = serverSocket.recv(bufferSize)
			if not data or len(data)==0:
				break
			content += data
			if b"\r\nContent-Length" in data:
				for d in re.split(b"\r\n", data):
					if b"Content-Length" in d:
						respLength += int(d.replace(b"Content-Length: ", b""))
			respLength -= bufferSize
			if respLength <= 0:
				break
		connSocket.sendall(content)
		print("All data sent\n")
		
		#Déconnexion du serveur
		serverSocket.close()
	except Exception as exc:
		print("Request to server:", exc, "\n")
		connSocket.sendall(b"HTTP/1.1 503 Service Unavailable\nServer: Python HTTP Proxy\nConnection: close\r\n\r\nService unavailable\n")

print("Proxy is running\n")

while True:
	connectionSocket, address = proxySocket.accept()
	Thread(target=handle_request, args=(connectionSocket,)).start()
