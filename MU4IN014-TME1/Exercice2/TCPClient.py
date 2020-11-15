from socket import *

serverName = '127.0.0.1'
serverPort = 1234
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
message = input('Message: ').encode('utf-8')
clientSocket.send(message)
modifiedMessage = clientSocket.recv(2048)
print(modifiedMessage.decode('utf-8'))
clientSocket.close()
