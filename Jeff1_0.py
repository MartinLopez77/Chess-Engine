import random

"""
Toma un movimiento aleatorio entre los posibles
"""

class Jeff1_0:

    # Tablero interno
    def __init__(self, board):
        self.board = board 

    # Elige un movimiento 
    def choose_move(self):
        legal_moves = list(self.board.legal_moves)
        if not legal_moves:
            return None

        move = random.choice(legal_moves)
        return move.uci()