from socket import *
import random

def send_message(message, clientAddress):
	serverSocket.sendto(message.encode('utf-8'), clientAddress)
	return None
	
def send_chance(chance):
	if random.randint(1,100) > chance:
		return 1
	else:
		return 0
	
def handle_message():
	message, clientAddress = serverSocket.recvfrom(2048)
	messageClient = message.decode('utf-8')
	if messageClient[0:4] != 'GET ':
		print('Wrong header, must start with GET')
		if send_chance(50):
			send_message('Wrong header, must start with GET', clientAddress)
	elif messageClient[len(messageClient)-8:len(messageClient)] != r'\r\n\r\n':
		print(r"Wrong header, must end with \r\n\r\n")
		if send_chance(50):
			send_message(r'Wrong header, must end with \r\n\r\n', clientAddress)
	else:
		try:
			print(messageClient[4:len(messageClient)-8])
			files = open(messageClient[4:len(messageClient)-8],'r')
			lines = files.readlines()
			
			filesize = 0
			response = ''
			
			listResponse = []
			cpt = 0
			for line in lines:
				#print(len(line.encode('utf-8'))) #DEBUG
				if cpt+1 == len(lines):
					if filesize + len(line.encode('utf-8')) <= 251:
						response += line
						listResponse.append(response)
					else:
						listResponse.append(response)
						response = line
						listResponse.append(response)
					break
				if filesize + len(line.encode('utf-8')) <= 251:
					filesize += len(line.encode('utf-8'))
					response += line
				else:
					#print(filesize) #DEBUG
					listResponse.append(response)
					filesize = 0
					response = ''
				cpt += 1
			#print(listResponse) #DEBUG
			#print('File size: ', end='')
			#print(filesize)
			if (cpt==0):
				send_message(str(len(listResponse)),clientAddress) #Envoie le nombre de paquet au client
			else:
				send_message(str(len(listResponse)),clientAddress)
			for response in listResponse:
				send_message(response,clientAddress)
			files.close()
		except Exception as exc:
			print('File not existing')
			send_message('File not existing',clientAddress)
		print(messageClient)
	

serverPort = 1234
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))
print('Server ready')
while True:
	handle_message()
