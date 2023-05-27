from subprocess import Popen, PIPE
from copy import copy
from typing import List

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
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        if load:
            try:
                with open(load, 'r') as f:
                    content = f.read().split('\n')
                    self.size = int(content[0])
                    self.board = [list(map(int, line.split())) for line in content[1:]]
            except:
                raise Exception('The file {} is not a valid save file'.format(load))
            if sum([sum([1 for j in i if i not in [0, 1, 2]]) for i in self.board]) != 0 or self.size < 5:
                raise Exception('The file {} is not a valid save file'.format(load))

    def __str__(self):
        tmp = '\n'.join([' '.join([str(x) for x in line]) for line in self.board])
        return f"{self.size}\n{tmp}"

    def __getitem__(self, key):
        return self.board[key]

class Game:
    def __init__(self, player1, player2, load=None):
        self.players : List[Player] = [Player(player1), Player(player2)]
        self.board : Board = Board(load=load)
        self.history : List[Board] = []
        self.turn : int = 0
        self.winner = None

    def init_game(self):
        [player.set_size(self.board.size) for player in self.players]