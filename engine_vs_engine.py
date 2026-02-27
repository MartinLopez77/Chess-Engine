import pygame
import chess
import os
from board_display import draw_board, draw_pieces

from Jeff1_0 import Jeff1_0
from Jeff1_1 import Jeff1_1
from Jeff1_3 import Jeff1_3
from Jeff1_5 import Jeff1_5
from Jeff1_6 import Jeff1_6

# ---------- CONFIG ----------
WIDTH = 640
HEIGHT = 640
SQ_SIZE = WIDTH // 8

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeffrey vs Jeffrey Turn-Based")

# Tenemos un único tablero, asignamos el color a cada motor
board = chess.Board()
engine_white = Jeff1_1(board, chess.WHITE)
engine_black = Jeff1_3(board, chess.BLACK)

last_move = None
game_over = False

# ---------- CARGAR IMÁGENES ----------
pieces = {}
image_folder = "images"
piece_files = {
    "P": "wp.png", "R": "wr.png", "N": "wn.png",
    "B": "wb.png", "Q": "wq.png", "K": "wk.png",
    "p": "bp.png", "r": "br.png", "n": "bn.png",
    "b": "bb.png", "q": "bq.png",
    "k": "bk.png",
}

for symbol, filename in piece_files.items():
    path = os.path.join(image_folder, filename)
    if os.path.exists(path):
        image = pygame.image.load(path)
        pieces[symbol] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))


# ---------- BUCLE PRINCIPAL ----------
running = True
while running:

    # Dibujar tablero y piezas
    draw_board(screen, SQ_SIZE, board, last_move, game_over)
    draw_pieces(screen, SQ_SIZE, board, pieces, None, None, None)
    pygame.display.flip()

    # --- Comprobar eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- Calcular movimiento al presionar espacio ---
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over:

            # motor del turno actual
            engine = engine_white if board.turn == chess.WHITE else engine_black

            # calcular movimiento y ejecutarlo
            move_uci = engine.choose_move()
            if not move_uci:
                print("No hay movimientos legales disponibles.")
                continue

            # Realizar el movimiento
            board.push(chess.Move.from_uci(move_uci))
            # Aquí se puede mostrar el movimiento en consola
            #print(f"Movimiento calculado ({engine.__class__.__name__}): {move_uci}")

            # comprobar fin de partida
            if board.is_game_over():
                game_over = True
                print("Resultado:", board.result())

pygame.quit()