import chess
import chess.engine
import chess.polyglot
import chess.pgn
import chess.svg
from search import *
import chess.syzygy

player=input("Enter the color you want to play as (w/b): ")
if player=='w':
    ai_color=chess.BLACK
else:
    ai_color=chess.WHITE
board=chess.Board()

while board.legal_moves.count()>0:
    if board.turn==ai_color:
        result=nextMove(board,ai_color,0.1)
        board.push(result)
        print(board)
    else:
        move=input("Enter your move: ")
        while move not in board.legal_moves:
            print("Invalid move")
            move=input("Enter your move: ")
        board.push_san(move)
        print(board)