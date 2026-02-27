from utils import score_board
import random

"""
Reliza un minimax donde la profundidad máxima varía en función de las ramas totales de cada uno de los
nodos. 
"""

class Jeff1_5:

    def __init__(self, board, color, depth=4, threshold=1000):
        self.board = board
        self.depth = depth
        self.color = color
        self.threshold = threshold
        self.stats = {}

    # Reiniciar estadísticas
    def reset_stats(self):
        self.stats = {
            "nodes": 0,
            "cutoffs": 0,
            "real_cutoffs_depth": 0,
            "real_cutoffs_threshold": 0,
            "real_cutoffs_terminal": 0,
            "branching_sum": 0,
            "branching_max": 0,
            "nodes_per_depth": {},
            "max_depth_reached": 0,
            "branches": []
        }

    # Minimax dinámico
    def minimax_with_dynamic_branch(self, board, depth, is_maximizing, my_color, threshold):

        current_depth = self.depth - depth

        self.stats["nodes"] += 1
        self.stats["nodes_per_depth"][current_depth] = \
            self.stats["nodes_per_depth"].get(current_depth, 0) + 1

        # ----------- CORTES -----------

        if board.is_game_over():
            self.stats["cutoffs"] += 1
            self.stats["real_cutoffs_terminal"] += 1
            return score_board(board, self.color)

        if depth == 0:
            self.stats["cutoffs"] += 1
            self.stats["real_cutoffs_depth"] += 1
            return score_board(board, self.color)

        if threshold == 0:
            self.stats["cutoffs"] += 1
            self.stats["real_cutoffs_threshold"] += 1
            return score_board(board, self.color)

        # --------------------------------

        legal_moves = list(board.legal_moves)
        movimientos = len(legal_moves)

        if not legal_moves:
            self.stats["cutoffs"] += 1
            return score_board(board, self.color)

        # Branching stats
        self.stats["branching_sum"] += movimientos
        self.stats["branching_max"] = max(
            self.stats["branching_max"], movimientos
        )

        self.stats["max_depth_reached"] = max(
            self.stats["max_depth_reached"],
            current_depth
        )

        self.stats["branches"].append(movimientos)


        if is_maximizing:
            best = -9999
            for move in legal_moves:
                board.push(move)
                val = self.minimax_with_dynamic_branch(board, depth-1, False, my_color, threshold//movimientos)
                board.pop()
                best = max(best, val)
            return best
        else:
            best = 9999
            for move in legal_moves:
                board.push(move)
                val = self.minimax_with_dynamic_branch(board, depth-1, True, my_color, threshold//movimientos)
                board.pop()
                best = min(best, val)
            return best


    def choose_move(self, verbose=True):

        self.reset_stats()

        my_color = self.color
        legal_moves = list(self.board.legal_moves)
        movimientos = len(legal_moves)

        self.lines_explored = 0

        if not legal_moves:
            return None

        best_score = -9999
        best_moves = []

        for move in legal_moves:
            self.board.push(move)

            score = self.minimax_with_dynamic_branch(
                self.board,
                self.depth-1,
                False,
                my_color,
                self.threshold // movimientos
            )

            self.board.pop()

            if score > best_score:
                best_score = score
                best_moves = [move] 
            elif score == best_score:
                best_moves.append(move)  

        # Elegir aleatoriamente entre los mejores
        best_move = random.choice(best_moves)

        if verbose:

            print("\n===== INFORME JEFF1_5 =====")
            print(f"Movimiento elegido: {best_move.uci()}")
            print(f"Score final: {best_score}")

            print("\n--- ÁRBOL ---")
            print(f"Nodos explorados: {self.stats['nodes']}")

            branches = self.stats["branches"]  
            if branches:  # evita dividir entre 0
                average = sum(branches) / len(branches)
            else:
                average = 0

            print(f"Branching medio: {round(average,2)}")
            print(f"Branching máximo: {self.stats['branching_max']}")
            print(f"Nodos por profundidad: {self.stats['nodes_per_depth']}")

            print("\n--- CORTES ---")
            print(f"Cortes totales: {self.stats['cutoffs']}")
            print(f"Por depth: {self.stats['real_cutoffs_depth']}")
            print(f"Por threshold: {self.stats['real_cutoffs_threshold']}")
            print(f"Por terminal: {self.stats['real_cutoffs_terminal']}")

            print("==================================\n")

        return best_move.uci()