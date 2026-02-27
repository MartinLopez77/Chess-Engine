import random
from utils import *

class Jeff1_3:

    def __init__(self, board, color, depth=3):
        # Cada motor tiene su propio tablero independiente
        self.board = board
        self.depth = depth
        self.color = color
        self.lines_explored = 0

    # Minimax clásico
    def minimax(self, board, depth, is_maximizing):

        self.lines_explored += 1

        if depth == 0 or board.is_game_over():
            return score_board(board, self.color)

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return score_board(board, self.color)

        if is_maximizing:
            best = -9999
            for move in legal_moves:
                board.push(move)
                val = self.minimax(board, depth-1, False)
                board.pop()
                best = max(best, val)
            return best
        else:
            best = 9999
            for move in legal_moves:
                board.push(move)
                val = self.minimax(board, depth-1, True)
                board.pop()
                best = min(best, val)
            return best

    def choose_move(self, verbose=True):

        legal_moves = list(self.board.legal_moves)
        if not legal_moves:
            return None

        self.lines_explored = 0

        best_value = -9999
        best_moves = []

        for move in legal_moves:
            self.board.push(move)
            value = self.minimax(self.board, self.depth-1, False)
            self.board.pop()

            if value > best_value:
                best_value = value
                best_moves = [move]
            elif value == best_value:
                best_moves.append(move)

        chosen_move = random.choice(best_moves)

        if verbose:
            print(f"Jeff1_3. Líneas exploradas: {self.lines_explored}")

        return chosen_move.uci()