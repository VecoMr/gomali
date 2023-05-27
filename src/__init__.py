from subprocess import Popen, PIPE
from copy import copy
from typing import List
from random import randint

class Player:
    def __init__(self, path):
        self.path = path
        self.process = Popen(path, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        #self.__get_about()

    def set_size(self, size):
        self.process.stdin.write(f'START {size}\n')
        self.process.stdin.flush()
        msg = self.process.stdout.readline().split()
        if msg[0] != 'OK':
            raise Exception(' '.join(msg[1:]))

    def __get_about(self):
        self.process.stdin.write('ABOUT\n')
        self.process.stdin.flush()
        self.name = self.process.stdout.readline().strip()
        self.version = self.process.stdout.readline().strip()
        self.author = self.process.stdout.readline().strip()
        self.country = self.process.stdout.readline().strip()

    def __str__(self):
        return self.path

class Board:
    def __init__(self, load=None, size=20):
        if load:
            try:
                with open(load, 'r') as f:
                    content = f.read().split('\n')
                    self.size = int(content[0])
                    self.board = [list(map(int, line.split())) for line in content[1:]]
            except:
                raise Exception('The file {} is not a valid save file'.format(load))
            if sum([sum([1 for j in i if i not in [0, 1, 2]]) for i in self.board]) != 0:
                raise Exception('The file {} is not a valid save file'.format(load))
        else:
            self.board = [[0 for _ in range(size)] for _ in range(size)]
            self.size = size
        if self.size < 5:
            raise Exception('The size of the board must be greater than 5')

    def __str__(self):
        tmp = '\n'.join([' '.join([str(x) for x in line]) for line in self.board])
        return f"{self.size}\n{tmp}"

    def __getitem__(self, key):
        return self.board[key]

class Game:
    def __init__(self, player1, player2, load=None, size=20, first='random'):
        self.players : List[Player] = []
        if first == 'random':
            first = str(randint(1, 2))
        if first == '1':
            self.players.append(Player(player2))
            self.players.append(Player(player1))
        else:
            self.players.append(Player(player1))
            self.players.append(Player(player2))
        self.board : Board = Board(load=load)
        self.history : List[Board] = []
        self.turn : int = -1
        self.winner = None

    def load_board(self, load):
        self.board = Board(load=load)

    def init_game(self):
        [player.set_size(self.board.size) for player in self.players]

    def play_turn(self):
        self.turn += 1
        player = self.turn % 2
        self.history.append(copy(self.board))
        self.players[player].process.stdin.write(str(self.board))
        self.players[player].process.stdin.flush()
        msg = self.players[player].process.stdout.readline().split()
        if msg[0] != 'OK':
            raise Exception(' '.join(msg[1:]))
        x, y = map(int, msg[1:])
        if self.board[x][y] != 0:
            raise Exception('The move ({}, {}) is not valid'.format(x, y))
        self.board[x][y] = player + 1
        self.winner = self.check_winner()

    def start_game(self):
        self.init_game()
        while not self.winner:
            self.play_turn()
        print(f'Player {self.winner} won')