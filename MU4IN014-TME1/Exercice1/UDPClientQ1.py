from socket import *

serverName = '127.0.0.1'
serverPort = 1234
clientSocket = socket(AF_INET,SOCK_DGRAM)
message = input('Message to send: ').encode('utf-8')
clientSocket.sendto(message,(serverName,serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode('utf-8'))
clientSocket.close()
