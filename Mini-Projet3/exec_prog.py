from subprocess import run
from threading import *
"""
Parameters:
 -contagion_period: [=X] nodes contaminate others for X time units on average (default 200)
 -gui:              [=0] do not show GUI
                    [=1]* show GUI (default)
 -height:           [=X] area is X units tall (default 1000)
 -help:             show this message
 -immune_period:    [=X] nodes remain immune for X time units on average (default 300)
 -infection_period: [=X] nodes get infected if they remain close to an infected node for X time units on average (default 100)
 -nb_infected:      [=X] initial number of infected nodes (default 2)
 -nb_nodes:         [=X] initial number of total nodes (default 120)
 -nb_snapshots:     [=X] total number of snapshots before simulation stops (default -1: infinite)
 -printout:         [=0] do not print anything
                    [=1]* print #sane, #infected, #immune (default)
                    [=2] print the status of every node
 -show_parameters:  [=0] do not show parameters
                    [=1]* show parameters (default)
 -snapshot_period:  [=X] make a snapshot every X time units (default 10)
 -stop_all_sane:    [=0]* do not stop the simulation when all nodes are sane (default)
                    [=1] stop the simulation when all nodes are sane
 -travel_distance:  [=X] nodes can move within a X*X square (default 200)
 -width:            [=X] area is X units wide (default 1000)
-----
"""

def exec_program(nb_samples, nb_snapshots, nb_infected, travel_distance, infection_period, contagion_period, immune_period, nb_nodes, filename):
	"""
	Fonction qui exécute le programme.
	
	filename: Nom du fichier

	nb_snapshots: Limite de snapshot pour éviter des exécutions infinies
	nb_samples: Nombres de tests souhaités pour les mêmes paramètres
	
	nb_infected: 2 par défaut
	travel_distance: 200 par défaut
	infection_period: 100 par défaut
	contagion_period: 200 par défaut
	immune_period: 300 par défaut
	nb_nodes: 100 par défaut, erreur dans -help	
	"""
	prog = ['java', '-jar', 'Virus.jar', '-gui=0', f'-nb_snapshots={nb_snapshots}', '-printout=2','-stop_all_sane=1']
	prog.append(f'-nb_infected={nb_infected}')
	prog.append(f'-travel_distance={travel_distance}')
	prog.append(f'-infection_period={infection_period}')
	prog.append(f'-contagion_period={contagion_period}')
	prog.append(f'-immune_period={immune_period}')
	prog.append(f'-nb_nodes={nb_nodes}')
	for i in range(0, nb_samples):
		print(f"fichier {filename}: Execution numéro {i}\n")
		res = run(prog, capture_output=True)
		with open(filename,'a') as f:
			f.write(res.stdout.decode('utf-8'))

for nb_exec in range(1, 10):
	nb_snaps = 2500
	nb_samp = 25
	nb_inf = nb_exec
	travel_dist = 200
	infec_period = 100
	cont_period = 200
	immu_period = 300
	nb_nod = 100
	f_name = "exec_data/nb_infected-"+str(nb_exec)+".txt"
	Thread(target=exec_program, args=(nb_samp, nb_snaps, nb_inf, travel_dist, infec_period, cont_period, immu_period, nb_nod, f_name,)).start()
