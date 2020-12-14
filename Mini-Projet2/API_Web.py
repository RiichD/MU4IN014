from bottle import *
from json import *

from re import *
from lxml import etree as ET

local_input = "dblp_2020_2020.xml"

p = ET.XMLParser(recover=True)
tree = ET.parse(local_input, parser=p)
root = tree.getroot()
print(f"XML File loaded and parsed, root is {root.tag}")

@route("/publications/<id:re:id-[0-9]+>")
def publications(id):
	"""
	On suppose que l'id commence à partir de 1.
	La syntaxe nécessite sur l'URL est de la forme : /publications/id-n, avec n un nombre.
	"""
	id = re.sub("id-", "", id)
	id = int(id)
	res = ""
	nb_pub = 0
	for child in root:
		if nb_pub == id-1:
			for i in range(len(child)):
				res += dumps([child[i].text]) + "<br/>"
			res = res + "<br/>"
			return res
		else:
			nb_pub += 1


@route("/publications/<limit:int>")
def publications(limit):
	res = ""
	nb_pub = 0
	for child in root:
		for i in range(len(child)):
			res += dumps([child[i].text]) + "<br/>"
		res = res + "<br/>"
		nb_pub += 1
		if nb_pub == limit:
			return res

@route("/authors/<name>")
def authors(name):
	nb_pub_author = 0
	nb_pub_coauthor = 0
	for child in root:
		author = False
		if len(child):
			for data in child: #Boucle permettant de vérifier que la donnée n'est pas vide
				if data.text != None and name in data.text:
					if name in child[0].text:
						author = True
					for i in range(len(child)):
						if child[i].text != None:
							if "author" == child[i].tag and name == child[i].text and author:
								print("Auteur: " , child[i].text)
								nb_pub_author += 1
							elif "author" == child[i].tag and name == child[i].text and not author:
								print("Coauteur: ", child[i].text)
								nb_pub_coauthor += 1
	res = str(nb_pub_author + nb_pub_coauthor) + "<br/>" 
	res += "Authors: " + str(nb_pub_author) + "<br/>" 
	res += "Coauthors: " + str(nb_pub_coauthor) + "<br/>" 
	return "Nombre de publications: " + res

@route("/authors/<name>/publications")
def auth_pub(name):
	"""
	Le premier autheur est l'autheur. Le reste des autheurs sont des coautheurs.
	"""
	res = ""
	for child in root:
		if len(child):
			for data in child: #Boucle permettant de vérifier que la donnée n'est pas vide
				if data.text != None and name in data.text:
					if name == child[0].text and 'author' == child[0].tag:
						for i in range(len(child)):
							if "title" == child[i].tag:
								print(child[i].text)
								res = res + dumps([(child[i].tag +" : " +child[i].text)])+ "<br/>"
	return "Titres de l'auteur " + name + ':<br/>' + res

@route("/authors/<name>/coauthors")
def auth_pub(name):
	"""
	Un coautheur se trouve à partir de la 2ème liste des autheurs d'une publication.
	"""
	res = ""
	list_coauthor = [] #Evite d'avoir des répétitions
	for child in root:
		if len(child):
			for data in child: #Boucle permettant de vérifier que la donnée n'est pas vide
				if data.text != None and name in data.text:
					for i in range(len(child)):
						if name == child[0].text and name != child[i].text and "author" == child[i].tag and child[i].text not in list_coauthor:
							print(child[i].text)
							list_coauthor.append(child[i].text)
							res = res + dumps([(child[i].tag +" : " +child[i].text)])+ "<br/>"
	return f"Coautheurs de {name}: " + "<br/>" + res

@route("/search/authors/<searchString>")
def search_aut(searchString):
	"""
	"""
	res = ""
	list_author = [] #Evite d'avoir des répétitions
	for child in root:
		if len(child):
			for data in child: #Boucle permettant de vérifier que la donnée n'est pas vide
				if data.text != None and searchString in data.text:
					for i in range(len(child)):
						if "author" == child[i].tag and child[i].text != None and (searchString in child[i].text or searchString.upper() in child[i].text) and child[i].text not in list_author:
							print(child[i].text)
							list_author.append(child[i].text)
							res = res + dumps([(child[i].tag +" : " +child[i].text)])+ "<br/>"
	return f"Liste des auteurs contenant {searchString}: " + "<br/>" + res

@route("/search/publications/<searchString>")
def search_pub(searchString):
	"""
	"""
	res = "" #Retourne les publications
	param = request.query.get("filter") #Recherche des paramètres disponibles s'il y en a
	existsParam = False #Indique la présence de paramètre
	options = [] #Contient tout les paramètres
	if param is None: #Vérifie s'il y a un argument
		print("no arg")
	else:
		existsParam = True
	
	if existsParam:
		for f in param.split(','):
			print(f.split(':'))
			options.append(f.split(':'))
	for child in root:
		if len(child):
			for data in child: #Boucle permettant de vérifier que la donnée n'est pas vide
				if data.text != None and searchString in data.text:
					found = False #Indique si la chaine de caractères et les options ont été trouvées.
					for i in range(len(child)):
						if "title" == child[i].tag and searchString in child[i].text:
							found = True
							break
					if found:
						tmp = "" #Stocke les informations temporairement
						for op in options:
							found = False #Un titre contenant searchString est trouvé, on réinitialise found pour trouver les options.
							for i in range(len(child)):
								if op[0] == child[i].tag and child[i].text != None and op[1] in child[i].text:
									print(child[i].text)
									#res = res + dumps([(child[i].tag +" : " +child[i].text)])+ "<br/>"
									tmp = tmp + dumps([(child[i].tag +" : " +child[i].text)])+ "<br/>"
									found = True
									break
							if not found: #Si l'option n'a pas été trouvée, alors on quitte la boucle puisque ce n'est pas la bonne publication
								break
						if found:
							print("Publication trouvée!")
							res += tmp
							res += "<br/>"
	return f"Liste des publications contenant {searchString}: " + "<br/>" + res

@route("/error/<msg>")
def error(msg):
	abort(401, msg)


run(host='localhost', port=8080)

