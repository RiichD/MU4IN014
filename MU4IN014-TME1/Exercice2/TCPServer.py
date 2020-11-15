from socket import *

serverPort = 1234
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('Server ready')
while True:
	connectionSocket, address = serverSocket.accept()
	messageClient = connectionSocket.recv(2048)
	message = messageClient.decode('utf-8')
	if message[0:4] != 'GET ':
		print('400 Bad Request\n')
		connectionSocket.send('HTTP 400 Bad Request'.encode('utf-8'))
	else:
		messageSplitted = message.split(' ')
		if len(messageSplitted) < 3:
			connectionSocket.send('HTTP 400 Bad Request'.encode('utf-8'))
			continue;
		else:
			print(messageSplitted) #DEBUG
			try:
				files = open(messageSplitted[1][1:], 'r')
				lines = files.readlines()
				response = messageSplitted[2][0:8] + ' 200 OK\n'
				for line in lines:
					response = response + line
				connectionSocket.send(response.encode('utf-8'))
				print('\n'+response+'\n')
				files.close()
			except Exception as exc:
				response = messageSplitted[2][0:8] + ' 404 Not Found\n'
				connectionSocket.send(response.encode('utf-8'))
				print('\n'+response+'\n')
			finally:
				connectionSocket.close()
