# Import socket module 
import socket             
import sys
# Create a socket object 
s = socket.socket()         
 
# connect to the server on local computer 
s.connect(('0.0.0.0', 6699)) 
# sets players name to command line argument
name = str(sys.argv[1])
# sends name to server
s.send(bytes(name, "utf-8"))
shortly = s.recv(1024)
print(shortly.decode("utf-8"))
whoisjudge = s.recv(1024)
print(whoisjudge.decode("utf-8"))
poke = s.recv(1024)
if name in str(whoisjudge.decode("utf-8")):
	print(poke.decode("utf-8"))
	prompt = input("Enter prompt, make sure to include a '_': \n")
	print(f"Sending prompt to server...")
	s.send(bytes(prompt, "utf-8"))
while True:
	pass




