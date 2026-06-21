import chess.polyglot
import time
from evaluate import *


max_depth = 18
INF = float('inf')


def nextMove(board: chess.Board, color: chess.Color) -> chess.Move:
    try:
        best_move = chess.polyglot.MemoryMappedReader("books/human.bin").weighted_choice(board).move
        return best_move
    except IndexError:
        best_move = iterativeDeepening(board, color, 5)
    return best_move


def _ordered_moves(board):
    moves = list(board.legal_moves)

    def score(m):
        s = 0
        if board.is_capture(m):
            victim = board.piece_type_at(m.to_square)
            attacker = board.piece_type_at(m.from_square)
            s = 1000 + 10 * (victim or chess.PAWN) - (attacker or chess.PAWN)
        if m.promotion:
            s += 900
        return s

    moves.sort(key=score, reverse=True)
    return moves


def minimax(depth, board, alpha, beta):
    moves = _ordered_moves(board)
    if not moves:
        if board.is_check():
            return -MATE if board.turn == chess.WHITE else MATE
        return 0
    if board.is_insufficient_material():
        return 0
    if depth == 0:
        return static_eval(board)

    if board.turn == chess.WHITE:
        value = -INF
        for move in moves:
            board.push(move)
            value = max(value, minimax(depth - 1, board, alpha, beta))
            board.pop()
            if value > alpha:
                alpha = value
            if alpha >= beta:
                break
        return value
    else:
        value = INF
        for move in moves:
            board.push(move)
            value = min(value, minimax(depth - 1, board, alpha, beta))
            board.pop()
            if value < beta:
                beta = value
            if beta <= alpha:
                break
        return value


def iterativeDeepening(board, color, max_time):
    start = time.time()
    best_move = None
    maximizing = (color == chess.WHITE)
    for depth in range(1, max_depth + 1):
        best_val = -INF if maximizing else INF
        local_best = None
        for move in _ordered_moves(board):
            board.push(move)
            points = minimax(depth - 1, board, -INF, INF)
            board.pop()
            if maximizing:
                if points > best_val:
                    best_val = points
                    local_best = move
            else:
                if points < best_val:
                    best_val = points
                    local_best = move
        if local_best is not None:
            best_move = local_best
        if abs(best_val) >= MATE or time.time() - start >= max_time:
            break
    return best_move
