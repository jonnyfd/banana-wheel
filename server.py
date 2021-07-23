# import socket, select, random modules
import socket
import select
import random

class Player():
    """Player Class"""

    def __init__(self, sock: socket.socket, name: str, isjudge: bool):
        # wait forever on calls to recv
        self.socket = sock
        self.name = name
        self.isjudge = isjudge


    def send(self, message: str):
        """Sends a message to a player"""
        self.socket.send(bytes(message, "utf-8"))


    def receive(self) -> str:
        """Receives a message from a player"""
        return self.socket.recv(1024).decode("utf-8")


def broadcast(player_list, message, exclude=None):
    """Sends a message to all players"""
    for player in player_list:
        if player is not exclude:
            player.send(message)


def get_player_with_socket(player_list: list, sock: socket.socket):
    for player in player_list:
        if sock == player.socket:
            return player
    print(f"WHAT THE?? No player with socket number {sock.fileno()} found")
    quit()


def valid_name(name: str, player_list: list) -> bool:
    """Checks if a name has been taken"""
    # check if name already taken
    for player in player_list:
        if name == player.name:
            return False

    return True


# the number of connections the server will wait for before starting game
num_players = 3

# list of clients
sock_list = list()
player_list = list()


# specifies IPv4 over TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", 6699))
s.listen(num_players)
# adds server to list of players
sock_list.append(s)

print("Awaiting players...")

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


def select_judge(player_list):

    # randomly select judge
    judge = random.choice(player_list)

    # reset previous judge
    for player in player_list:
        player.isjudge = False

    # set new judge and return
    judge.isjudge = True
    return judge


# everyone is here, start game
broadcast(player_list, "Game starting...")

# keep track of current round number, for kicks
round_number = 0

while True:

    # 1. select judge
    round_number += 1
    print(f"Starting round {round_number}")

    judge = select_judge(player_list)
    print(f"{judge.name} is the judge")

    # 2. tell everyone who the judge is
    broadcast(player_list, judge.name)

    # 3. have judge submit a new prompt
    prompt = judge.receive()
    print(f"The prompt is:\n{prompt}")

    # 4. broadcast the new prompt
    broadcast(player_list, prompt, exclude=judge)

    # 5. wait for all non-judge players to submit their responses
    responses = []
    waiting = [player.socket for player in player_list if player is not judge]
    while waiting != []:
        active_socket = select.select(
                 waiting, [], []
        )[0][0]
        player = get_player_with_socket(player_list, active_socket)
        curr = player.receive()

        # keep track of number, response, and player
        responses.append((len(waiting), curr, player.name))
        waiting.remove(active_socket)

    # shuffle responses
    random.shuffle(responses)

    # merge all responses into single string that looks like:
    # 1 - "dogs"
    # 2 - "cats"
    # 3 - "birds"
    # etc
    response_str = "\n".join(str(response[0]) + " - " + response[1] for response in responses)

    # 6. display submissions to everyone
    broadcast(player_list, response_str)

    # 7. receive winning number from judge
    winning_number = int(judge.receive())
    winning_name = ""
    for response in responses:
        if winning_number == response[0]:
            winning_name = response[2]

    # 7. announce winner
    print(f"{winning_name} won.")
    broadcast(player_list, winning_name)

    # 8. next round?

