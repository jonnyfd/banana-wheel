# Import socket module 
import socket             

# Create a socket object 
s = socket.socket()         
 
# connect to the server on local computer 
s.connect(('0.0.0.0', 6699)) 
msg = s.recv(1024)
print(msg.decode("utf-8"))
# once connected, print "welcome to banana wheel"
name = input("What is your name? \n")
s.send(bytes(name, "utf-8"))
shortly = s.recv(1024)
print(shortly.decode("utf-8"))
while True:
	pass



