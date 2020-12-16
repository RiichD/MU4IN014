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
	Elle retourne un dictionnaire contenant les informations.
	"""
	res = {}
	nb_pub = 0
	if id <= 0: #id ne peut pas être inférieur à 1
		redirect("/error/403/" + f"{id} is not between 1 or more and the id must be an integer, try again.")
	for child in root:
		if nb_pub == id-1:
			n = 0 #Entier permettant de différencier les clés identiques
			for i in range(len(child)):
				if child[i].tag in res: #Cas lorsqu'il y a plusieurs clés identiques
					res[child[i].tag + str(n)] = child[i].text
					n += 1
				else: #Cas lorsqu'il n'y a qu'une seule clé
					res[child[i].tag] = child[i].text
					n = 0
			return res
		else:
			nb_pub += 1
	redirect("/error/404/"+"Page not found") #Erreur s'il n'y a aucune publication

@route("/publications")
def publications():
	"""
	La fonction permet d'obtenir les publications les limit premières publications.
	Un paramètre limit peut être utilisé pour modifier cette limite sur l'URL. 
	Sinon, il est aussi possible de modifier via la variable globale PUB_LIMIT.
	La fonction retourne un dictionnaire de la liste des publications, les données sont stockées dans un dictionnaire.
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
		tmp = {} #Stocke les informations temporairement
		isNull = True
		n = 0 #Entier permettant de différencier les clés identiques
		for i in range(len(child)):
			if child[i].text is not None:
				if child[i].tag in tmp:
					tmp[child[i].tag + str(n)] = child[i].text
					n += 1
				else:
					tmp[child[i].tag] = child[i].text
					n = 0
				isNull = False
		if not isNull: #S'il y a des données, on ajoute tmp dans la liste res
			res.append(tmp)
		if len(res) == limit:
			return {'data':res}
	redirect("/error/404/"+"Page not found")

@route("/authors/<name>")
def authors(name):
	"""
	La fonction retourne le nombre de fois que name a publié en tant que coauteur et le nombre de coauteurs.
	Le résultat est un dictionnaire contenant un autre dictionnaire.
	"""
	res = [] #Liste des coauteurs
	estCoauteur = 0 #Le nombre de fois que l'auteur est un coauteur
	try:
		for child in root:
			isAuthor = False
			isCoauthor = False
			for data in child: #Boucle vérifiant si name est trouvé en tant qu'auteur
				if 'author' == data.tag and data.text is not None and name == data.text:
					print(f"{data.text} is an author")
					isAuthor = True
					break
			
			if isAuthor:
				for data in child: #Boucle recherchant les coauteurs de name
					author = {}
					if 'author' == data.tag and data.text is not None:
						author[data.tag] = data.text
						if name != data.text:
							isCoauthor = True
							if author not in res:
								print(data.text+" is a coauthor")
								res.append(author)
					else:
						break
			if isCoauthor:
				estCoauteur += 1
	except Exception as exc: #Capture les erreurs inattendues
		print("An error occurred: ", exc)
		redirect("/error/403/" + f"An error occurred: " + str(exc))
	print("Liste des coauteurs:\n", res)
	return {'data':{'Publications':estCoauteur,'Coauteurs':len(res)}}
	
