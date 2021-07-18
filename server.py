# import socket, select, random modules
import socket
import select
import random

class Player():

    def __init__(self, sock: socket.socket, name: str, isjudge: bool):
        self.socket = sock
        self.name = name
        self.isjudge = isjudge


def valid_name(name: str, player_list: list) -> bool:

    # check if name already taken
    for player in player_list:
        if name == player.name:
            return False

    return True


# the number of connections the server will wait for before starting game
num_players = 2

# list of clients
sock_list = list()
player_list = list()


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
        name = clientsocket.recv(1024).decode("utf-8")

        # check if player name has valid characters
        if not name.isalpha():
            clientsocket.send(bytes("Name contains invalid characters", "utf-8"))
            clientsocket.close()

            # return to beginning of loop
            continue

        # check if player name already taken
        if not valid_name(name, player_list):
            clientsocket.send(bytes("Name already taken", "utf-8"))
            clientsocket.close()

            # return to beginning of loop
            continue

        sock_list.append(clientsocket)
        player_list.append(Player(clientsocket, name, False))
        curr_players += 1
        clientsocket.send(bytes("The game will start shortly.", "utf-8"))
        print(f"'{name}' joined the game.")

    # if not new client, this means that an old client is sending a message. print it.
    else:
         msg = active_socket.recv(1024)
         print(msg)

# lets go
(random.choice(player_list)).isjudge = True
for player in player_list:
    print( player.name, player.isjudge, sep =' ' )
for player in player_list:
    if player.isjudge == True:
        print(f"{player.name} is the judge. They will make the first prompt.")
    else:
        continue
print("All players are ready")

