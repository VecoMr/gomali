import argparse
import os

from src.__init__ import Game

def main():
    parser = argparse.ArgumentParser(description='Gomali: A simple Gomoku manager in python')
    parser.add_argument('-p1', '--player1', help='the path to the ia for the player 1', required=True)
    parser.add_argument('-p2', '--player2', help='the path to the ia for the player 2', required=True)
    parser.add_argument('-s', '--size', help='the size of the board', default=20, type=int)
    parser.add_argument('-l','--load', help='load a game from a file', default=None)
    args = parser.parse_args()

    if not os.path.isfile(args.player1):
        print('The file {} does not exist'.format(args.player1))
        exit(1)
    if not os.path.isfile(args.player2):
        print('The file {} does not exist'.format(args.player2))
        exit(1)
    if args.load and not os.path.isfile(args.load):
        print('The file {} does not exist'.format(args.load))
        exit(1)
    if args.size < 5:
        print('The size of the board must be greater than 5')
        exit(1)

    game = Game(args.player1, args.player2)
    game.init_game()


if __name__ == '__main__':
    main()