@route("/authors/<name>/publications")
def auth_pub(name):
	"""
	La fonction retourne un dictionnaire de la liste des publications de name, les données sont stockées dans un dictionnaire.
	"""
	res = []
	i = 0 #Iterator
	min = 0 #Indice à partir duquel on veut récupérer les informations
	isCounting = False
	
	#Récupération des paramètres et vérification de ces paramètres
	param_start = request.query.get("start")
	param_count = request.query.get("count")
	param_order = request.query.get("order")
	if param_start is None:
		print("Start parameter not enabled\n")
	else:
		if not param_start.isnumeric() or int(param_start) < 0:
			print("Start parameter not enabled: Value below 0\n")
			redirect("/error/403/" + "An error occurred: start value is below 0! Must be a number, integer between 0 or more")
		else:
			min = int(param_start)
			print(f"Start parameter enabled, starting at {min}\n")
	
	if param_count is None:
		print("Count parameter not enabled\n")
	else:
		if not param_count.isnumeric() or int(param_count) < 0:
			print("Count parameter not enabled: Value below 0\n")
			redirect("/error/403/" + "An error occurred: count value is below 0! Must be a number, integer between 0 or more")
		else:
			print(f"Count parameter enabled, retrieving {param_count} values\n")
			isCounting = True
	max = 100+min
	
	#Rercherche des informations souhaitées
	try:
		for child in root:
			pub = {} #Dictionnaire contenant les informations
			isAuthor = False
			n = 0
			for data in child:
				if data.text is not None:
					if data.tag in pub: #Cas lorsqu'il y a plusieurs clés identiques
						pub[data.tag + str(n)] = data.text
						n += 1
					else:
						pub[data.tag] = data.text	
						n = 0
					if not isAuthor and 'author' == data.tag and name == data.text:
						isAuthor = True
			if isAuthor: #L'auteur a été trouvé dans cette publication, on l'ajoute dans la liste si les conditions le permet
				if min > i:
					i += 1
				elif isCounting and len(res) >= int(param_count):
					break
				elif len(res) < max-min:
					print(f"{name} is an author of {pub}\n")
					res.append(pub)
	except Exception as exc: #Capture les erreurs inattendues
		print("An error occurred: ", exc)
		redirect("/error/403/" + f"An error occurred: " + str(exc))
	
	#Gère les clés et l'ordre
	keyExists = False
	isInteger = True
	if param_order:
		for r in res:
			if param_order in r:
				print(f'{param_order} exists\n')
				keyExists = True
				break
	
	if keyExists:
		tmp = []
		for r in res: #Boucle permettant de vérifier si la clé existe et si c'est un entier
			if param_order in r:
				tmp.append(r)
				if isInteger:
					try:
						if int(r[param_order]):
							continue
					except ValueError as exc: #Ce n'est pas entier, l'ordre dépend des caractères
						isInteger = False
						print(f'{param_order} is not an integer\n')
		if len(tmp) > 0:
			if isInteger:
				print(f"{param_order} is an integer\n")
				res_ordered=sorted(tmp, key=lambda x: int(x[param_order]))
			else:
				res_ordered=sorted(tmp, key=lambda x: x[param_order])
			for r in res:
				if r not in res_ordered:
					res_ordered.append(r) #Les cas qui ne peuvent pas être ordonné sont à la fin de la liste
			return {'data':res_ordered}
	return {'data':res}


@route("/authors/<name>/coauthors")
def auth_pub(name):
	"""
	La fonction retourne tout les coauteurs de name sous la forme d'un dictionnaire de la liste de coauteurs.
	Les données sont stockées sous forme de dictionnaire.
	"""
	res = [] #Liste des coauteurs
	i = 0 #Iterator
	min = 0 #Indice à partir duquel on veut récupérer les informations
	isCounting = False
	
	#Recherche des paramètres et vérifications de ces paramètres
	param_start = request.query.get("start")
	param_count = request.query.get("count")
	param_order = request.query.get("order")
	if param_start is None:
		print("Start parameter not enabled\n")
	else:
		if not param_start.isnumeric() or int(param_start) < 0:
			print("Start parameter not enabled: Value below 0\n")
			redirect("/error/403/" + "An error occurred: start value is below 0! Must be a number, integer between 0 or more")
		else:
			min = int(param_start)
			print(f"Start parameter enabled, starting at {min}\n")
	
	if param_count is None:
		print("Count parameter not enabled\n")
	else:
		if not param_count.isnumeric() or int(param_count) < 0:
			print("Count parameter not enabled: Value below 0\n")
			redirect("/error/403/" + "An error occurred: count value is below 0! Must be a number, integer between 0 or more")
		else:
			print(f"Count parameter enabled, retrieving {param_count} values\n")
			isCounting = True
	max = 100+min
	
	#Boucle recherchant les informations souhaitées
	try:
		for child in root:
			isAuthor = False
			isCoauthor = False
			for data in child: #Boucle vérifiant si name est trouvé en tant qu'auteur
				if 'author' == data.tag and data.text is not None and name == data.text:
					print(f"{data.text} is an author")
					isAuthor = True
					break
			
			if isAuthor: #C'est un auteur de la publication, recherche des autres auteurs (coauteurs)
				for data in child:
					author = {}
					if 'author' == data.tag and data.text is not None:
						author[data.tag] = data.text
						if name != data.text:
							isCoauthor = True
							if author not in res: #Un auteur différent de name est trouvé
								if min > i:
									i += 1
								elif isCounting and len(res) >= int(param_count):
									break
								elif len(res) < max-min:
									print(data.text+" is a coauthor")
									res.append(author)
					else:
						break
	except Exception as exc: #Capture les erreurs inattendues
		print("An error occurred: ", exc)
		redirect("/error/403/" + f"An error occurred: " + str(exc))
	print("Liste des coauteurs:\n", res)
	if param_order == "author": #Il n'y a que la clé author dans la liste
		res_ordered=sorted(res, key=lambda x: x["author"])
		return {'data':res_ordered}
	return {'data':res}

