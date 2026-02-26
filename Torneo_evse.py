import threading
import chess
import random
import time

from Jeff1_0 import *
from Jeff1_1 import *
from Jeff1_2 import *
from Jeff1_3 import *
from Jeff1_4 import *
from Jeff1_5 import *
from Jeff2_0 import *


# ------------------- JUGAR UNA PARTIDA -------------------

def play_game(engine_white, engine_black, verbose=False, max_moves=200):
    board = chess.Board()
    move_count = 0
    time_white = 0.0
    time_black = 0.0

    while not board.is_game_over():

        if move_count >= max_moves:
            return "1/2-1/2", time_white, time_black

        if board.turn == chess.WHITE:
            start = time.time()
            move_uci = engine_white(board)
            end = time.time()
            time_white += end - start
        else:
            start = time.time()
            move_uci = engine_black(board)
            end = time.time()
            time_black += end - start

        if move_uci is None:
            return "1/2-1/2", time_white, time_black

        move = chess.Move.from_uci(move_uci)

        if move in board.legal_moves:
            board.push(move)
            move_count += 1
        else:
            return "1/2-1/2", time_white, time_black

        if verbose:
            print(board)
            print("--------")

    return board.result(), time_white, time_black

# Modificar torneo para permitir interrupción
def tournament(engine_a, engine_b, n_games=10, max_moves=200, stop_flag=None):
    results = {"A_wins": 0, "B_wins": 0, "Draws": 0}
    total_time_a = 0.0
    total_time_b = 0.0

    tournament_start = time.time()

    for i in range(n_games):

        # Comprobar si hay flag de parada
        if stop_flag and stop_flag.is_set():
            print("\n--- TORNEO DETENIDO A MITAD ---")
            break

        game_start = time.time()

        if i % 2 == 0:
            result, time_a, time_b = play_game(engine_a, engine_b, max_moves=max_moves)
        else:
            result, time_b, time_a = play_game(engine_b, engine_a, max_moves=max_moves)

        total_time_a += time_a
        total_time_b += time_b

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

        game_end = time.time()
        print(f"Partida {i+1}/{n_games} terminada. Resultado: {result} | "
              f"Tiempo total partida: {round(game_end - game_start, 3)} s | "
              f"Tiempo A: {round(time_a,3)} s | Tiempo B: {round(time_b,3)} s")

    tournament_end = time.time()
    total_time = tournament_end - tournament_start
    avg_time = total_time / max(1,i+1)
    avg_time_a = total_time_a / max(1,i+1)
    avg_time_b = total_time_b / max(1,i+1)

    print("\n--- RESULTADOS FINALES DEL TORNEO ---")
    print(f"A gana: {results['A_wins']}")
    print(f"B gana: {results['B_wins']}")
    print(f"Empates: {results['Draws']}")
    print("\n--- TIEMPO ---")
    print(f"Tiempo total torneo: {round(total_time, 3)} s")
    print(f"Tiempo medio por partida: {round(avg_time, 3)} s")
    print(f"Tiempo total jugador A: {round(total_time_a, 3)} s | Tiempo medio por partida A: {round(avg_time_a,3)} s")
    print(f"Tiempo total jugador B: {round(total_time_b, 3)} s | Tiempo medio por partida B: {round(avg_time_b,3)} s")


# ------------------- EJECUCIÓN -------------------
if __name__ == "__main__":

    n_games = 10
    max_moves = 150

    # Creamos un flag que puede parar el torneo
    stop_flag = threading.Event()

    try:
        tournament(
            get_engine_move_Jeff1_3,
            get_engine_move_Jeff2_0,
            n_games=n_games,
            max_moves=max_moves,
            stop_flag=stop_flag
        )
    except KeyboardInterrupt:
        stop_flag.set()
        print("\n--- TORNEO INTERRUMPIDO MANUALMENTE ---")