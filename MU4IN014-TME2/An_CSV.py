# Exercice 5

from csv import *

def print_infos(f):
	"""
	Fonction qui affiche pour chaque entrées : titre, auteur et nombre de prêts.
	"""
	first_line = True
	with open(f, newline='') as csvfile:
		r = reader(csvfile, delimiter=';', quotechar='|')
		if first_line:
			next(r)
		for row in r:
			print(f'titre: {row[3]}\tauteur: {row[4]}\tprêts: {row[2]}')

def print_doc(f):
	"""
	Fonction qui affiche le nombre de prêts par type de documents.
	"""
	list_type = []
	list_nb_pret = []
	first_line = True
	
	#Recherche des différents type de documents
	with open(f, newline='') as csvfile:
		r = reader(csvfile, delimiter=';', quotechar='|')
		if first_line:
			next(r)
		for row in r:
			if row[1] not in list_type:
				print('Type added: ', row[1])
				list_type.append(row[1])
	
	#Rercherche du nombre de prêts par type de documents
	for t in list_type:
		with open(f, newline='') as csvfile:
			r = reader(csvfile, delimiter=';', quotechar='|')
			if first_line:
				next(r)
			nb_pret = 0
			for row in r:
				if row[1] == t:
					nb_pret += int(row[6])
			list_nb_pret.append((t, nb_pret))
		
	for nb in list_nb_pret:
		print(nb)

def print_cost_effectiveness(f):
	"""
	Fonction qui affiche les titres dans l'ordre de rentabilité.
	"""
	first_line = True
	list_cost_effectiveness = []
	
	with open(f, newline='') as csvfile:
		r = reader(csvfile, delimiter=';', quotechar='|')
		if first_line:
			next(r)
		for row in r:
			list_cost_effectiveness.append((int(row[8]), row[3]))

	list_sorted = sorted(list_cost_effectiveness, reverse=True)	
	for c in list_sorted:
		print(c)
# Question 2
print_infos('les-titres-les-plus-pretes.csv')

# Question 3
print_doc('les-titres-les-plus-pretes.csv')

# Question 4
print_cost_effectiveness('les-titres-les-plus-pretes.csv')