@route("/search/authors/<searchString>")
def search_authors(searchString):
	"""
	La fonction permet de chercher un auteur qui possède la chaine de caractère searchString.
	Elle retourne une dictionnaire de la liste d'auteurs. Les données sont dans un dictionnaire.
	"""
	res = []
	i = 0 #Iterator
	min = 0 #Indice à partir duquel on veut récupérer les informations
	isFull = False #Booléen qui indique si la liste d'auteurs a atteint le maximum
	isCounting = False
	
	#Recherche des paramètres et vérifications de ces paramètres
	param_start = request.query.get("start")
	param_count = request.query.get("count")
	param_order = request.query.get("order")
	if param_start is None:
		print("Start parameter not enabled\n")
	else:
		if not param_start.isnumeric() or int(param_start) < 0:
			print("Start parameter not enabled: Value below 0\n")
			redirect("/error/403/" + "An error occurred: start value is below 0! Must be a number, integer between 0 or more")
		else:
			min = int(param_start)
			print(f"Start parameter enabled, starting at {min}\n")
	
	if param_count is None:
		print("Count parameter not enabled\n")
	else:
		if not param_count.isnumeric() or int(param_count) < 0:
			print("Count parameter not enabled: Value below 0\n")
			redirect("/error/403/" + "An error occurred: count value is below 0! Must be a number, integer between 0 or more")
		else:
			print(f"Count parameter enabled, retrieving {param_count} values\n")
			isCounting = True
	
	if searchString == '*':
		searchString = '' #Vide donc on récupère tout les auteurs
	max = 100+min
	
	try:
		for child in root:
			for data in child:
				author = {}
				if 'author' == data.tag and data.text is not None:
					author[data.tag] = data.text
					if searchString in data.text and author not in res:
						if min > i: #L'auteur à cet indice est ignoré
							i += 1
						elif  i >= max: #Le nombre d'auteurs a retourner en résultat est au maximum
							isFull = True
						elif isCounting and len(res) >= int(param_count):
							isFull = True
						elif len(res) < max-min:
							print(author)
							res.append(author)
						else:
							isFull = True
				if isFull:
					break
			if isFull:
				break
	except Exception as exc: #Capture les erreurs inattendues
		print("An error occurred: ", exc)
		redirect("/error/403/" + f"An error occurred: " + str(exc))
	print("Nombre d'auteurs trouvés: ", len(res))
	if param_order == "author":
		res_ordered=sorted(res, key=lambda x: x["author"])
		return {'data':res_ordered}
	return {'data':res}

