import random
import chess
from utils import score_move

"""
Toma un movimiento aleatorio entre aquellos que aporten mayor beneficio
"""

class Jeff1_1:

    # Tablero interno
    def __init__(self, board: chess.Board | None = None):
        self.is_internal_board = board is None
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

        puntuaciones_movimiento = [(mov, score_move(self.board, mov)) for mov in legal_moves]
        mejor_puntuacion = max(puntuaciones_movimiento, key=lambda x: x[1])[1]

        mejores_movimientos = [mov for mov, score in puntuaciones_movimiento
            if score == mejor_puntuacion]
        move = random.choice(mejores_movimientos)

        if self.is_internal_board:
            self.board.push(move)

        return move.uci()
