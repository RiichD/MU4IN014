from socket import *
from threading import *
from pathlib import Path
import re
from datetime import datetime

#Proxy config
proxyPort = 1234
proxyName = ''
proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
proxySocket.bind((proxyName,proxyPort))
proxySocket.listen(1)
bufferSize = 8192

#Server config
serverName = '127.0.0.1'
serverPort = 1235 #80 pour le serveur Apache
serverFilePath = '/var/www/html' #Emplacement des fichiers du serveur, ici Apache
serverTimeout = 2 #Assure la déconnexion au serveur s'il y a un problème

#Proxy parameters
loggerName = "Logger.txt"
loggerDelimiter = '\n\t\t\n'

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
		connSocket.sendall(b"HTTP/1.1 400 Bad Request\nServer: Python HTTP Proxy Logger\nConnection: close\r\n\r\nBad Request\n")
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

		#Ajout de la réponse du serveur dans le Logger et déconnexion du serveur
		logger_file(req, content)
		serverSocket.close()
	except Exception as exc:
		print("Request to server:", exc, "\n")
		connSocket.sendall(b"HTTP/1.1 503 Service Unavailable\nServer: Python HTTP Proxy Logger\nConnection: close\r\n\r\nService Unavailable\n")

def file_infos(reqData):
	"""
	Fonction retournant le chemin ET le nom (filePath, filename) du fichier à partir de la requête du client.
	filePath : le chemin
	filename : le nom
	"""
	
	#Recherche du chemin et du nom
	filePath = ""
	filename = ""
	
	filePath = serverFilePath+re.split(r' ', str(reqData))[1]
	#print("filePath: ", filePath) #DEBUG
	
	listPath = re.split(r'[\\/]', filePath)
	filename = listPath[len(listPath)-1]
	#print("filename: ", filename) #DEBUG
	return filePath, filename

def logger_file(reqData, respData):
	"""
	Fonction permettant d'ajouter les requêtes et réponses dans le fichier logger
	Si boolean_size vaut True, on récupère la taille du fichier. Sinon, on ne fait rien
	p correspond au chemin du fichier
	"""
	try:
		#Ajoute la requête du client dans le fichier de log ainsi que la date et l'heure
		if reqData != b'':
			#Récupère les informations sur le fichier en question
			filePath, filename = file_infos(reqData)

			data = "TIME: "+str(datetime.now())+'\n'
			data += str(reqData) + loggerDelimiter
		
		#Ajoute la réponse du serveur dans le fichier de log ainsi que la taille du fichier si isFile est vrai
		if respData != b'':
			dataSplitted = re.split(b"\r\n\r\n", respData)[0]
			if b"\r\nContent-Length" in dataSplitted:
				for content in re.split(b"\r\n", dataSplitted):
					if b"Content-Length" in content:
						size = content.replace(b"Content-Length: ", b"").decode('utf-8')
						data += "SIZE: "+str(size)+'\n'
			data += str(re.split(b"\r\n\r\n",respData)[0]) + loggerDelimiter
		
		#Ecriture dans le fichier de log
		if reqData != b'' and respData != b'':
			f = open(loggerName, 'a+')
			f.write(str(data))
			f.close()
	except Exception as exc:
		print("Logger error:", exc)


print("Proxy is running\n")

while True:
	connectionSocket, address = proxySocket.accept()
	Thread(target=handle_request, args=(connectionSocket,)).start()
