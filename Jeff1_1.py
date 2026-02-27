import random
from utils import score_board

"""
Toma un movimiento aleatorio entre los que aportan un mayor beneficio inmediato
"""

class Jeff1_1:

    def __init__(self, board, color):
        self.board = board
        self.color = color 

    def choose_move(self):
        legal_moves = list(self.board.legal_moves)

        if not legal_moves:
            return None

        puntuaciones_movimiento = []

        for mov in legal_moves:
            self.board.push(mov)  
            score = score_board(self.board, self.color)  # Toma el valor del tablero entero
            self.board.pop()    

            puntuaciones_movimiento.append((mov, score))

        mejor_puntuacion = max(puntuaciones_movimiento, key=lambda x: x[1])[1]

        mejores_movimientos = [
            mov for mov, score in puntuaciones_movimiento
            if score == mejor_puntuacion
        ]

        move = random.choice(mejores_movimientos)

        return move.uci()