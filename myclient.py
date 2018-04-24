import socket
import json
from myGame import Game


HOST = '127.0.0.1'
PORT = 5000


PLAYER_1 = "PLAYER_1"
PLAYER_2 = "PLAYER_2"

SET_NAME = "SET_NAME"
GET_NAME = "GET_NAME"
WAIT = "WAIT"
START = "START"
PLAY = "PLAY"
UPDATE = "UPDATE"
QUIT = "QUIT"
END = "END"


game = Game()

         
mySocket = socket.socket()
mySocket.connect((HOST, PORT))


while True:
    data = mySocket.recv(2048)

    if not data:
        print("disconnected from server.")
        break

    data = json.loads(data.decode())
    game.cells = data["cells"]

    # print('Received from server:')
    # string = data["message"] + ", player: " + data["player"]
    # print('message: ' + string + ", state: " + data["state"])

    if data["state"] == GET_NAME:
        print("Welcome to Tic-Tac-Toe\n")
        print("  - Please Enter the Player's Name -\n")

        message = str(input(data["player"] + " : "))

        data = {"cells": game.cells, "message": message, "player": data["player"], "state": SET_NAME}
        json_data = json.dumps(data).encode()
        mySocket.send(json_data)

    elif data["state"] == WAIT:
        game.refresh()
        print(data["message"])

    elif data["state"] == START:
        game.refresh()
        if data["player"] == PLAYER_1:
            message = input(data["message"])
            data = {"cells": game.cells, "message": message, "player": data["player"], "state": UPDATE}
        else:
            # starts game for PLAYER_2, print 'waiting your opponent' and wait
            print(data["message"])
            data = {"cells": game.cells, "message": "PLAYER_2: waiting for PLAYER_1 first move.", "player": data["player"], "state": WAIT}

        json_data = json.dumps(data).encode()
        mySocket.send(json_data)

    elif data["state"] == PLAY:
        # update the game
        game.refresh()
        message = input(data["message"])
        data = {"cells": game.cells, "message": message, "player": data["player"], "state": UPDATE}
        json_data = json.dumps(data).encode()
        mySocket.send(json_data)

    elif data["state"] == END:
        choice = ""
        while choice != "Y" and choice != "N":
            game.refresh()
            print(data["message"])
            choice = str(input("Would you like to play again? (Y/N) : "))
            choice = choice.upper()
            print()

        data = {"cells": game.cells, "message": choice, "player": data["player"], "state": END}
        json_data = json.dumps(data).encode()
        mySocket.send(json_data)

    elif data["state"] == "QUIT":
        game.refresh()
        print(data["message"])
        message = data["player"] + " - notifies server that it's quiting."
        data = {"cells": game.cells, "message": message, "player": data["player"], "state": "QUIT"}
        json_data = json.dumps(data).encode()
        mySocket.send(json_data)
        break
    else:
        print("the state is : " + data["state"])
        message = input("input: ")
        data["message"] = data["player"] + " - " + message
        json_data = json.dumps(data).encode()
        mySocket.send(json_data)


mySocket.close()


