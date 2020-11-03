from socket import *

serverName = '127.0.0.1'
serverPort = 1234
clientSocket = socket(AF_INET,SOCK_DGRAM)
clientSocket.settimeout(3)
retry = False #Booleen indiquant s'il faut renvoyer le message au serveur si le client ne recoit pas de reponse
while True:
	try:
		if not retry:
			message = input('Message: ').encode('utf-8')
		if message.decode('utf-8') == "quit": #Entrer quit pour quitter le client
			break
		clientSocket.sendto(message,(serverName,serverPort))
		try:	
			modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
			number_packet = int(modifiedMessage) #Récupère le nombre de paquets
			print(modifiedMessage.decode('utf-8'))
			while number_packet > 0:
				print('New packet: ')
				packet, serverAddress = clientSocket.recvfrom(2048)
				print(packet.decode('utf-8')) #Affiche les paquets
				number_packet -=1
		except Exception as exc:
			print(modifiedMessage.decode('utf-8'))
		retry = False
	except Exception as exc:
		print("timeout")
		retry = True
		
clientSocket.close()
