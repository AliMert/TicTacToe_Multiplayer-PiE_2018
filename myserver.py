import socket
import threading
import json
from myGame import Game


HOST = '127.0.0.1'
PORT = 5000

SET_NAME = "SET_NAME"
GET_NAME = "GET_NAME"
WAIT = "WAIT"
START = "START"
PLAY = "PLAY"
UPDATE = "UPDATE"
END = "END"
QUIT = "QUIT"

players = {"PLAYER_1": {}, "PLAYER_2": {}}

PLAYER_1 = "PLAYER_1"
PLAYER_2 = "PLAYER_2"


game = Game()


class ClientThread(threading.Thread):

    def __init__(self, ip, port, client_socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.client_connection = client_socket
        print("[+] New thread started for " + ip + ":" + str(port))

        if not players[PLAYER_1]:
            print("player1 connection is established.")
            players[PLAYER_1].update({"connection": {}})
            players[PLAYER_1]["connection"]["ip"] = self.ip
            players[PLAYER_1]["connection"]["port"] = self.port
            players[PLAYER_1]["connection"]["socket"] = self.client_connection
            players[PLAYER_1]["name"] = "PLAYER_1"
            players[PLAYER_1]["state"] = GET_NAME

        elif not players["PLAYER_2"]:
            print("player2 connection is established.")
            players["PLAYER_2"].update({"connection": {}})
            players["PLAYER_2"]["connection"]["ip"] = self.ip
            players["PLAYER_2"]["connection"]["port"] = self.port
            players["PLAYER_2"]["connection"]["socket"] = self.client_connection
            players[PLAYER_2]["name"] = "PLAYER_2"
            players[PLAYER_1]["state"] = GET_NAME

    def run(self):
        print("Connection from : " + self.ip + ":" + str(PORT))
        message = "Welcome to the server.\n"

        if not players["PLAYER_2"] and players[PLAYER_1]["name"] == PLAYER_1:
            print("sending first request to PLAYER-1")
            send_request(message, PLAYER_1, GET_NAME)

        if players[PLAYER_2] and players[PLAYER_2]["name"] == PLAYER_2:
            print("sending first request to PLAYER-2")
            send_request(message, PLAYER_2, GET_NAME)

        while True:
            data = self.client_connection.recv(2048)

            if not data:
                break

            data = data.decode()
            data = json.loads(data)
            print("Client(%s:%s) sent : %s" % (self.ip, str(self.port), data))

            if data["state"] == SET_NAME:
                player = data["player"]
                players[player]["name"] = data["message"]

                if player == PLAYER_1:
                    # sent player-1 'waiting for your opponent'
                    # then client1 sends back to confirm it then client1 will wait
                    send_request("waiting for your opponent to get ready, please wait...", PLAYER_1, WAIT)

                elif player == PLAYER_2:
                    # now start game by sending both clients START request
                    send_request("please enter a number 1-9: ", PLAYER_1, START)
                    send_request("waiting for your opponent: ", PLAYER_2, START)
                else:
                    print("something went wrong while switching players at ( if data['state'] == SET_NAME )")
                    print("Seems like there is an extra player in the town!!")

            elif data["state"] == UPDATE:
                move = data["message"]
                if not move.isnumeric() or int(move) < 1 or game.cells[int(move) - 1] != " ":
                    send_request("please enter a number 1-9: ", data["player"], PLAY)

                else:
                    # add new move and update both clients
                    update_cells(data["player"], int(move) - 1)

                    if game.is_winner(data["player"]):
                        send_request(players[data["player"]]["name"].upper() + " WON !!", data["player"], END)
                        data["player"] = reverse_players_to_send_request(data["player"])
                        send_request(players[data["player"]]["name"].upper() + " LOST !!", data["player"], END)

                    elif game.is_tie():
                        send_request("TIE GAME !!\n", data["player"], END)
                        data["player"] = reverse_players_to_send_request(data["player"])
                        send_request("TIE GAME !!\n", data["player"], END)

                    else:

                        if players[data["player"]]:
                            data["player"] = reverse_players_to_send_request(data["player"])
                            if players[data["player"]]:
                                data["player"] = reverse_players_to_send_request(data["player"])
                                send_request("waiting for your opponent: ", data["player"], WAIT)  # WAIT
                                data["player"] = reverse_players_to_send_request(data["player"])
                                send_request("please enter a number 1-9: ", data["player"], PLAY)
                            else:
                                game.reset()
                                send_request(players[data["player"]]["name"] + " quited the game.\nwaiting for a new player to join...",
                                             reverse_players_to_send_request(data["player"]), WAIT)  # WAIT
                        else:
                            data["player"] = reverse_players_to_send_request(data["player"])
                            game.reset()
                            send_request(players[data["player"]]["name"] + " quited the game.\nwaiting for a new player to join...",
                                         reverse_players_to_send_request(data["player"]), WAIT)  # WAIT

            elif data["state"] == WAIT:
                print("client send WAIT state to server. message:\n" + data["message"])

            elif data["state"] == END:
                if data["message"] == "Y":
                    if players[PLAYER_1] and players[PLAYER_2]:
                        # reset cells
                        empty_list = [" ", " ", " ", " ", " ", " ", " ", " ", " "]

                        if game.cells != empty_list:

                            if data["player"] == PLAYER_1:
                                send_request("waiting for your opponent's answer to play again or not... ", PLAYER_1, WAIT)
                                game.cells = empty_list
                            else:
                                # player 2 first said yes
                                send_request("waiting for your opponent's answer to play again or not... ", PLAYER_2, START)
                                game.cells = empty_list
                        else:
                            send_request("please enter a number 1-9: ", PLAYER_1, START)
                            send_request("waiting for your opponent: ", PLAYER_2, START)

                elif data["message"] == "N":
                    if players[PLAYER_1]:
                        send_request("Thanks for Playing !! ", PLAYER_1, QUIT)
                    if players[PLAYER_2]:
                        send_request("Thanks for Playing !! ", PLAYER_2, QUIT)

            elif data["state"] == QUIT:
                players[data["player"]] = {}
                print("client send QUIT state to server. message:\n" + data["message"])

        # WHILE ENDED

        # Disconnection of a client could cause this

        game.reset()

        if players[PLAYER_1] and self.port == players[PLAYER_1]["connection"]["port"]:
            if players[PLAYER_2]:
                send_request(players[PLAYER_1]["name"] + " quited the game.\nwaiting for a new player to join...", PLAYER_2, "WAIT")
            print("*\n*\n*\nClient(PLAYER_1) at " + str(self.ip) + ":" + str(self.port) + " disconnected...\n")
            players[PLAYER_1] = {}

        elif players[PLAYER_2] and self.port == players[PLAYER_2]["connection"]["port"]:
            if players[PLAYER_1]:
                send_request(players[PLAYER_2]["name"] + " quited the game.\nwaiting for a new player to join...", PLAYER_1, "WAIT")
            print("Client(PLAYER_2) at " + str(self.ip) + ":" + str(self.port) + " disconnected...\n")
            players[PLAYER_2] = {}


# server function
def send_request(message, player, state):
    data = {"cells": game.cells, "message": message, "player": player, "state": state}
    json_data = json.dumps(data).encode()
    players[player]["connection"]["socket"].send(json_data)


def update_cells(player, index):
    if player == PLAYER_1:
        game.cells[index] = "X"
    elif player == PLAYER_2:
        game.cells[index] = "O"


def reverse_players_to_send_request(player):
    if player == PLAYER_1:
        return PLAYER_2
    elif player == PLAYER_2:
        return PLAYER_1
    else:
        print("something went wrong while reversing players")
        exit(-1)


# MAIN

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

mySocket.bind((HOST, PORT))

while True:
    mySocket.listen(4)
    print("\nListening for incoming connections...")

    (client_connection, (IP, PORT)) = mySocket.accept()

    if players[PLAYER_1] and players["PLAYER_2"]:
        print("connection attempt to server is denied.\n")
        data = {"cells": "cells_array", "message": "This game is for 2 people, connection attempt to server is denied.", "player": "PLAYER_3", "state": "QUIT"}
        client_connection.send(json.dumps(data).encode())
        client_connection.close()
        continue
    else:
        new_thread = ClientThread(IP, PORT, client_connection)
        new_thread.start()
