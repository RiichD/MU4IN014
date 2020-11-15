# Exercice 1

from re import *

def handle_mail(mails):
	"""
	Fonction vérifiant si les adresses gmail sont valides.
	mails contient la liste des mails à analyser.
	"""
	mailsAccepted = []
	for m in mails:
		tmpM = search('[^@]+@[gmail.com]+$', m)
		if tmpM:
			mailsAccepted.append(m)
	return mailsAccepted

liste_mails = ['marie.Dupond@gmail.com', 'lucie.Durand@wanadoo.fr',
'Sophie.Parmentier@@gmail.com', 'franck.Dupres.gmail.com',
'pierre.Martin@lip6.fr', 'eric.Deschamps@gmail.com'] 

def last_char_is_a_number(s):
	"""
	Fonction vérifiant si la chaine de caractères s se termine par un chiffre.
	"""
	isNumber = False
	if search('[0-9]$', s):
		isNumber = True
	return isNumber

def check_ipv4(addr):
	"""
	Fonction vérifiant si la chaine de caractères ipv4 dans addr contient des zéros problématiques. Si c'est le cas, les zéros sont retirés.
	"""
	res = addr
	
	regexGroup = '(\d+).(\d+).(\d+).(\d+)'
	rg = match(regexGroup, addr)
	res = (rg.group(1).lstrip('0') + '.'
	+ rg.group(2).lstrip('0') + '.'
	+ rg.group(3).lstrip('0') + '.'
	+ rg.group(4).lstrip('0'))
	
	return res

def date_convert(date):
	"""
	Fonction convertissant la date au format MM-DD-YYYY vers le format DD-MM-YYYY.
	"""
	new_format = sub('(\d{2})-(\d{2})-(\d{4})', r'\2-\1-\3', date)
	
	return new_format

# Question 1
mails_accepted = handle_mail(liste_mails)
print("Liste des mails acceptés :\n", mails_accepted, "\n")

# Question 2
s1 = "Je suis une chaine de caractères qui se termine par un chiffre 1"
print(f"{s1}:\n", last_char_is_a_number(s1), "\n")
s2 = "Je suis une chaine de caractères qui ne se termine pas par un chiffre 2."
print(f"{s2}:\n", last_char_is_a_number(s2), "\n")

# Question 3
ipv4_1 = "216.08.094.196"
ipv4_2 = "216.80.140.196"
print(f"Adresse {ipv4_1}:\n", check_ipv4(ipv4_1), "\n")
print(f"Adresse {ipv4_2}:\n", check_ipv4(ipv4_2), "\n")

# Question 4
date = "11-06-2020"
print(f"Date {date}:\n", date_convert(date))

