import chess
import chess.engine
import chess.polyglot
import chess.pgn
import chess.svg
from search import *
from evaluate import *
import chess.syzygy
import os

player=input("Enter the color you want to play as (w/b): ")
if player=='w':
    ai_color=chess.BLACK
else:
    ai_color=chess.WHITE
board=chess.Board()
while board.legal_moves.count()>0:
    
    if board.turn==ai_color:
        result=nextMove(board,ai_color)
        board.push(result)
        print(f"AI move: {result}")
        print(board)
    else:
        move=input("Enter your move: ")
        os.system('clear')
        while True:
            try:
                move=board.parse_san(move)
                uci = move.uci()
                break
            except chess.InvalidMoveError:
                print("Invalid move")
                move=input("Enter your move: ")
            except chess.IllegalMoveError:
                print("Illegal move")
                move=input("Enter your move: ")
        board.push(move)
        print(board)
Evaluation = eval(board)
if Evaluation == (float('inf') or -float('inf')) and board.turn == ai_color:
    print("mate you lose")
elif Evaluation == (float('inf') or -float('inf')) and board.turn != ai_color:
    print("mate you win")

else:
    print("draw")
