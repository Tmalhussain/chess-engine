import chess
import chess.polyglot
import time
from evaluate import *

max_depth = 18


def nextMove(board, color, max_time):
    try:
        best_move = chess.polyglot.MemoryMappedReader("books/human.bin").weighted_choice(board).move
        return best_move
    except IndexError:
        best_move = iterativeDeepening(board, color, max_time)
        return best_move


def iterativeDeepening(board, color, max_time):
    move_points = []
    start = time.time()
    for i in range(1, max_depth + 1):
        move_points = minimax(i, board, -9999, 9999, True, None, move_points)
        move_points = orderMoves(move_points)
        if time.time() - start > max_time:
            break
    return move_points[0][1]


def orderMoves(move_points):
    move_points.sort(reverse=True)
    return move_points


def minimax(depth, board, alpha, beta, maxPlayer, curmove, move_points):
    if depth == 0:
        move_points.append((-eval(board), curmove))
        if eval(board) == float('inf'):
            print("mate you lose")
            exit(0)
        if eval(board) == -float('inf'):
            print("mate you win")
            exit(0)
        if eval(board) == "draw":
            print("draw")
            exit(0)
        return -eval(board), move_points
    if maxPlayer:
        maxEval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            evalu, move_points = minimax(depth - 1, board, alpha, beta, False, move)
            board.pop()
            maxEval = max(maxEval, evalu)
            alpha = max(alpha, evalu)
            if beta <= alpha:
                break
        return maxEval, move_points
    else:
        minEval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            evalu, move_points = minimax(depth - 1, board, alpha, beta, True, move)
            board.pop()
            minEval = min(minEval, evalu)
            beta = min(beta, evalu)
            if beta <= alpha:
                break
        return minEval, move_points


def quiescence(depth, board, alpha, beta, maximizingPlayer):
    if depth == 0:
        return -eval(board)
    if maximizingPlayer:
        maxEval = -9999
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
        minEval = 9999
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
