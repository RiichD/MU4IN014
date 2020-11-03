from socket import *

serverPort = 1234
serverSocket = socket(AF_INET,SOCK_DGRAM)

serverSocket.bind(('',serverPort))

print('server ready')

while True:
    _, clientAddress = serverSocket.recvfrom(2048)
    serverSocket.sendto(b'PONG',clientAddress)