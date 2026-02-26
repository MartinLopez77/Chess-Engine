import pygame
import chess
from board_display import *
from utils import *
import os
from Jeff1_0 import *
from Jeff1_1 import *
from Jeff1_2 import *
from Jeff1_3 import *
from Jeff1_5_stats import *

# ---------- CONFIG ----------
WIDTH = 640
HEIGHT = 640
SQ_SIZE = WIDTH // 8
RESPONSE_DELAY = 500

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pelea brutal contra Jeffrey")

board = chess.Board()   # Crea un objeto tablero desde 0
selected_square = None
last_move = None
dragging_piece = None
game_over = False      # Mira si se ha acabado la partida actual

# ---------- CARGAR IMÁGENES ----------
pieces = {}
image_folder = "images"
piece_files = {
    "P": "wp.png", "R": "wr.png", "N": "wn.png",
    "B": "wb.png", "Q": "wq.png", "K": "wk.png",
    "p": "bp.png", "r": "br.png", "n": "bn.png",
    "b": "bb.png", "q": "bq.png", "k": "bk.png",
}

# Asocia a cada pieza una imagen
for symbol, filename in piece_files.items():
    path = os.path.join(image_folder, filename)
    if os.path.exists(path):
        image = pygame.image.load(path)
        pieces[symbol] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))

# ---------- VARIABLES ----------
clock = pygame.time.Clock()
pending_response = None      # Este es el movimiento con el que replica el engine, cambiar para el caso de que empiecen las negras
response_timer = 0

# ---------- BUCLE PRINCIPAL ----------
running = True

while running:
    dt = clock.tick(60)

    draw_board(screen, SQ_SIZE, board, last_move, game_over)

    if not game_over:
        draw_move_dots(screen, SQ_SIZE, board, selected_square)

    # Dibuja las piezas en el tablero y las que se están moviendo al ser arrastradas
    draw_pieces(screen, SQ_SIZE, board, pieces, dragging_piece, selected_square,
        pygame.mouse.get_pos() if not game_over else None)

    # Aquí se podría poner un mensaje final
    if board.is_game_over() and not game_over:
        game_over = True

        if board.is_checkmate():
            # El turno actual es el jugador que está en mate
            losing_king_square = board.king(board.turn)

    # Actualiza la ventana de juego con los últimos cambios
    pygame.display.flip()

    # ---------- RESPUESTA AUTOMÁTICA ----------
    if pending_response and not game_over:
        response_timer += dt
        if response_timer >= RESPONSE_DELAY:
            move = chess.Move.from_uci(pending_response)

            if move in board.legal_moves:
                board.push(move)
                last_move = move

            pending_response = None
            response_timer = 0

    # ---------- EVENTOS ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            continue

        elif event.type == pygame.MOUSEBUTTONDOWN:
            square = get_square_from_mouse(event.pos, SQ_SIZE)
            piece = board.piece_at(square)

            if piece and piece.color == board.turn:
                selected_square = square
                dragging_piece = piece

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_piece:
                square = get_square_from_mouse(event.pos, SQ_SIZE)
                move = chess.Move(selected_square, square)

                # Promoción automática
                if board.piece_at(selected_square).piece_type == chess.PAWN:
                    if chess.square_rank(square) == 7:
                        move.promotion = chess.QUEEN

                move_uci = move.uci()

                if move in board.legal_moves:
                    board.push(move)
                    last_move = move

                    response_uci = get_engine_move_Jeff1_5(board)
                    if response_uci:
                        pending_response = response_uci
                        response_timer = 0


                dragging_piece = None
                selected_square = None

pygame.quit()
