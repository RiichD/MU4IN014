from bottle import *
from json import *

from re import *
from lxml import etree as ET

local_input = "dblp_2020_2020.xml"

p = ET.XMLParser(recover=True)
tree = ET.parse(local_input, parser=p)
root = tree.getroot()
print(f"XML File loaded and parsed, root is {root.tag}")

#Variables globales
PUB_LIMIT = 100 #Le nombre de publications qu'on veut obtenir pour "/publications"


@route("/publications/<id:int>")
def publications(id):
	"""
	La fonction permet d'obtenir la publication correspondante avec l'id.
	On suppose que l'id commence à partir de 1.
	Elle retourne une chaîne de caractère contenant les informations.
	"""
	res = ""
	nb_pub = 0
	if id <= 0:
		redirect("/error/403/" + f"{id} is not between 1 or more and the id must be an integer, try again.")
	for child in root:
		if nb_pub == id-1:
			for i in range(len(child)):
				res += child[i].tag + " : " + child[i].text
				if i < len(child)-1:
					res += '<br/>' #Newline
			return dumps([res])
		else:
			nb_pub += 1
	redirect("/error/404/"+"Page not found") #Erreur s'il n'y a aucune publication

@route("/publications")
def publications():
	"""
	La fonction permet d'obtenir les publications les limit premières publications.
	Un paramètre limit peut être utilisé pour modifier cette limite sur l'URL. 
	Sinon, il est aussi possible de modifier via la variable globale PUB_LIMIT.
	La fonction retourne une liste des publications.
	"""
	res = [] #Les informations récoltées sont stockées dans cette liste
	limit = PUB_LIMIT
	param = request.query.get("limit") #Recherche des paramètres disponibles s'il y en a
	if param is not None: #Vérifie s'il y a un argument
		try:
			limit = int(param)
		except ValueError as exc:
			redirect("/error/403/" + f"{param} is not a number, try again.")
	for child in root:
		tmp = "" #Stocke les informations temporairement
		isNull = True
		for i in range(len(child)):
			if child[i].text != None:
				tmp += child[i].tag + " : " + child[i].text
				if i < len(child)-1:
					tmp += '<br/>' #Newline
				isNull = False
		if not isNull:
			res.append(dumps([tmp]) + '<br/>''<br/>') #Formatage
		if len(res) == limit:
			return res
	redirect("/error/404/"+"Page not found")

@route("/authors/<name>")
def authors(name):
	"""
	La fonction retourne le nombre de fois que name a publié en tant que coauteur et le nombre de coauteurs.
	"""
	res = [] #Liste des coauteurs
	estCoauteur = 0 #Le nombre de fois que l'auteur est un coauteur
	try:
		for child in root:
			if len(child):
				for data in child: #Boucle permettant de vérifier que la donnée n'est pas vide
					if data.text != None and name in data.text:
						isCoauteur = False
						for i in range(len(child)): #Compte le nombre d'auteurs
							if child[i].text != None:
								author = dumps([(child[i].tag + " : " +child[i].text)])+ "<br/>"
								if "author" == child[i].tag and name != child[i].text and author not in res:
									print(author)
									res.append(author)
									isCoauteur = True
						if isCoauteur: #S'il y a plus d'un auteur hormis l'auteur lui même, alors c'est un coauteur
							estCoauteur += 1
	except Exception as exc: #Capture les erreurs inattendues
		print("An error occurred: ", exc)
		redirect("/error/403/" + f"An error occurred: " + str(exc))
	return f"{estCoauteur} publications dont il est coauteur avec {len(res)} coauteurs."+'<br/>'
	
@route("/authors/<name>/publications")
def auth_pub(name):
	"""
	La fonction retourne la liste les publications de name.
	"""
	res = []
	try:
		for child in root:
			if len(child):
				for data in child: #Boucle permettant de vérifier que la donnée n'est pas vide
					if data.text != None and name in data.text:
						if 'author' == child[0].tag:
							for i in range(len(child)):
								if "title" == child[i].tag:
									print(child[i].text)
									res.append(dumps([(child[i].tag + " : " +child[i].text)]) + "<br/>")
	except Exception as exc: #Capture les erreurs inattendues
		print("An error occurred: ", exc)
		redirect("/error/403/" + f"An error occurred: " + str(exc))
	res.insert(0, f"Les titres de l'auteur {name}:" + '<br/>')
	return res

