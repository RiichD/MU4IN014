# Exercice 2

import xml.etree.ElementTree as ET

tree=ET.parse('cd_catalog.xml')
root=tree.getroot()

def get_data():
	"""
	Fonction récupérant le titre, l'artiste, le pays, la compagnie et l'année de tout les CD.
	"""
	for child in root:
		print("Titre :", child[0].text)
		print("Artiste :", child[1].text)
		print("Pays :", child[2].text)
		print("Compagnie :", child[3].text)
		print("Année :", child[5].text, "\n")
		
def get_from_year(year):
	"""
	Fonction récupérant la liste des CD des années year.
	year doit est supérieur ou égal à 1000.
	"""
	print(f"\nListe des CD des années {year}:\n")
	for child in root:
		if child[5].text[0:3] == year[0:3]:
			print(child[0].text)
			
def get_from_lang(country):
	"""
	Fonction récupérant les CD provenant de country.
	"""
	print(f"\nListe des CD provenant du {country}:\n")
	for child in root:
		if child[2].text == country:
			print(child[0].text)
# Question 2
get_data()

# Question 3
get_from_year('1980')

# Question 4
get_from_lang('UK')
