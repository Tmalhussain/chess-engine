import sys
from search import *
from evaluate import *

class UCIEngine:
    def __init__(self):
        self.board = None

    def process_command(self, command):
        tokens = command.split()

        if tokens[0] == "uci":
            self.uci()
        elif tokens[0] == "isready":
            self.isready()
        elif tokens[0] == "position":
            self.position(tokens[1:])
        elif tokens[0] == "go":
            self.go()
        elif tokens[0] == "quit":
            self.quit()

    def uci(self):
        print("id name MishoBot")
        print("id author Mishari")
        print("uciok")

    def isready(self):
        print("readyok")

    def position(self, tokens):
        if tokens[0] == "startpos":
            self.board = chess.Board()
            if len(tokens) > 1 and tokens[1] == "moves":
                for move in tokens[2:]:
                    self.board.push(chess.Move.from_uci(move))
        elif tokens[0] == "fen":
            fen = " ".join(tokens[1:7])
            self.board = chess.Board(fen)
            if len(tokens) > 7 and tokens[7] == "moves":
                for move in tokens[8:]:
                    self.board.push(chess.Move.from_uci(move))
        else:
            print("Error: unknown position command")

    def go(self):

        move = nextMove(self.board, ai_color)
        print(f"bestmove {move}")

    def quit(self):
        sys.exit()

if __name__ == "__main__":
    engine = UCIEngine()

    while True:
        command = input()
        engine.process_command(command)
