from requests import *
server_ip = "127.0.0.1"
server_port = 8080
r1 = get(f"http://{server_ip}:{server_port}/authors/Louise A. Dennis")
print(r1.text)

"""
from requests import *
server_ip = "127.0.0.1"
server_port = 8080
r1 = get(f"http://{server_ip}:{server_port}/add/4/5")
print(r1.text)
r2 = get(f"http://{server_ip}:{server_port}/add/7/14")
print(r2.text)
"""
