from subprocess import Popen, PIPE
from copy import copy
from typing import List, Union
from random import shuffle
from enum import Enum
from time import sleep, time
from re import match
import selectors


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
    OK = 11
    ERROR = 12
    TAKEBACK = 13
    RESTART = 14
    PLAY = 15
    UNKNOW = 16
    DEBUG = 17
    SUGGEST = 18

class Actions:
    def __init__(self, name : str, args : List) -> None:
        self.type = Actions_type[name]
        self.name = name
        self.args = args

    def __str__(self) -> str:
        return f"{self.name} {' '.join([str(x) for x in self.args])}"


class Player:
    def __init__(self, path):
        self.path = path
        self.process = Popen(path, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
        self.stdin : List[Actions] = []
        self.stdout : List[str] = []
        self.stderr : List[str] = []

    def get_action(self, command: str, need_response : bool = True, action: str = None, timeout : int = 1) -> str:
        print(f'GET action {command}')
        self.process.stdin.write(command)
        self.stdin.append(command)
        self.process.stdin.flush()

        output = ""
        if need_response:
            selector = selectors.DefaultSelector()
            selector.register(self.process.stdout, selectors.EVENT_READ)
            start_time = time()

            while True:
                elapsed_time = time() - start_time
                if elapsed_time >= timeout:
                    break
                events = selector.select(timeout - elapsed_time)
                if events:
                    for key, _ in events:
                        if key.fileobj is self.process.stdout:
                            line = self.process.stdout.readline()
                            if line == "":
                                break
                            else:
                                output += line
                else:
                    elapsed_time = time() - start_time
                    if elapsed_time >= timeout:
                        break
        print("output", output)
        return output

    def set_size(self, size):
        msg = self.get_action(f"START {size}\n")
        print("GET SIZE = ", msg)

    def get_about(self):
        msg = self.get_action('ABOUT\n').split('"')
        print("GET ABOUT = ", msg)

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
            if x_size == None:
                self.x_size = size
            else:
                self.x_size = x_size
            if y_size == None:
                self.y_size = size
            else:
                self.y_size = y_size
            self.board = [[0 for _ in range(self.x_size)] for _ in range(self.y_size)]
            if self.x_size != self.y_size:
                self.size = max(self.x_size, self.y_size)
            else:
                self.size = x_size
            if not self.size:
                self.size = max(self.x_size, self.y_size)
        if self.size < 5 or self.x_size < 5 or self.y_size < 5:
            raise Exception('The size of the board must be greater than 5')

    def __str__(self):
        tmp = '\n'.join([' '.join([str(x) for x in line]) for line in self.board])
        return f"{self.size}\n{tmp}"

    def __getitem__(self, key):
        return self.board[key]

class Game:
    def __init__(self, player1, player2, load=None, size=20, first='random'):
        self.players : List[Player] = [Player(player1), Player(player2)]
        if first == 'random':
            shuffle(self.players)
        if first == '2':
            self.players = self.players[::-1]
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
        pass

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
        while not self.winner:
            self.play_turn()
        print(f'Player {self.winner} won')