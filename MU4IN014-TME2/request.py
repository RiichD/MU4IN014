# Exercice 6 - Question 2

from requests import *

ip_adress = "http://127.0.0.1:1234/"

def test():
	"""
	Fonction permettant de tester la requête à l'API Web.
	"""
	link = "http://127.0.0.1:1234/sub/4/20"

	r = get(link)
	print(f"Request status is {r.status_code},\n"
	 f"Content length is {len(r.content)} bytes,\n"
	 f"Text size is {len(r.text)} chars.")
	print(f"Response headers: {r.headers}")
	print(f"{r.text}")

def user_request():
	"""
	Fonction qui permet à l'utilisateur d'entrer l'opération et les valeurs à réaliser.
	"""
	op = ''
	val1 = ''
	val2 = ''
	while True:
		op = input("Enter operand:\n")
		if op == 'exit':
			break
		val1 = input("Enter value1:\n")
		if val1 == 'exit':
			break
		val2 = input("Enter value2:\n")
		if val2 == 'exit':
			break
		print(f'You entered :\nOperand: {op}, value 1: {val1}, value 2: {val2}')
		link = ip_adress+op+'/'+val1+'/'+val2
		r = get(link)
		print(f"Request status is {r.status_code},\n"
		 f"Content length is {len(r.content)} bytes,\n"
		 f"Text size is {len(r.text)} chars.")
		print(f"Response headers: {r.headers}")
		print(f"{r.text}")
#test()
user_request()

