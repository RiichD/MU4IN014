from socket import *

serverName = '127.0.0.1'
serverPort = 1234
clientSocket = socket(AF_INET,SOCK_DGRAM)
clientSocket.settimeout(3)
while True:
	message = input('Message: ').encode('utf-8')
	if message.decode('utf-8') == "quit": #Entrer quit pour quitter le client
		break
	clientSocket.sendto(message,(serverName,serverPort))
	modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
	print(modifiedMessage.decode('utf-8'))
		
clientSocket.close()
