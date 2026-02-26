import pygame
import chess
import os
import threading
import time
from board_display import *
from utils import *

from Jeff1_0 import *
from Jeff1_1 import *
from Jeff1_3 import *
from Jeff1_5_stats import *

# ---------- CONFIG ----------
WIDTH = 640
HEIGHT = 640
SQ_SIZE = WIDTH // 8
MOVE_DELAY = 2000  # ms entre movimientos

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeffrey vs Jeffrey Threaded")

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

# ---------- VARIABLES DE TIEMPO Y HILOS ----------
clock = pygame.time.Clock()
move_timer = 0
pending_move = None
calculating = False

# ---------- FUNCIONES DE HILO ----------
def calculate_move(board_copy, engine_function):
    """
    Calcula el movimiento usando un engine en un hilo separado.
    """
    global pending_move, calculating
    start = time.time()
    pending_move = engine_function(board_copy)
    end = time.time()
    print(f"Movimiento calculado ({engine_function.__name__}) en {round(end-start,3)} s")
    calculating = False

# ---------- BUCLE PRINCIPAL ----------
running = True
while running:
    dt = clock.tick(60)

    # Dibujar tablero y piezas
    draw_board(screen, SQ_SIZE, board, last_move, game_over)
    draw_pieces(screen, SQ_SIZE, board, pieces, None, None, None)
    pygame.display.flip()

    # ---------- MOTOR VS MOTOR CON HILO ----------
    if not game_over:
        move_timer += dt

        # Lanzar cálculo si no hay pendiente y no se está calculando
        if not calculating and pending_move is None:
            calculating = True
            board_copy = board.copy(stack=True)  # Copia del tablero
            if board.turn == chess.WHITE:
                engine = get_engine_move_Jeff1_5
            else:
                engine = get_engine_move_Jeff1_5
            threading.Thread(target=calculate_move, args=(board_copy, engine)).start()

        # Ejecutar movimiento si ya pasó el delay y hay movimiento calculado
        if move_timer >= MOVE_DELAY and pending_move:
            move = chess.Move.from_uci(pending_move)
            if move in board.legal_moves:
                board.push(move)
                last_move = move
            pending_move = None
            move_timer = 0

        # Comprobar fin de partida
        if board.is_game_over():
            game_over = True
            print("Resultado:", board.result())

    # ---------- EVENTOS ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()