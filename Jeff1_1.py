import random
from utils import score_move

"""
Toma un movimiento aleatorio entre aquellos que aporten mayor beneficio
"""

class Jeff1_1:

    # Tablero interno
    def __init__(self, board):
        self.board = board 

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

        return move.uci()