from socket import *
from time import *

serverName = 'localhost'
serverPort = 1234

clientSocket = socket(AF_INET,SOCK_DGRAM)

nb_samples = 100
avg_TTL = 0
sum_TTL = 0

for i in range(nb_samples):
	start = time_ns()
	clientSocket.sendto(b"PING",(serverName,serverPort))
	clientSocket.recvfrom(2048)
	stop = time_ns()
	sum_TTL += stop - start

avg_TTL = (sum_TTL / nb_samples)

print(f"Average TTL from {nb_samples} samples is {avg_TTL}ns") 

clientSocket.close()