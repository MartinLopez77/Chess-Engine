import pygame
import chess
import os
import threading
import time
from board_display import *
from utils import *

from Jeff1_0 import *
from Jeff1_1 import *
from Jeff1_2 import *
from Jeff1_3 import *
from Jeff1_4 import *
from Jeff1_5_stats import *
from Jeff2_0 import *

# ---------- CONFIG ----------
WIDTH = 640
HEIGHT = 640
SQ_SIZE = WIDTH // 8

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeffrey vs Jeffrey - Manual Step")

board = chess.Board()
last_move = None
game_over = False

# ---------- CARGAR IMÁGENES ----------
pieces = {}
image_folder = "images"
piece_files = {
    "P": "wp.png", "R": "wr.png", "N": "wn.png",
    "B": "wb.png", "Q": "wq.png", "K": "wk.png",
    "p": "bp.png", "r": "br.png", "n": "bn.png",
    "b": "bb.png", "q": "bq.png", "k": "bk.png",
}

for symbol, filename in piece_files.items():
    path = os.path.join(image_folder, filename)
    if os.path.exists(path):
        image = pygame.image.load(path)
        pieces[symbol] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))

# ---------- VARIABLES DE HILO ----------
pending_move = None
calculating = False


# ---------- FUNCIÓN DE HILO ----------
def calculate_move(board_copy, engine_function):
    global pending_move, calculating
    start = time.time()
    pending_move = engine_function(board_copy)
    end = time.time()
    print(f"Movimiento calculado ({engine_function.__name__}) en {round(end-start,3)} s")
    calculating = False


# ---------- BUCLE PRINCIPAL ----------
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    # Dibujar tablero
    draw_board(screen, SQ_SIZE, board, last_move, game_over)
    draw_pieces(screen, SQ_SIZE, board, pieces, None, None, None)
    pygame.display.flip()

    # Si el hilo ya terminó, aplicar movimiento
    if pending_move and not calculating and not game_over:
        move = chess.Move.from_uci(pending_move)
        if move in board.legal_moves:
            board.push(move)
            last_move = move
        pending_move = None

        if board.is_game_over():
            game_over = True
            print("Resultado:", board.result())

    # ---------- EVENTOS ----------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # 👇 AQUÍ ESTÁ LA MODIFICACIÓN CLAVE
        if event.type == pygame.KEYDOWN:

            # Pulsar ESPACIO para que juegue el motor
            if event.key == pygame.K_SPACE and not calculating and not game_over:

                calculating = True
                board_copy = board.copy(stack=True)

                if board.turn == chess.WHITE:
                    engine = get_engine_move_Jeff1_3
                else:
                    engine = get_engine_move_Jeff2_0

                threading.Thread(
                    target=calculate_move,
                    args=(board_copy, engine),
                    daemon=True
                ).start()

pygame.quit()