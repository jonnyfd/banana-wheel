# import socket, select, random modules
import socket
import select
import random

class Player():

    def __init__(self, sock: socket.socket, name: str, isjudge: bool):
        self.socket = sock
        self.name = name
        self.isjudge = isjudge

    def send(self, message: str):
        self.socket.send(bytes(message, "utf-8"))

    def broadcast(self, player_list, message):
        for player in player_list:
            player.send(message)

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


def select_judge(player_list):

    # randomly select judge
    judge = random.choice(player_list)
    
    # reset previous judge
    for player in player_list:
        player.isjudge = False

    # set new judge and return
    judge.isjudge = True
    return judge


# keep track of current round number, for kicks
round_number = 0

while round_number == 0:

    # 1. select judge
    round_number += 1
    judge = select_judge(player_list)

    # lets go
    for player in player_list:
        print( player.name, player.isjudge, sep =' ' )
    for player in player_list:
        if player.isjudge == True:
            print(f"{player.name} is the judge. They will make the first prompt.")
        else:
            continue
    print("All players are ready")

    # 2. tell everyone who the judge is
    Player.broadcast(player, player_list, str(judge.name) + " is the judge. They will make the first prompt")

    # 3. have judge submit a new prompt
    for player in player_list:
        if player.isjudge == True:
            player.send("...")
            active_socket = player
        else: 
            continue
    # how do we know where the "blanks" are?
    # could treat '_' as the blanks

    # 4. broadcast the new prompt
    
    prompt = active_socket.socket.recv(1024) 
    print(f"{prompt.decode()}")   


    for player in player_list:
        if player.isjudge == False:
            player.socket.send(prompt)
        else: 
            continue

    # 5. wait for all non-judge players to submit their responses

    # 6. broadcast when all submissions have been received

    # 7. display submissions to judge, have judge select

    # 8. announce winner

    # 9. next round?

