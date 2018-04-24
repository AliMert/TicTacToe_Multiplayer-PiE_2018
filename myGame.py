import os

os.system("clear")


class Game:
    def __init__(self):
        self.cells = [" ", " ", " ", " ", " ", " ", " ", " ", " "]

    def display(self):
        print(" %s | %s | %s " % (self.cells[0], self.cells[1], self.cells[2]))
        print("-----------")
        print(" %s | %s | %s " % (self.cells[3], self.cells[4], self.cells[5]))
        print("-----------")
        print(" %s | %s | %s " % (self.cells[6], self.cells[7], self.cells[8]))

    def refresh(self):
        # Clears the screen
        os.system("clear")
        # prints the header
        print("Welcome to Tic-Tac-Toe\n")
        # Shows the board
        self.display()

    def is_winner(self, player):
        move = "X" if player == "PLAYER_1" else "O"
        for x, y, z in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
            if self.cells[x] == self.cells[y] == self.cells[z]:
                if self.cells[x] == move:  # is "X" or "O": # maybe test
                    return True
        return False

    def is_tie(self):
        for cell in self.cells:
            if cell == " ":
                return False
        return True

    def reset(self):
        self.cells = [" ", " ", " ", " ", " ", " ", " ", " ", " "]


