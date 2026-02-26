import random
from utils_2 import *

# Se hace un minimax de profundidad k
def minimax(board, depth, is_maximizing, my_color):
    if depth == 0 or board.is_game_over():
        return score_board_advanced(board, my_color)

    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return score_board_advanced(board, my_color)

    if is_maximizing:
        best = -9999
        for move in legal_moves:
            board.push(move)
            val = minimax(board, depth-1, False, my_color)
            board.pop()
            if val is not None:
                best = max(best, val)
        return best
    else:
        best = 9999
        for move in legal_moves:
            board.push(move)
            val = minimax(board, depth-1, True, my_color)
            board.pop()
            if val is not None:
                best = min(best, val)
        return best

def get_engine_move_Jeff2_0(board, depth=3):
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None

    my_color = board.turn  # Color del motor

    best_value = -9999
    best_moves = []

    for move in legal_moves:
        board.push(move)
        value = minimax(board, depth-1, False, my_color)
        board.pop()

        if value > best_value:
            best_value = value
            best_moves = [move]
        elif value == best_value:
            best_moves.append(move)

    chosen_move = random.choice(best_moves)

    return chosen_move.uci()

