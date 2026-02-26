from utils import *
import random

def minimax_with_dynamic_branch(board, depth, is_maximizing, my_color, threshold):

    if depth == 0 or board.is_game_over() or threshold==0:
        return score_board(board, my_color)

    legal_moves = list(board.legal_moves)
    movimientos = len(legal_moves)

    if not legal_moves:
        return score_board(board, my_color)

    if is_maximizing:
        best = -9999
        for move in legal_moves:
            board.push(move)
            val = minimax_with_dynamic_branch(board, depth-1, False, my_color, threshold//movimientos)
            board.pop()
            best = max(best, val)
        return best
    else:
        best = 9999
        for move in legal_moves:
            board.push(move)
            val = minimax_with_dynamic_branch(board, depth-1, True, my_color, threshold//movimientos)
            board.pop()
            best = min(best, val)
        return best


def get_engine_move_Jeff1_5(board, max_depth=5, threshold=1000):
    my_color = board.turn
    legal_moves = list(board.legal_moves)
    movimientos = len(legal_moves)

    if not legal_moves:
        return None

    best_score = -9999
    best_moves = []

    for move in legal_moves:
        board.push(move)

        score = minimax_with_dynamic_branch(
            board,
            max_depth-1,
            False,
            my_color,
            threshold // movimientos
        )

        board.pop()

        if score > best_score:
            best_score = score
            best_moves = [move]  # nueva lista con este movimiento
        elif score == best_score:
            best_moves.append(move)  # añadimos empate

    # Elegir aleatoriamente entre los mejores
    best_move = random.choice(best_moves)

    return best_move.uci()