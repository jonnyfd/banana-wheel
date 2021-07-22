# Import socket module 
import socket             
import sys


def get_valid_winning_numbers(response_str):
    """Grabs valid numbers from prompt response string"""
    responses = response_str.split("\n")
    numbers = []
    for response in responses:
        numbers.append(int(response[0]))
    return numbers


# get player name
name = str(sys.argv[1])

# Create a socket object 
s = socket.socket()         
 
# connect to the server on local computer 
s.connect(('0.0.0.0', 6699)) 

# try connect to server
s.send(bytes(name, "utf-8"))
response = s.recv(1024).decode("utf-8")
print(response)

# check for error
if response != "The game will start shortly.":
    quit()

# connection succeeded, wait for game to start
#status = s.recv(1024).decode("utf-8")
#print(status)
#if status != "Game starting...":
 #   quit()

round_number = 0
wins = 0
while True:

    round_number += 1
    print(f"Starting round {round_number}")

    judge = s.recv(1024).decode("utf-8")
    print(f"The judge for this round is: {judge}")

    if name == judge:
        prompt = ""
        while "_" not in prompt:
            prompt = input("Enter prompt, make sure to include a '_': \n")

        print("Sending prompt to server...")
        s.send(bytes(prompt, "utf-8"))

        # receive all prompt responses from server
        print("Waiting for responses to come in...")
        responses = s.recv(1024)
        print(f"The responses are:\n{responses}")

        # client submits winning response number
        valid_numbers = get_valid_winning_numbers(responses)
        winner = 0
        while winner not in valid_numbers:
            try:
                winner = int(input("Who is the winner? "))
            except Exception:
                pass
            if winner not in valid_numbers:
                print("Invalid, try again")

        # send number to server
        s.send(bytes(str(winner), "utf-8"))

        # round over
        winner_name = s.recv(1024).decode("utf-8")
        print(f"The winner is: {winner_name}!")

    else:
        print("Awaiting prompt from judge...")
        prompt = s.recv(1024).decode("utf-8")
        print(f"Prompt:\n{prompt}")

        response = input("What is your response?")
        s.send(bytes(response, "utf-8"))

        print("Waiting for responses to come in...")
        responses = s.recv(1024)
        print(f"The responses are:\n{responses}")

        print("Awaiting judgement...")
        winner = s.recv(1024).decode("utf-8")

        if winner == name:
            print("You won!")
            wins += 1
        else:
            print(f"Son of a... {winner} won.")