@route("/authors/<name>/coauthors")
def auth_pub(name):
	"""
	La fonction retourne tout les coauteurs de name.
	"""
	res = [f"Les coauteurs de {name} sont les suivants:" + "<br/>"]
	try:
		for child in root:
			if len(child):
				for data in child: #Boucle permettant de vérifier que la donnée n'est pas vide
					if data.text != None and name in data.text:
						coauthor = ""
						for i in range(len(child)):
							coauthor = dumps([(child[i].tag + " : " +child[i].text)])+ "<br/>"
							if name != child[i].text and "author" == child[i].tag and coauthor not in res:
								print(child[i].text)
								res.append(coauthor)
	except Exception as exc: #Capture les erreurs inattendues
		print("An error occurred: ", exc)
		redirect("/error/403/" + f"An error occurred: " + str(exc))
	return res

@route("/search/authors/<searchString>")
def search_aut(searchString):
	"""
	La fonction permet de chercher un auteur qui possède la chaine de caractère searchString.
	Elle retourne une liste d'auteurs.
	"""
	res = [f"Liste des auteurs contenant {searchString}: " + "<br/>"]
	try:
		for child in root:
			if len(child):
				for data in child: #Boucle permettant de vérifier que la donnée n'est pas vide
					if data.text != None and searchString in data.text:
						for i in range(len(child)):
							if "author" == child[i].tag and child[i].text != None:
								author = dumps([(child[i].tag + " : " +child[i].text)])+ "<br/>"
								if (searchString in child[i].text or searchString.upper() in child[i].text) and author not in res:
									print(child[i].text)
									res.append(author)
	except Exception as exc: #Capture les erreurs inattendues
		print("An error occurred: ", exc)
		redirect("/error/403/" + f"An error occurred: " + str(exc))
	return res

@route("/search/publications/<searchString>")
def search_pub(searchString):
	"""
	La fonction retourne une liste de publications contenant searchString en titre.
	Un paramètre filter permet de faire une recherche plus précise.
	"""
	res = [f"Liste des publications contenant {searchString}: " + "<br/>"] #Retourne les publications
	param = request.query.get("filter") #Recherche des paramètres disponibles s'il y en a
	existsParam = False #Indique la présence de paramètre
	options = [] #Contient tout les paramètres
	try:
		if param is None: #Vérifie s'il y a un argument
			print("no parameter")
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
						pub_title = ""
						for i in range(len(child)): #Recherche du titre
							if "title" == child[i].tag and child[i].text != None and searchString in child[i].text:
								found = True
								pub_title = dumps([child[i].tag + " : " + child[i].text]) + "<br/>"
								break
						if existsParam and found:
							for op in options:
								found = False #Un titre contenant searchString est trouvé, on réinitialise found pour trouver les options.
								for i in range(len(child)):
									if child[i].text != None:
										if op[0] == child[i].tag and op[1] in child[i].text:
											print(child[i].text)
											found = True
											break
								if not found: #Si l'option n'a pas été trouvée, alors on quitte la boucle puisque ce n'est pas la bonne publication
									break
							if found:
								print("Publication trouvée!")
								res.append(pub_title)
						elif found:
							for i in range(len(child)):
								if 'title' == child[i].tag and child[i].text != None and searchString in child[i].text:
									print(child[i].text)
									res.append(pub_title)
	except Exception as exc: #Capture les erreurs inattendues
		print("An error occurred: ", exc)
		redirect("/error/403/" + f"An error occurred: " + str(exc))
	return res

#@route("/authors/<name_origin>/distance/<name_destination>")
#def authors_distance(name_origin, name_destination):

@route("/error/<code:int>/<msg>")
def error(code, msg):
	abort(code, msg)


run(host='localhost', port=8080)

