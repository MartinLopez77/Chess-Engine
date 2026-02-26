import chess
import random
import time
from utils import *

# ---------------------------------------------------------
# MINIMAX DINÁMICO ULTRA INSTRUMENTADO
# ---------------------------------------------------------

def minimax_with_dynamic_branch(board, depth, is_maximizing,
                                my_color, threshold, stats, current_depth):

    stats["nodes"] += 1
    stats["nodes_per_depth"][current_depth] = \
        stats["nodes_per_depth"].get(current_depth, 0) + 1

    # ------------------ CONDICIONES DE CORTE ------------------

    if board.is_game_over():
        stats["cutoffs"] += 1
        stats["real_cutoffs_terminal"] += 1
        return score_board(board, my_color)

    if depth == 0:
        stats["cutoffs"] += 1
        stats["real_cutoffs_depth"] += 1
        return score_board(board, my_color)

    if threshold == 0:
        stats["cutoffs"] += 1
        stats["real_cutoffs_threshold"] += 1
        return score_board(board, my_color)

    # -----------------------------------------------------------

    legal_moves = list(board.legal_moves)
    movimientos = len(legal_moves)

    if not legal_moves:
        stats["cutoffs"] += 1
        return score_board(board, my_color)

    # Registrar branching
    stats["branching_sum"] += movimientos
    stats["branching_max"] = max(stats["branching_max"], movimientos)

    # Registrar threshold
    stats["threshold_values"].append(threshold)
    stats["threshold_per_depth"][current_depth] = \
        stats["threshold_per_depth"].get(current_depth, []) + [threshold]

    # Calcular siguiente threshold
    next_threshold = threshold // movimientos if movimientos > 0 else 0

    # Registrar profundidad real alcanzada
    stats["max_depth_reached"] = max(
        stats["max_depth_reached"],
        current_depth
    )

    # ------------------ RECURSIÓN ------------------

    if is_maximizing:
        best = -9999
        for move in legal_moves:
            board.push(move)
            val = minimax_with_dynamic_branch(
                board,
                depth-1,
                False,
                my_color,
                next_threshold,
                stats,
                current_depth+1
            )
            board.pop()
            best = max(best, val)
        return best

    else:
        best = 9999
        for move in legal_moves:
            board.push(move)
            val = minimax_with_dynamic_branch(
                board,
                depth-1,
                True,
                my_color,
                next_threshold,
                stats,
                current_depth+1
            )
            board.pop()
            best = min(best, val)
        return best


# ---------------------------------------------------------
# MOTOR PRINCIPAL DINÁMICO
# ---------------------------------------------------------

def get_engine_move_Jeff1_5(board,
                            max_depth=10,
                            threshold=5000,
                            verbose=True):

    my_color = board.turn
    legal_moves = list(board.legal_moves)

    if not legal_moves:
        return None

    movimientos = len(legal_moves)

    stats = {
        "nodes": 0,
        "cutoffs": 0,
        "real_cutoffs_depth": 0,
        "real_cutoffs_threshold": 0,
        "real_cutoffs_terminal": 0,
        "branching_sum": 0,
        "branching_max": 0,
        "nodes_per_depth": {},
        "threshold_per_depth": {},
        "threshold_values": [],
        "max_depth_reached": 0
    }

    start_time = time.time()

    best_score = -9999
    best_moves = []

    for move in legal_moves:

        board.push(move)

        score = minimax_with_dynamic_branch(
            board,
            max_depth - 1,
            False,
            my_color,
            threshold // movimientos if movimientos > 0 else 0,
            stats,
            1
        )

        board.pop()

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    # Elegir aleatoriamente entre los mejores
    best_move = random.choice(best_moves)

    end_time = time.time()

    # ------------------ INFORME ------------------

    if verbose:

        avg_branching = stats["branching_sum"] / stats["nodes"] \
            if stats["nodes"] > 0 else 0

        print("\n===== INFORME MOTOR DINÁMICO =====")
        print(f"Movimiento elegido: {best_move.uci() if best_move else None}")
        print(f"Score final: {best_score}")
        print(f"Tiempo: {round(end_time-start_time,3)} s")

        print("\n--- ÁRBOL ---")
        print(f"Nodos explorados: {stats['nodes']}")
        print(f"Branching medio: {round(avg_branching,2)}")
        print(f"Branching máximo: {stats['branching_max']}")
        print(f"Nodos por profundidad: {stats['nodes_per_depth']}")
        print(f"Profundidad máxima real: {stats['max_depth_reached']}")

        print("\n--- CORTES ---")
        print(f"Cortes totales: {stats['cutoffs']}")
        print(f"Por depth: {stats['real_cutoffs_depth']}")
        print(f"Por threshold: {stats['real_cutoffs_threshold']}")
        print(f"Por terminal: {stats['real_cutoffs_terminal']}")

        if stats["threshold_values"]:
            print("\n--- THRESHOLD ---")
            print(f"Threshold inicial: {threshold}")
            print(f"Threshold mínimo: {min(stats['threshold_values'])}")
            print(f"Threshold medio: "
                  f"{sum(stats['threshold_values']) // len(stats['threshold_values'])}")

        print("==================================\n")

    return best_move.uci() if best_move else None