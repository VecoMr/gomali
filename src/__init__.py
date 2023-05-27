from subprocess import Popen, PIPE
from copy import copy
from typing import List, Union
from random import randint
from enum import Enum

class Actions_type(Enum):
    START = 1
    ABOUT = 2
    TURN = 3
    BEGIN = 4
    BOARD = 5
    END = 6
    RECTSTART = 7
    RECTTURN = 8
    RECTEND = 9
    RECTBOARD = 10

class Actions:
    def __init__(self, name : str, args : List) -> None:
        self.name = name
        self.args = args

    def __str__(self) -> str:
        return f"{self.name} {' '.join([str(x) for x in self.args])}"


class Player:
    def __init__(self, path):
        self.path = path
        self.process = Popen(path, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        self.stdin : List[str] = []
        self.stdout : List[str] = []
        self.stderr : List[str] = []

    def get_action(self, command: str, action: str = None):
        self.process.stdin.write(command)
        self.stdin.append(command)
        self

    def set_size(self, size):
        self.process.stdin.write(f'START {size}\n')
        self.process.stdin.flush()
        msg = self.process.stdout.readline().split()
        if msg[0] != 'OK':
            raise Exception(' '.join(msg[1:]))

    def get_about(self):
        self.process.stdin.write('ABOUT\n')
        self.process.stdin.flush()
        msg = self.process.stdout.readline().split('"')
        self.name = msg[1]
        self.version = msg[3]
        self.author = msg[5]
        self.country = msg[7]

    def __str__(self):
        return self.path

class Board:
    def __init__(self, load=None, x_size=None, y_size=None, size=20):
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
            self.x_size = len(self.board[0])
            self.y_size = len(self.board)
            if self.x_size == self.y_size:
                self.size = self.x_size
            else:
                self.size = None
        else:
            if not x_size:
                self.x_size = size
            else:
                self.x_size = x_size
            if not y_size:
                y_size = size
            else:
                self.y_size = y_size
            self.board = [[0 for _ in range(x_size)] for _ in range(y_size)]
            if x_size != y_size:
                self.size = None
        if self.size < 5 or self.x_size < 5 or self.y_size < 5:
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
        self.board : Board = Board(load=load, size=size)
        self.history : List[Board] = []
        self.turn_history : List[Union[str, List[int]]] = ["BEGIN\n"]
        self.turn : int = 0
        self.winner = None

    def load_board(self, load):
        self.board = Board(load=load)

    def init_game(self):
        [player.set_size(self.board.size) for player in self.players]
        [player.get_about() for player in self.players]

    def check_winner(self):
        for i in range(self.board.size - 4):
            for j in range(self.board.size - 4):
                if self.board[i][j] != 0 and self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] == self.board[i + 3][j + 3] == self.board[i + 4][j + 4]:
                    return self.board[i][j]
        return None
    
    def play_turn(self):
        player = self.turn % 2
        last_turn = self.turn_history[-1]
        

    def start_game(self):
        self.init_game()
        # while not self.winner:
        #     self.play_turn()
        # print(f'Player {self.winner} won')