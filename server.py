import socket
import select


num_players = 2
sock_list = list()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 6699))
s.listen(num_players)
sock_list.append(s)


curr_players = 0
while curr_players < num_players:
	active_socket = select.select(sock_list, [], [])[0][0]

	if active_socket == s:
		clientsocket, address = s.accept()
		sock_list.append(clientsocket)
		curr_players += 1
		print("New client")

	else:
		print(active_socket.recv())


print("All players are ready")