@route("/search/publications/<searchString>")
def search_pub(searchString):
	"""
	La fonction retourne une liste de publications contenant searchString en titre.
	Un paramètre filter permet de faire une recherche plus précise.
	"""
	res = [] #Liste des publications
	i = 0 #Iterator
	min = 0 #Indice à partir duquel on veut récupérer les informations
	filter_list = [] #Liste des filtres
	isFilter = False
	isCounting = False
	
	#Recherche des paramètres et vérifications de ces paramètres
	param_filter = request.query.get("filter")
	param_start = request.query.get("start")
	param_count = request.query.get("count")
	param_order = request.query.get("order")
	
	if param_filter is None:
		print("No filter available\n")
	else:
		print("Filter activating, checking...\n")
		for f in param_filter.split(","):
			key_value = f.split(":")
			if len(key_value) == 2:
				print(f"Parameter {f} added\n")
				filter_list.append(key_value)
				isFilter = True
			else:
				print(f"Parameter {f} doesn't contain key:value\n")
		if not isFilter:
			print("Filter not working, try again\n")
			redirect("/error/403/" + f"An error occurred: Filter wrong format! key:value")
		else:
			print("Filter is activated\n")
	if param_start is None:
		print("Start parameter not enabled\n")
	else:
		if not param_start.isnumeric() or int(param_start) < 0:
			print("Start parameter not enabled: Value below 0\n")
			redirect("/error/403/" + "An error occurred: start value is below 0! Must be a number, integer between 0 or more")
		else:
			min = int(param_start)
			print(f"Start parameter enabled, starting at {min}\n")
	
	if param_count is None:
		print("Count parameter not enabled\n")
	else:
		if not param_count.isnumeric() or int(param_count) < 0:
			print("Count parameter not enabled: Value below 0\n")
			redirect("/error/403/" + "An error occurred: count value is below 0! Must be a number, integer between 0 or more")
		else:
			print(f"Count parameter enabled, retrieving {param_count} values\n")
			isCounting = True
	
	if searchString == '*':
		searchString = '' #Vide donc on récupère tout les auteurs
	max = 100+min
	
	try:
		for child in root:
			cpt_filter = 0 #Compte le nombre de filtre
			titleExists = False
			dict_res = {} #Ne pas utiliser clear() pour vider!
			n = 0
			isAuthor = False
			for data in child: #Recherche d'un titre contenant searchString
				if data.text is not None:
					if 'author' in data.tag: #S'il y a un auteur et non un editeur ou autre
						isAuthor = True
					if data.tag in dict_res: #Cas lorsqu'il a plusieurs clés similaires
						dict_res[data.tag + str(n)] = data.text
						n += 1
					else:
						dict_res[data.tag] = data.text
						n = 0
					if "title" == data.tag and searchString in data.text:
						titleExists = True
			
			#Cas si searchString est dans le titre
			if isAuthor and titleExists and not isFilter and dict_res not in res: #Cas si le filtre n'est pas activé
				if min > i:
					i += 1
				elif i >= max or (isCounting and len(res) >= int(param_count)) or len(res) >= max-min:
					break
				else:
					print(f"{dict_res} added with filters\n")
					res.append(dict_res)
			elif isAuthor and titleExists and isFilter and dict_res not in res:
				for data in child:
					if data.text is not None:
						for f in filter_list:
							if f[0] in data.tag and f[1] in data.text: #Comparaison de toutes les options dans le filtre
								cpt_filter += 1 #Le compteur doit être égal au nombre de filtre présent dans la liste pour que ce soit une publication valable
					
				if isFilter and cpt_filter >= len(filter_list) and titleExists: #Cas si le filtre est activé et valable
					if min > i:
						i += 1
					elif i >= max or (isCounting and len(res) >= int(param_count)) or len(res) >= max-min:
						break
					else:
						print(f"{dict_res} added with filters\n")
						res.append(dict_res)
	except Exception as exc: #Capture les erreurs inattendues
		print("An error occurred: ", exc)
		redirect("/error/403/" + f"An error occurred: " + str(exc))
	
	#Gère les clés et l'ordre
	keyExists = False
	isInteger = True
	if param_order:
		for r in res:
			if param_order in r:
				print(f'{param_order} exists\n')
				keyExists = True
				break
	
	if keyExists:
		tmp = []
		for r in res: #Boucle permettant de vérifier si la clé existe et si c'est un entier
			if param_order in r:
				tmp.append(r)
				if isInteger:
					try:
						if int(r[param_order]):
							continue
					except ValueError as exc:
						isInteger = False
						print(f'{param_order} is not an integer\n')
		if len(tmp) > 0:
			if isInteger:
				print(f"{param_order} is an integer\n")
				res_ordered=sorted(tmp, key=lambda x: int(x[param_order]))
			else:
				res_ordered=sorted(tmp, key=lambda x: x[param_order])
			for r in res:
				if r not in res_ordered:
					res_ordered.append(r) #Les cas qui ne peuvent pas être ordonné sont à la fin de la liste
			return {'data':res_ordered}
		redirect("/error/403/" + f"data with order is not working: Empty list")
	else:
		print("data without key\n")
		return {'data':res}

@route("/authors/<name_origin>/distance/<name_destination>")
def authors_distance(name_origin, name_destination):
	"""
	La fonction retourne la distance entre name_origin et name_destination.
	Je précise que je n'ai pas très bien compris quelle est la distance ici.
	"""
	return 0

@route("/error/<code:int>/<msg>")
def error(code, msg):
	"""
	La fonction retourne les erreurs, le code correspondant au code HTTP.
	"""
	abort(code, msg)


run(host='localhost', port=8080)

