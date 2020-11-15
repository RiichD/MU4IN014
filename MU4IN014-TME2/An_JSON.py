# Exercice 3

from json import *

def get_data(file_path):
	"""
	Fonction permettant d'obtenir le nom du réalisateur, le titre, l'arrondissement, la date de début et de fin et les coordonnées géographiques de file_path.
	"""
	data = {}

	with open(file_path) as infile:
		data = load(infile)
		for p in data:
			try:
				f = p['fields']
				if f.get('nom_realisateur'):
					print("Réalisateur :", f['nom_realisateur'])
				else:
					print("Realisateur inconnu")
				
				if f.get('nom_tournage'):
					print("Titre :", f['nom_tournage'])
				else:
					print("Titre inconnu")
				
				if f.get('ardt_lieu'):
					print("Arrondissement :", f['ardt_lieu'])
				else:
					print("Arrondissement inconnu")
				
				if f.get('date_debut'):
					print("Date de début :", f['date_debut'])
				else:
					print("Date de début inconnue")
				
				if f.get('date_fin'):
					print("Date de fin :", f['date_fin'])
				else:
					print("Date de fin inconnue")
				
				if f.get('geo_shape'):
					print("Coordonnées géographiques :", f['geo_shape'])
				else:
					print("Coordonnées géographiques inconnues")
				
				print('\n')
			except TypeError:
				print("data not available")

def get_for_each_film(file_path, fileFormat, fileName):
	"""
	Fonction qui affiche les réalisateurs, les dates de tournage et les lieux de chaque film.
	Comme il y a beaucoup de données à afficher, une version qui enregistre les données dans un fichier est possible:
		fileFormat vrai => les données sont écrites dans un fichier. Faux sinon, et  l'affichage se fait sur le terminal.
		fileName => nom du fichier si fileFormat est vrai.
	"""
	data = {}
	list_Title = [] #Contient la liste des films affichés pour éviter d'afficher deux fois un même film.
	try :
		if fileFormat:
			f = open(fileName, 'w+')
		with open(file_path) as infile:
			data = load(infile)
			for p in data:
				try:
					f1 = p['fields']
					if f1.get('ardt_lieu') and f1['nom_tournage'] not in list_Title:
						if fileFormat:
							f.write('\n'+str(f1['nom_tournage'])+'\n\n')
						else:
							print("\n#####")
							print("Nom du tournage :", f1['nom_tournage'])
							print("#####")
						for n in data:
							f2 = n['fields']
							if f2.get('nom_tournage') and (f2['nom_tournage'] not in list_Title) and (f1['nom_tournage'] == f2['nom_tournage']):
								nom = "Réalisateur inconnu" 
								date_deb = "Date de début inconnue"
								date_fin = "Date de fin inconnue"
								lieu = "Lieu inconnu"
								adresse = 'Adresse inconnue'
								if f2.get('nom_realisateur'):
									nom = f2['nom_realisateur']
								
								if f2.get('date_debut'):
									date_deb = f2['date_debut']
								
								if f2.get('date_fin'):
									date_fin = f2['date_fin']
								
								if f2.get('id_lieu'):
									lieu = "Lieu :", f2['id_lieu']
								
								if f2.get('adresse_lieu'):
									adresse = "Adresse lieu :", f2['adresse_lieu']
								dic = {'Réalisateur':nom, 'Date_deb':date_deb, 'Date_fin':date_fin, 'Lieu':lieu, 'Adresse':adresse}
								if fileFormat:
									f.write(str(dic)+'\n')
								else:
									print(dic)
						list_Title.append(f1['nom_tournage'])
				except TypeError:
					print("data not available")
		if fileFormat:
			f.close()
	except Exception as exc:
		print("File error", exc)
	
def nb_shooting_per_ardt(file_path):
	"""
	Fonction qui affiche le nombre de tournages dans chaque arrondissement.
	"""
	data = {}
	list_ardt = [] #Contient tous les arrondissements provenant du fichier.
	list_count = [] #Contient le nombre d'occurrences de chaque arrondissements à l'indice respectif.
	
	with open(file_path) as infile:
		data = load(infile)
		for p in data:
			try:
				f = p['fields']
				if f.get('ardt_lieu') and f['ardt_lieu'] not in list_ardt:
					list_ardt.append(f['ardt_lieu'])
					list_count.append(1)
				else:
					list_count[list_ardt.index(f['ardt_lieu'])] +=1
			except TypeError:
				print("data not available")
	
	for i in range(0,len(list_ardt)):
		print(f"Il a eu {list_count[i]} tournages dans l'arrondissement {list_ardt[i]}")

# Question 2
#get_data('lieux-de-tournage-a-paris.json')

# Question 3 Plus lisible si la valeur vaut True pour fileFormat
get_for_each_film('lieux-de-tournage-a-paris.json', False, 'film_data.txt')

# Question 4
#nb_shooting_per_ardt('lieux-de-tournage-a-paris.json')

