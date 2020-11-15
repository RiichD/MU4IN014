# Exercice 6 - Question 1

from requests import *
from socket import *
from json import *
from re import *
from threading import *

serverPort = 1234
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print('Server ready')
def handle_request(connSocket):
	"""
	Fonction qui gère les requêtes des clients.
	"""
	try:
		request = connectionSocket.recv(2048)
		if 'favicon.ico' not in request.decode('utf-8') and request != '' and 'GET' in request.decode('utf-8'):
			print("Request:\n" + request.decode('utf-8'))
			tmp_req = split(' ', request.decode('utf-8'))
			if len(tmp_req) > 1:
				response = operation(tmp_req[1])
				if type(response) is dict:
					response = response_validated(response)
					print('Sending to client...\n' + response)
					connSocket.send(response.encode())
				else:
					response = "HTTP/1.1 400 Bad Request\nServer: PYTHON API WEB\nConnection: close\r\n\r\nBad Request\n"
					print('Request error:\n' + response)
					connSocket.send(response.encode())
			else:
				response = "HTTP/1.1 400 Bad Request\nServer: PYTHON API WEB\nConnection: close\r\n\r\nBad Request\n"
				print('Request error:\n' + response)
				connSocket.send(response.encode())
		connSocket.close()
	except Exception as exc:
		print("Request error\n", exc)

def operation(resp):
	"""
	Fonction qui réalise les opérations.
	"""
	try:
		tmp = split('/', resp)
		if len(tmp) > 3:
			op = tmp[1]
			val1 = tmp[2]
			val2 = tmp[3]
			if not val1.isdigit() and not val2.isdigit():
				return None
			else:
				val1 = int(tmp[2])
				val2 = int(tmp[3])
				if op == 'add':
					data = {'value1':val1,'value2':val2,'operand':op,'result':val1+val2}
					return data
				elif op == 'sub':
					data = {'value1':val1,'value2':val2,'operand':op,'result':val1-val2}
					return data
				elif op == 'mul':
					data = {'value1':val1,'value2':val2,'operand':op,'result':val1*val2}
					return data
				elif op == 'div':
					if val2 == 0:
						return None
					data = {'value1':val1,'value2':val2,'operand':op,'result':val1/val2}
					return data
				elif op == 'mod':
					data = {'value1':val1,'value2':val2,'operand':op,'result':val1%val2}
					return data
		else:
			return None
	except Exception as exc:
		print("Operation failed\n", exc)

def response_validated(resp):
	"""
	Fonction qui valide la réponse en ajoutant une entête réponse HTTP.
	"""
	try:
		header = "HTTP/1.1 200 OK\nServer: PYTHON API WEB\nContent-Type: application/json\r\n\r\n"
		return header + dumps(resp) + '\n'
	except Exception as exc:
		print("Response validation failed\n", exc)

while True:
	connectionSocket, address = serverSocket.accept()
	Thread(target=handle_request, args=(connectionSocket,)).start()
