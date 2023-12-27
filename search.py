import chess
import chess.polyglot
import time
from evaluate import *

max_depth = 18
move_points = []
def nextMove(board, color):
    try:
        best_move = chess.polyglot.MemoryMappedReader("books/human.bin").weighted_choice(board).move
    except IndexError:
        best_move = iterativeDeepening(board, color,5)
    return best_move


def iterativeDeepening(board, color, max_time):
    start = time.time()
    for move in board.legal_moves:
        move_points.append((0,move))
    best_move = None
    for i in range(1, max_depth + 1):
        points,best_move = minimax(i, board, float('inf'), -float('inf'), color==board.turn, None, color)
        if time.time() - start >= max_time:
            break
    move_points.clear()
    return best_move



def minimax(depth, board, alpha, beta, maxPlayer, curmove, ai_color):
    if depth == 0:
        for move in board.legal_moves:
            if move == curmove:
                points = quiescence(1, board, alpha, beta, maxPlayer)
        quiescence(1, board, alpha, beta, maxPlayer)

        if eval(board) == (float('inf') or -float('inf')) and board.turn == ai_color:
            print("mate you lose")
            exit(0)
        if eval(board) == (float('inf') or -float('inf')) and board.turn != ai_color:
            print("mate you win")
            exit(0)
        if eval(board) == "draw":
            print("draw")
            exit(0)
        return -eval(board), curmove
    if maxPlayer:
        maxEval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            evalu,_= minimax(depth - 1, board, alpha, beta, False, move, ai_color)
            board.pop()
            maxEval = max(maxEval, evalu)
            alpha = max(alpha, evalu)
            if beta <= alpha:
                break
        return maxEval, curmove
    else:
        minEval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            evalu,_ = minimax(depth - 1, board, alpha, beta, True, move, ai_color)
            board.pop()
            minEval = min(minEval, evalu)
            beta = min(beta, evalu)
            if beta <= alpha:
                break
        return minEval, curmove


def quiescence(depth, board, alpha, beta, maximizingPlayer):
    if depth == 0:
        return -eval(board)
    if maximizingPlayer:
        maxEval = -float('inf')
        for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                evalu = quiescence(depth - 1, board, alpha, beta, False)
                board.pop()
                maxEval = max(maxEval, evalu)
                alpha = max(alpha, evalu)
                if beta <= alpha:
                    break
        return maxEval
    else:
        minEval = float('inf')
        for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                evalu = quiescence(depth - 1, board, alpha, beta, True)
                board.pop()
                minEval = min(minEval, evalu)
                beta = min(beta, evalu)
                if beta <= alpha:
                    break
        return minEval
