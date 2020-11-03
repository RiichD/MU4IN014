from socket import *
from threading import *
from pathlib import Path
import re
from shutil import copyfile

#Proxy config
proxyPort = 1236
proxyName = ''
proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
proxySocket.bind((proxyName,proxyPort))
proxySocket.listen(1)
bufferSize = 8192

#Server config
serverName = '127.0.0.1'
serverPort = 80 #80 pour le serveur Apache
serverFilePath = '/var/www/html' #Emplacement des fichiers du serveur, ici Apache
serverTimeout = 2 #Assure la déconnexion au serveur s'il y a un problème

#Proxy parameters
proxy_cachePath = [] #Contient le chemin du fichier à partir de serverFilePath. Par exemple, /var/www/html/files/response1.txt
proxy_cacheFile = [] #Contient le nom du fichier uniquement
proxy_cacheDir = 'caches/' #Les fichiers sont mis en caches dans ce répertoire

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
		connSocket.sendall(b"HTTP/1.1 400 Bad Request\nServer: Python HTTP Proxy Cache\nConnection: close\r\n\r\nBad Request\n")
	connSocket.close()

def request_to_server(connSocket, req):
	"""
	Fonction envoyant les requêtes que reçoit le proxy au server.
	Le proxy reçoit la réponse du serveur sous plusieurs paquets et les envoie au client.
	req correspond à la requête du client.
	"""
	try:
		if copy_check(connSocket, req): #Vérifie s'il y a besoin de faire une requête au serveur
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
			
			#Copie du fichier attendu dans le cache et déconnexion du serveur
			if "404 Not Found".encode('utf-8') not in content:
				copy_file(connSocket, req, content)
			serverSocket.close()
		else:
			try:
				filePath, filename = file_infos(req)
				print(f"Old request found for {filename}\n")
				f = open(proxy_cacheDir+filename, 'rb')
				connSocket.sendall(f.read())
				f.close()
			except Exception as exc:
				print("Couldn't open file in cache\n")
				connSocket.sendall(b"HTTP/1.1 404 Not Found\nServer: Python HTTP Proxy Cache\nConnection: close\r\n\r\nCouldn't Open File in Cache\n")
	except Exception as exc:
		print("Request to server:", exc, "\n")
		connSocket.sendall(b"HTTP/1.1 503 Service Unavailable\nServer: Python HTTP Proxy Cache\nConnection: close\r\n\r\nService Unavailable\n")

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
	
def copy_check(connSocket, reqData):
	"""
	Fonction vérifiant si le fichier demandé est déjà dans le cache.
	Si le fichier est dans le cache, la fonction retourne False. => Pas besoin de faire une requête au serveur
	Sinon Vrai. => Requête au serveur à envoyer
	"""
	#Récupération du chemin et du nom du fichier
	filePath, filename = file_infos(reqData)
	
	check_OK = False
	
	if filename in proxy_cacheFile and filePath in proxy_cachePath:
		#Vérifie l'entête du fichier trouvé
		if Path(proxy_cacheDir+filename).exists():
			f = open(proxy_cacheDir+filename, "rb")
			if not b'HTTP/1.1 200 OK\r\n' in f.read():
				print(f"{filename} exists but contains errors\n")
				proxy_cachePath.remove(filePath)
				proxy_cacheFile.remove(filename)
				print("Proxy cache Path :\n", proxy_cachePath, "\n")
				print("Proxy cache File :\n", proxy_cacheFile, "\n")
				check_OK = True
	else:
		return True
	return check_OK

def copy_file(connSocket, reqData, data):
	"""
	Fonction qui copie les données envoyées par le serveur dans filename.
	"""
	try:
		#Récupération du chemin et du nom du fichier
		filePath, filename = file_infos(reqData)
		
		#Vérifie si la requête du client correspond à un fichier, et s'il existe
		if filename != "" and filename != "favicon.ico" and not Path(filePath).is_dir():
			print(f"File found! Copying {filename}\n")
			f = open(proxy_cacheDir+filename, "wb")
			f.write(data)
			f.close()
			print(f"Copy of {filename} DONE!\n")
			
			#Sauvegarde du chemin et du nom du fichier dans les caches correspondant
			if filePath not in proxy_cachePath:
				proxy_cachePath.append(filePath)
			if filename not in proxy_cacheFile:
				proxy_cacheFile.append(filename)
			print("Proxy cache Path :\n", proxy_cachePath, "\n")
			print("Proxy cache File :\n", proxy_cacheFile, "\n")
		else:
			print("Copy failed, not a file!\n")
	except Exception as exc:
		print("Copying file failed:", exc)

print("Proxy is running\n")

while True:
	connectionSocket, address = proxySocket.accept()
	Thread(target=handle_request, args=(connectionSocket,)).start()
