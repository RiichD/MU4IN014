from numpy import *
from pandas import *
from re import *
from matplotlib import pyplot
from glob import *

list_file = glob("nb_nodes/*.txt")
for filename in list_file:
	nb_tests = 0 #Compteur du nombre de tests effectués
	print(f"Lecture du fichier {filename}\n")
	with open(filename, "r") as f:
		for line in f:
			for data in line.split(' '):
				if data == 'Simulation': #Nouvelle simulation trouvée, réinitialisation des variables
						nb_tests += 1
	print(f"Nombre de tests pour {filename}: {nb_tests}\n")
