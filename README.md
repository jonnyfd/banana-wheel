# Banana Wheel

Banana wheel is a game similar to apples to apples. There are no preset cards. All prompts and answers to said prompts are written by the players.

# How does it work?

Everyone connects to the game server using client.py. After everybody is connected (amount of players is determined in server.py file), the server randomly selects a first player to be the judge.

The judge writes the first prompt and sends it to the server. An example prompt would be something like: "Sorry I'm late, I was __________."

The server takes this prompt and sends it to the rest of the players. All of the players (except for the judge) fill in the blank. The server collects the answers and displays them to all the players (anonymously). Once everybody is done having a good laugh, the judge picks their favorite answer to the prompt. The winner is displayed to everybody, and is the judge of the next round. They also get a point for winning the round.

This goes on until everybody has had their fill. The scoreboard is displayed at the end of the game.

# How do I play?
Because this is a multiplayer game, it uses two programs. Client.py and server.py.
All of the players will need to download and configure client.py, one player (somebody who owns a server) will need to download and configure server.py.

Server.py instructions:
You will need to download python if you don't already have it. https://www.python.org/downloads/
You may need to open a port. The steps will be different depending on what router/OS your server is running. Not gonna put the instructions for that here. If you have a server I assume you know how to do that.

Find the line that says s.bind(("0.0.0.0", 6699)), and change the second number to whatever port you opened on your router.

Find the line that says num players = 2, and change it to the total amount of players you are expecting. The server doesn't count as a player. 

Run python3 server.py in your terminal.

Client.py instructions:
You will need to download python if you don't already have it. https://www.python.org/downloads/

Open up client.py in any texteditor. Notepad works just fine.
Find the line that says: s.connect(('0.0.0.0', 6699)) 
Change the number in quotes to the IP address of the server that server.py is running on. Change the second number to whatever port has been opened on that server.

Open up your command line/terminal, navigate to where you downloaded client.py, and type python3 client.py <yourname>.