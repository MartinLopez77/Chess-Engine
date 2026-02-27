import threading
import chess
import time

from Jeff1_0 import Jeff1_0
from Jeff1_1 import Jeff1_1
from Jeff1_3 import Jeff1_3
from Jeff1_5 import Jeff1_5
from Jeff1_6 import Jeff1_6


# ------------------- FUNCIONES AUXILIARES -------------------

def play_game(engine_white_func, engine_black_func, board, verbose=True, max_moves=200):
    move_count = 0
    time_white = 0.0
    time_black = 0.0

    while not board.is_game_over():
        if move_count >= max_moves:
            return "1/2-1/2", time_white, time_black

        if board.turn == chess.WHITE:
            start = time.time()
            move_uci = engine_white_func(board)
            end = time.time()
            time_white += end - start
        else:
            start = time.time()
            move_uci = engine_black_func(board)
            end = time.time()
            time_black += end - start

        if move_uci is None:
            return "1/2-1/2", time_white, time_black

        move = chess.Move.from_uci(move_uci)

        if move in board.legal_moves:
            board.push(move)
            move_count += 1
        else:
            print("Ilegal")
            return "1/2-1/2", time_white, time_black

        if verbose:
            print(board)
            print("--------")


    return board.result(), time_white, time_black


def tournament(engine_class_a, engine_class_b, n_games=10, max_moves=200, stop_flag=None):
    results = {"A_wins": 0, "B_wins": 0, "Draws": 0}
    total_time_a = 0.0
    total_time_b = 0.0

    tournament_start = time.time()

    for i in range(n_games):
        if stop_flag and stop_flag.is_set():
            print("\n--- TORNEO DETENIDO A MITAD ---")
            break

        # Crear nuevas instancias de cada motor para la partida
        board = chess.Board()
        engine_a_instance = engine_class_a(board, chess.WHITE)
        engine_b_instance = engine_class_b(board, chess.BLACK)

        # Wrappers para play_game
        engine_a_func = lambda b, e=engine_a_instance: e.choose_move()
        engine_b_func = lambda b, e=engine_b_instance: e.choose_move()

        # Alternar colores cada partida
        if i % 2 == 0:
            result, time_a, time_b = play_game(engine_a_func, engine_b_func, board, max_moves=max_moves)
        else:
            result, time_b, time_a = play_game(engine_b_func, engine_a_func, board, max_moves=max_moves)

        total_time_a += time_a
        total_time_b += time_b

        # Contabilizar resultados
        if result == "1-0":
            if i % 2 == 0:
                results["A_wins"] += 1
            else:
                results["B_wins"] += 1
        elif result == "0-1":
            if i % 2 == 0:
                results["B_wins"] += 1
            else:
                results["A_wins"] += 1
        else:
            results["Draws"] += 1

        print(f"Partida {i+1}/{n_games} terminada. Resultado: {result} | "
              f"Tiempo A: {round(time_a,3)} s | Tiempo B: {round(time_b,3)} s")

    # Estadísticas finales
    tournament_end = time.time()
    total_time = tournament_end - tournament_start
    avg_time = total_time / max(1,n_games)
    avg_time_a = total_time_a / max(1,n_games)
    avg_time_b = total_time_b / max(1,n_games)

    print("\n--- RESULTADOS FINALES DEL TORNEO ---")
    print(f"A gana: {results['A_wins']}")
    print(f"B gana: {results['B_wins']}")
    print(f"Empates: {results['Draws']}")
    print("\n--- TIEMPO ---")
    print(f"Tiempo total torneo: {round(total_time,3)} s")
    print(f"Tiempo medio por partida: {round(avg_time,3)} s")
    print(f"Tiempo total jugador A: {round(total_time_a,3)} s | Tiempo medio por partida A: {round(avg_time_a,3)} s")
    print(f"Tiempo total jugador B: {round(total_time_b,3)} s | Tiempo medio por partida B: {round(avg_time_b,3)} s")


# ------------------- EJECUCIÓN -------------------
if __name__ == "__main__":
    n_games = 10
    max_moves = 150
    stop_flag = threading.Event()

    try:
        tournament(
            Jeff1_1,   # Motor A
            Jeff1_3,   # Motor B
            n_games=n_games,
            max_moves=max_moves,
            stop_flag=stop_flag
        )
    except KeyboardInterrupt:
        stop_flag.set()
        print("\n--- TORNEO INTERRUMPIDO MANUALMENTE ---")