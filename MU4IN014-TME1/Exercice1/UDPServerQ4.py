from socket import *
import random

serverPort = 1234
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))
print('Server ready')
while True:
	message, clientAddress = serverSocket.recvfrom(2048)
	modifiedMessage = message.decode('utf-8').upper()	
	if random.randint(1,100) > 50:
		serverSocket.sendto(modifiedMessage.encode('utf-8'),clientAddress)
	print(modifiedMessage)
