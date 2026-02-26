import chess
import random
from utils import score_board


# ==========================================================
# NODO DEL ÁRBOL
# ==========================================================
class JeffNode:
    def __init__(self, board, move=None):
        self.board = board.copy()  # copia propia del tablero
        self.move = move           # movimiento que llevó a este nodo
        self.children = []         # hijos del nodo
        self.score = None          # score de minimax
        self.expanded_depth = 0    # hasta qué profundidad se expandió


# ==========================================================
# MOTOR JEFF 1.6
# ==========================================================
class Jeff1_6:

    def __init__(self, initial_board, initial_depth=2):
        self.root = JeffNode(initial_board)
        self.current_depth = initial_depth
        self.my_color = initial_board.turn

    # ------------------------------------------------------
    # ACTUALIZAR ÁRBOL SEGÚN MOVIMIENTO DEL RIVAL
    # ------------------------------------------------------
    def update_with_opponent_move(self, move_uci):
        """
        move_uci: string UCI del movimiento del rival
        """

        move_obj = self.root.board.parse_uci(move_uci)

        # Buscar en hijos
        chosen_child = None
        for child in self.root.children:
            if child.move == move_obj:
                chosen_child = child
                break

        if chosen_child:
            # Solo quedarnos con la rama del rival
            self.root.children = []
            self.root = chosen_child
            return

        # Si no estaba en hijos, crear nodo nuevo
        new_board = self.root.board.copy()
        new_board.push(move_obj)
        self.root.children = []
        self.root = JeffNode(new_board, move=move_obj)

    # ------------------------------------------------------
    # EXPANSIÓN MINIMAX
    # ------------------------------------------------------
    def expand(self, node, depth, is_maximizing):

        if depth == 0 or node.board.is_game_over():
            node.score = score_board(node.board, self.my_color)
            return node.score

        # Evitar expandir más de lo necesario
        if node.expanded_depth >= depth:
            return node.score

        legal_moves = list(node.board.legal_moves)
        if not legal_moves:
            node.score = score_board(node.board, self.my_color)
            return node.score

        best = -999999 if is_maximizing else 999999

        # Crear hijos si aún no tiene
        if not node.children:
            for move in legal_moves:
                new_board = node.board.copy()
                new_board.push(move)
                child = JeffNode(board=new_board, move=move)
                node.children.append(child)

        # Expandir recursivamente
        for child in node.children:
            val = self.expand(child, depth - 1, not is_maximizing)
            if is_maximizing:
                best = max(best, val)
            else:
                best = min(best, val)

        node.score = best
        node.expanded_depth = depth

        return best

    # ------------------------------------------------------
    # ELEGIR MOVIMIENTO
    # ------------------------------------------------------
    def choose_move(self):
        """
        Devuelve movimiento en UCI
        """

        # Aumentar profundidad progresivamente
        self.current_depth += 1

        # Expandir desde raíz
        self.expand(
            self.root,
            self.current_depth,
            self.root.board.turn == self.my_color
        )

        # Elegir entre los mejores hijos
        best_score = -999999
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