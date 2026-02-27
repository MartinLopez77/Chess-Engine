import random
from utils import score_board


class JeffNode:
    def __init__(self, board, move = None):
        self.board = board.copy()  # copia propia del tablero
        self.children = []         # hijos del nodo
        self.score = None          # score de minimax (Sirve para algo?)
        self.move = move

"""
Guarda los movimientos ya estudiados de un turno a otro, en este caso esto no es de mucha utilidad pues son
pocas las líneas que se guardan, pero podría ser útil en otros casos.
"""

class Jeff1_6:

    def __init__(self, board, color, depth=3):
        self.board = board
        self.root = JeffNode(board)  # Nodo raíz
        self.depth = depth
        self.my_color = color

    # Expansión minimax
    def expand(self, node, depth, is_maximizing):

        if depth == 0 or node.board.is_game_over():
            node.score = score_board(node.board, self.my_color)
            return node.score

        legal_moves = list(node.board.legal_moves)
        if not legal_moves:
            node.score = score_board(node.board, self.my_color)
            return node.score

        best = -999 if is_maximizing else 999

        # Crear hijos si aún no tiene
        if not node.children:
            for move in legal_moves:
                node.board.push(move)
                child = JeffNode(node.board,move)
                node.children.append(child)
                node.board.pop()

        # Expandir recursivamente
        for child in node.children:
            val = self.expand(child, depth - 1, not is_maximizing)
            if is_maximizing:
                best = max(best, val)
            else:
                best = min(best, val)

        node.score = best

        return best

    # Elegir movimiento, se tiene en cuenta lo que se ha guardado previamente
    def choose_move(self):

        # Sincronizar árbol con el tablero real antes de expandir
        matching_child = None
        for child in self.root.children:
            if child.board.fen() == self.board.fen():
                matching_child = child
                break

        if matching_child:
            self.root.children = []  # Eliminamos las otras ramas
            self.root = matching_child
            print(len(self.root.children))  # Permite ver que funcione correctamente
        else:
            # Si no había coincidencia, crear nodo nuevo
            self.root = JeffNode(self.board)


        # Expandir desde raíz
        self.expand(
            self.root,
            self.depth,
            self.root.board.turn == self.my_color  # Esto es lo que puede estar mal
        )

        # Elegir entre los mejores hijos
        best_score = -9999
        best_children = []

        for child in self.root.children:
            if child.score > best_score:
                best_score = child.score
                best_children = [child]
            elif child.score == best_score:
                best_children.append(child)

        chosen = random.choice(best_children)

        # Re-enraizar solo con la rama elegida
        self.root.children = []
        self.root = chosen

        return chosen.move.uci()