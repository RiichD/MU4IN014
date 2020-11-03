from socket import *

serverName = '127.0.0.1'
serverPort = 1234	
retry = False
attempt = 0
while True:
	try:	
		clientSocket = socket(AF_INET, SOCK_STREAM)
		
		if attempt == 3:
			print("Maximum attempt reached, disconnecting")
			break
		
		if not retry:
			message = input('Message: ').encode('utf-8')
			
		if message.decode('utf-8') == "quit": #Entrer quit pour quitter le client
			break
			
		clientSocket.connect((serverName,serverPort))
		clientSocket.settimeout(3)
		
		clientSocket.send(message)
		modifiedMessage = clientSocket.recv(2048)
		print(modifiedMessage.decode('utf-8'))
			
		retry = False
		attempt = 0
	except Exception as exc:
		print("timeout")
		retry = True
		attempt += 1
		
clientSocket.close()
		
