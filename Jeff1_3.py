import random
from utils import *

class Jeff1_3:

    def __init__(self, depth=3):
        # Cada motor tiene su propio tablero independiente
        self.board = chess.Board()
        self.depth = depth
        self.lines_explored = 0

    # Realizar el movimiento del rival
    def update_with_opponent_move(self, move_uci):
        move = self.board.parse_uci(move_uci)
        if move in self.board.legal_moves:
            self.board.push(move)

    # Minimax clásico
    def minimax(self, board, depth, is_maximizing, root_turn):

        self.lines_explored += 1

        if depth == 0 or board.is_game_over():
            return score_board(board, root_turn)

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return score_board(board, root_turn)

        if is_maximizing:
            best = -9999
            for move in legal_moves:
                board.push(move)
                val = self.minimax(board, depth-1, False, root_turn)
                board.pop()
                best = max(best, val)
            return best
        else:
            best = 9999
            for move in legal_moves:
                board.push(move)
                val = self.minimax(board, depth-1, True, root_turn)
                board.pop()
                best = min(best, val)
            return best

    def choose_move(self, verbose=True):
        """
        Devuelve el mejor movimiento en UCI, sin modificar el tablero interno.
        """
        legal_moves = list(self.board.legal_moves)
        if not legal_moves:
            return None

        self.lines_explored = 0
        root_turn = self.board.turn

        best_value = -9999
        best_moves = []

        for move in legal_moves:
            self.board.push(move)
            value = self.minimax(self.board, self.depth-1, False, root_turn)
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