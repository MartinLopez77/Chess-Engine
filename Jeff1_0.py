import random
import chess

"""
Toma un movimiento aleatorio entre los posibles
"""

class Jeff1_0:

    # Tablero interno
    def __init__(self, board: chess.Board | None = None):
        self.board = board or chess.Board()

    # Realizar el movimiento del rival
    def update_with_opponent_move(self, move_uci):
        move = self.board.parse_uci(move_uci)
        if move in self.board.legal_moves:
            self.board.push(move)

    # Elige un movimiento 
    def choose_move(self):
        legal_moves = list(self.board.legal_moves)
        if not legal_moves:
            return None
        move = random.choice(legal_moves)
        return move.uci()
