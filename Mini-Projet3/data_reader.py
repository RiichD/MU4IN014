from numpy import *
from pandas import *
from re import *
from matplotlib import pyplot
from glob import *

list_file = glob("nb_nodes/*.txt")

do_output = True #True si on veut un fichier de sortie pour les résultats, False sinon
output_file = "data.txt" #Nom du fichier de sortie contenant les informations récupérées

#open(output_file, 'w').close() #Vide le fichier

cpt_read = 0 #Compte le nombre de fichier lu

option_line = 'nodes.' #Indique quelle ligne l'option a été modifiée
"""
Options list:
infected nodes initially
as travel distance
as infection period
as contagion period
as immune period
nodes.
"""
	
for filename in list_file:
	name = 'i' #Nom de chaque ligne
	number_i = 0 #Nombre correspondant aux itérations de chaque ligne

	nb_tests = 0 #Compteur du nombre de tests effectués

	res = {} #Dictionnaire contenant 

	tab_i_list = [] #Tableau contenant la liste des indices d'un test
	tab_i = [] #Tableau contenant les indices pronvenant d'un test
	
	option = -1 #Récupère l'option modifiée en question
	
	print(f"Lecture du fichier {filename}\n")
	with open(filename, "r") as f:
		for line in f:
			tmp = []
			isData = True
			if option == -1 and option_line in line:
				option = int(line.split(' ')[1])
			for data in line.split(' '):
				if data != '' and data != '\n' and data.isnumeric():
					tmp.append(int(data))
				elif data == '' or data == '\n':
					continue
				else:
					if data == 'Simulation': #Nouvelle simulation trouvée, réinitialisation des variables
						if len(tab_i) > 0:
							tab_i = []
						tab_i_list.append(tab_i)
						nb_tests += 1
					isData = False
					break
			
			if isData and len(tmp) > 0: #Une donnée ne contient que des entiers
				res[name+str(number_i)] = tmp
				tab_i.append(name+str(number_i))
				number_i += 1

	if len(res) > 0:
		tab_time = [] #Contient la durée de chaque exécution
		tab_max_infec = [] #Contient le nombre d'infecté pour chaque itération
		tab_mult_infec = [] #Tableau des multi_infections
		
		df = DataFrame(res)
		dfT = df.T
		print(dfT)
		print("Nombre de tests:", nb_tests)
		cpt_read += 1
		print(f"Nombre de fichiers lus: {cpt_read}\n")
		
		for i in range(0, number_i):
			if 1 in df[name+str(i)].value_counts():
				tab_max_infec.append(df[name+str(i)].value_counts()[1])
		
		for i_list in tab_i_list:
			sum_mult_infec = 0
			for n in range(0, len(df)): #Parcours de tous les individus
				isInfected = False
				cpt_infec = 0 #Compteur de multi-infections
				for i in i_list:
					if df[i][n] == 1 and not isInfected: #Etat lorsque l'individu est infecté
						cpt_infec += 1
						isInfected = True
					elif (df[i][n] == 2 or df[i][n] == 0) and isInfected: #Etat lorsque l'individu guéri
						isInfected = False
				if cpt_infec > 1: #Il faut être infecté au moins 2 fois pour être considéré comme une multi-infection
					sum_mult_infec += cpt_infec
			tab_mult_infec.append(sum_mult_infec)
		if do_output:
			f_out = open(output_file, "a")
			
			for t in tab_i_list:
				tab_time.append(len(t))
			
			data_out = f"filename={filename}\n"
			data_out += f"nb_tests={nb_tests}\n"
			data_out += f"option={option}\n"
			data_out += f"list_time={tab_time}\n"
			data_out += f"list_max_infec={tab_max_infec}\n"
			data_out += f"list_mult_infec={tab_mult_infec}\n"
			data_out += f"-----\n"
			
			f_out.write(data_out)
		
			f_out.close()
