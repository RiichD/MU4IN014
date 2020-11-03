from socket import *
from threading import *
from pathlib import Path
import re

#Proxy config
proxyPort = 1235
proxyName = ''
proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
proxySocket.bind((proxyName,proxyPort))
proxySocket.listen(1)
bufferSize = 8192

#Server config
serverName = '127.0.0.1'
serverPort = 1236 #80 pour le serveur Apache
serverFilePath = '/var/www/html' #Emplacement des fichiers du serveur, ici Apache
serverTimeout = 2 #Assure la déconnexion au serveur s'il y a un problème

#Proxy parameters
censorDefaultFile = "CensorDefaultFile.txt" #Fichier par défaut si un fichier interdit est demandé dans une requête GET. Ce fichier doit être créé avant!
censor_ForbiddenFiles = ["admin1.txt", "mod1.txt", "file"] #Nom du fichier interdit

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
		connSocket.sendall(b"HTTP/1.1 400 Bad Request\nServer: Python HTTP Proxy Censor\nConnection: close\r\n\r\nBad Request\n")
	connSocket.close()

def request_to_server(connSocket, req):
	"""
	Fonction envoyant les requêtes que reçoit le proxy au server.
	Le proxy reçoit la réponse du serveur sous plusieurs paquets et les envoie au client.
	req correspond à la requête du client.
	"""
	try:
		#Vérifie que le fichier peut être accédé
		if check_file(req):
			
			#Connexion au serveur
			serverSocket = socket(AF_INET,SOCK_STREAM)
			serverSocket.connect((serverName,serverPort))
			serverSocket.send(req)
			serverSocket.settimeout(serverTimeout)
			
			content = ''.encode('utf-8') #Conserve toutes les données provenant du serveur
			
			#Récupèration des données provenant du serveur
			while True:
				data = serverSocket.recv(bufferSize)
				if not data or len(data)==0:
					break
				content += data
				if len(data) < bufferSize: #Si la longueur de data == bufferSize, alors il y a d'autres données encore à recevoir
					break
			connSocket.sendall(content)
			print("All data sent\n")
			
			#Déconnexion du serveur
			serverSocket.close()
		else:
			try:
				f = open(censorDefaultFile, "r")
				connSocket.sendall(b"HTTP/1.1 403 Forbidden\nServer: Python HTTP Proxy Censor\r\n\r\n" + f.read().encode('utf-8'))
				f.close()
			except Exception as exc:
				print("Couldn't Open Default Censor File\n")
				connSocket.sendall(b"HTTP/1.1 404 Not Found\nServer: Python HTTP Proxy Cache\nConnection: close\r\n\r\nCouldn't Open Default Censor File\n")
	except Exception as exc:
		print("Request to server:", exc, "\n")
		connSocket.sendall(b"HTTP/1.1 503 Service Unavailable\nServer: Python HTTP Proxy Censor\nConnection: close\r\n\r\nService Unavailable\n")

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

def check_file(reqData):
	"""
	Fonction permettant de vérifier si le fichier demandé par le client fait partie de la liste des fichiers interdits.
	La fonction retourne True si le fichier n'est pas interdit, False sinon.
	"""
	isAllowed = True
	try:
		filePath, filename = file_infos(reqData)
		print("Checking file: ", filePath)
		if filename in censor_ForbiddenFiles:
			isAllowed = False
		return isAllowed
	except Exception as exc:
		print("Check file error: ", exc)

print("Proxy is running\n")

while True:
	connectionSocket, address = proxySocket.accept()
	Thread(target=handle_request, args=(connectionSocket,)).start()
