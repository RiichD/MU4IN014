from numpy import *
from pandas import *
from matplotlib import pyplot
from re import *

filename = "travel_dist_data.txt" #Nom du fichier qui permet de réaliser les graphiques

out_name = "travel_dist" #Fichiers de sortie contenant ce nom, ainsi qu'un sous-dossier de ce nom
out_path = f"graphs/{out_name}/" #Chemin du fichier de sortie, ainsi que le sous-dossier du nom de out_name

legend_title = out_name

nb_files = 0 #Compteur du nombre de fichier #DEBUG

tab_option = [] #Tableau contenant les options modifiées
tab_time = [] #Tableau contenant des listes de durée d'exécution
tab_max_infec = [] #Tableau contenant des listes du maximum d'infectés par itération
tab_mult_infec = [] #Tableau contenant des listes des multi-infections par itération

with open(filename, 'r') as f:
	for line in f:
		tmp = []
		line_split = line.split('=')
		if line_split[0] == 'filename':
			nb_files += 1
		elif line_split[0] == 'option':
			tab_option.append(int(sub('\n', '', line_split[1])))
		elif line_split[0] == 'list_time':
			tmp = sub('[][,\n]', '', line_split[1]).split(' ')
			tab_time.append([int(t) for t in tmp])
		elif line_split[0] == 'list_max_infec':
			tmp = sub('[][,\n]', '', line_split[1]).split(' ')
			tab_max_infec.append([int(t) for t in tmp])
		elif line_split[0] == 'list_mult_infec':
			tmp = sub('[][,\n]', '', line_split[1]).split(' ')
			tab_mult_infec.append([int(t) for t in tmp])

def graph_builder(xlabel, ylabel, title, step, maxStep, output, data, toPlot):
	"""
	Fonction permettant de créer un graphe.
	
	Paramètres:
	xlabel: Nom du label en x
	ylabel: Nom du label en y
	title: Titre du graphique
	output: Nom du fichier de sortie avec chemin du dossier si nécessaire
	maxStep: Limite d'informations à récupérer
	step: Récupère les données d'intervalles step. Par exemple si la valeur est de 5, on récupère toutes les 5 itérations (0, 5, 10, 15, ...)
	toPlot: Liste contenant les valeurs à afficher. Si toPlot est vide, on affiche tout
	"""
	df = DataFrame()
	for n in range(0, len(data)):
		tmp = []
		s = 0
		while (s < maxStep and s < len(data[n])):
			tmp.append(data[n][s])
			s += step
		df[tab_option[n]]=Series(tmp)
	mean = df.mean(1)
	error = df.std(1) / sqrt(1000)
	if len(toPlot):
		for toP in toPlot:
			if toP in df:
				df[toP].plot()
	else:
		df.plot()
	mean.plot(color='b', label='mean', zorder=4)
	pyplot.fill_between(df.index, mean-3*error, mean+3*error,alpha=0.5, edgecolor='r', facecolor='r', zorder=3)
	pyplot.ylabel(ylabel)
	pyplot.xlabel(xlabel)
	pyplot.title(title)
	pyplot.legend(loc = 'upper right', title = legend_title, fancybox=True, framealpha=0.5)
	pyplot.savefig(output)

def histogram_builder(xlabel, ylabel, title, densityOn, binsSize, output, data, toPlot):
	"""
	Fonction permettant de créer un histogramme.
	
	Paramètres:
	xlabel: Nom du label en x
	ylabel: Nom du label en y
	title: Titre du graphique
	densityOn: Activation de la densité sur l'histogramme
	binsSize: Valeur de bins
	output: Nom du fichier de sortie avec chemin du dossier si nécessaire
	toPlot: Liste contenant les valeurs à afficher. Si toPlot est vide, on affiche tout
	"""
	df = DataFrame()
	for n in range(0, len(data)):
		if len(data[n]):
			df[tab_option[n]]=Series(data[n])
			if len(toPlot):
				if tab_option[n] in toPlot:
					df[tab_option[n]].hist(bins=binsSize,density=densityOn, color='b')
			else:
				df[tab_option[n]].hist(bins=binsSize,density=densityOn, color='b')
	pyplot.ylabel(ylabel)
	pyplot.xlabel(xlabel)
	pyplot.title(title)
	pyplot.savefig(output)

def heatmap_builder(size, drange, title, output, data):
	"""
	Fonction permettant de créer un heatmap.
	
	Paramètres:
	size: Nombre de cases pour une ligne
	drange: Liste contenant l'intervalle de valeur
	title: Titre du graphique
	output: Nom du fichier de sortie avec chemin du dossier si nécessaire
	"""
	df = DataFrame()
	tab_tmp = []
	for t in data:
		tab_tmp += t
	normal = Series(random.normal(loc=0,scale=1,size=size))
	d = Series(tab_tmp)
	for i in range(size):
		df["c" + str(i)] = cut(d*(i/size) + normal*(size-i)/size, drange).value_counts()
	pyplot.pcolor(df)
	si = sorted(df.index, key=lambda interval: interval.left)
	pyplot.yticks(arange(0.5, len(df.index), 1), si)
	pyplot.title(title)
	pyplot.savefig(output)
#TIME
graph_builder("Samples", "Time in iteration", "Time graph", 1, 10000, f"{out_path}time_graph_{out_name}.pdf", tab_time, list(range(0, 1000, 100)))
f9 = pyplot.figure(9)
histogram_builder("Time in iteration", "Density", "Time histogram", True, 1, f"{out_path}time_hist_{out_name}.pdf", tab_time, list(range(0, 300, 25))+list(range(700, 1000, 25)))
f8 = pyplot.figure(8)
heatmap_builder(100, list(range(0,10)), "Time heatmap", f"{out_path}time_heat_{out_name}.pdf", tab_time)
f7 = pyplot.figure(7)

#MAX
graph_builder("Time in iteration", "Infected", "Maximum infection graph", 1, 10000, f"{out_path}max_graph_{out_name}.pdf", tab_max_infec, list(range(0, 1000, 150)))
f6 = pyplot.figure(6)
histogram_builder("Maximum infected", "Density", "Maximum infected histogram", True, 20, f"{out_path}max_hist_{out_name}.pdf", tab_max_infec, list(range(0, 1000, 100)))
f5 = pyplot.figure(5)
heatmap_builder(1000, list(range(0,10)), "Maximum infected heatmap", f"{out_path}max_heat_{out_name}.pdf", tab_max_infec)
f4 = pyplot.figure(4)

#MULTI-INFECTIONS
graph_builder("Samples", "Number of multi-infections", "Multi-infections graph", 1, 10000, f"{out_path}mult_graph_{out_name}.pdf", tab_mult_infec, list(range(0, 1000, 100)))
f3 = pyplot.figure(3)
histogram_builder("Multi-infections", "Density", "Multi-infections histogram", True, 1, f"{out_path}mult_hist_{out_name}.pdf", tab_mult_infec, list(range(0, 1000, 25)))
f2 = pyplot.figure(2)
heatmap_builder(1000, list(range(0,10)), "Multi-infections heatmap", f"{out_path}mult_heat_{out_name}.pdf", tab_mult_infec)
pyplot.show()
