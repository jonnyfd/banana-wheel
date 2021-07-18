# import socket and select modules 
import socket
import select

# the number of connections the server will wait for before starting game
num_players = 2

# list of clients
sock_list = list()

# specifies IPv4 over TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 6699))
s.listen(num_players)
# adds server to list of players
sock_list.append(s)


curr_players = 0
# while not everybody has connected yet, wait for connections
while curr_players < num_players:
	# reads from list of sockets. prepares us to sort between new connections and messages
	active_socket = select.select(sock_list, [], [])[0][0]
	# if new client, let em in. add them to the list of players.
	if active_socket == s:
		clientsocket, address = s.accept()
		sock_list.append(clientsocket)
		curr_players += 1
		print("New client")
		clientsocket.send(bytes("Welcome to banana wheel.", "utf-8"))
	# if not new client, this means that an old client is sending a message. print it.
	else:
		who = active_socket.recv(1024)
		# makes it personal
		active_socket.send(bytes("The game will start shortly " + str(who.decode("utf-8")) + ".", "utf-8"))
# lets go
print("All players are ready")

