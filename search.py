import chess.polyglot
import time
from evaluate import *


max_depth = 18
move_points = []
def nextMove(board: chess.Board, color: chess.Color)->(chess.Move):
    try:
        best_move = chess.polyglot.MemoryMappedReader("books/human.bin").weighted_choice(board).move
        return best_move
    except IndexError:
        best_move = iterativeDeepening(board, color, 5)
    return best_move


def iterativeDeepening(board, color, max_time):
    start = time.time()
    best_move = None
    for i in range(1, max_depth + 1):
        max_points = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            points = minimax(i - 1, board, -float('inf'), float('inf'), color == board.turn, color)
            board.pop()
            if points > max_points:
                max_points = points
                best_move = move
        if time.time() - start >= max_time:
            break
        print(f"iter at depth {i}: {best_move}: {max_points}")

    return best_move
def minimax(depth, board, alpha, beta, curPlayer, ai_color):
    if depth == 0:
        return eval(board)
    if eval(board) == float('inf') or eval(board) == -float('inf'):
        return eval(board)
    maxEval = float('inf') * (1 if curPlayer else -1)
    for move in board.legal_moves:
        board.push(move)
        evalu = minimax(depth - 1, board, alpha, beta, not curPlayer, ai_color)
        board.pop()
        if curPlayer:
            if evalu < maxEval:
                maxEval = evalu

            alpha = max(alpha, evalu)
        else:
            if evalu > maxEval:
                maxEval = evalu

            beta = min(beta, evalu)


        if beta <= alpha:
            break
    return maxEval
def quiescence(depth, board, alpha, beta, currentPlayer):
    if depth == 0:
        return -eval(board)
    if currentPlayer:
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
        if(maxEval==None):
            return eval(board)
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
