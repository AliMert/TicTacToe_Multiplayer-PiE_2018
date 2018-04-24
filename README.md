# PiTE - Tic Tac Toe Client Server

 This project is an enhanced version of the previous homework which consists to create a client-server Tic Tac Toe with two players.
 Actually, this project is running on localhost, it can be changed easily to run it on a server

# Prerequisites

    - Python 3

    - sudo apt-get install python3


# Must to do

Start on your server the python script called myserver.py

```
python3 myserver.py
```

```
Listening for incoming connections...
[+] New thread started for 127.0.0.1:53539
player1 connection is established.
Connection from : 127.0.0.1:53539

Listening for incoming connections...
sending first request to PLAYER-1

[+] New thread started for 127.0.0.1:53540
player2 connection is established.
Connection from : 127.0.0.1:53540
sending first request to PLAYER-2

Listening for incoming connections...
```

 Every player should run the script called myclient.py **(the server accpets only two players, it denied all requests from more players)**

```
python3 myclient.py
```

 When the server has two players connected, the game starts

# How to play

* Enter your player's name and wait until the other player is ready
```
Welcome to Tic-Tac-Toe

  - Please Enter the Player's Name -

PLAYER_1/2 : *your_name*

```
* Then the game is started and you can enter the number of the case to play

```
Welcome to Tic-Tac-Toe

   |   |
-----------
   |   |
-----------
   |   |
please enter a number 1-9:
```


## Project made by **Ali Bert** and **Alexis OUKSEL**