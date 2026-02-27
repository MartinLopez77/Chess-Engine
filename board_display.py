import pygame
import chess

# ---------- CONFIG ----------
WIDTH = 640
HEIGHT = 640
SQ_SIZE = WIDTH // 8
RESPONSE_DELAY = 500

# Colores de tablero y de jaques
WHITE_COLOR = (240, 217, 181)
BROWN_COLOR = (181, 136, 99)
HIGHLIGHT_COLOR = (246, 246, 105)
MOVE_DOT_COLOR = (100, 100, 100)
CHECK_COLOR = (255, 0, 0)


# -------------------------------------------------
# FUNCIÓN AUXILIAR PARA CALCULAR COORDENADAS
# -------------------------------------------------
def get_draw_coords(square, sq_size, flip):
    file = chess.square_file(square)
    rank = chess.square_rank(square)

    if flip:
        col = 7 - file
        row = rank
    else:
        col = file
        row = 7 - rank

    return col, row


# -------------------------------------------------
# DIBUJAR TABLERO
# -------------------------------------------------
def draw_board(screen, sq_size, board, last_move, game_over, flip=False):
    font_coords = pygame.font.SysFont("Arial", 18, bold=True)
    letters = "abcdefgh"

    for row in range(8):
        for col in range(8):

            draw_row = row
            draw_col = col

            if flip:
                draw_row = 7 - row
                draw_col = 7 - col

            color = WHITE_COLOR if (row + col) % 2 == 0 else BROWN_COLOR
            pygame.draw.rect(
                screen,
                color,
                (draw_col * sq_size, draw_row * sq_size, sq_size, sq_size)
            )

            text_color = BROWN_COLOR if color == WHITE_COLOR else WHITE_COLOR

            # Letras (a-h) abajo
            if row == (0 if flip else 7):
                file_letter = letters[7 - col] if flip else letters[col]
                text = font_coords.render(file_letter, True, text_color)
                screen.blit(
                    text,
                    (draw_col * sq_size + sq_size - text.get_width() - 2,
                     draw_row * sq_size + sq_size - text.get_height() - 2)
                )

            # Números (1-8) lateral
            if col == (7 if flip else 0):
                rank_number = str(row + 1) if flip else str(8 - row)
                text = font_coords.render(rank_number, True, text_color)
                screen.blit(
                    text,
                    (draw_col * sq_size + 2, draw_row * sq_size + 2)
                )

    # Resaltar último movimiento
    if last_move:
        for sq in [last_move.from_square, last_move.to_square]:
            col, row = get_draw_coords(sq, sq_size, flip)
            pygame.draw.rect(
                screen,
                HIGHLIGHT_COLOR,
                (col * sq_size, row * sq_size, sq_size, sq_size)
            )

    # Resaltar jaque
    if board.is_check() and not game_over:
        king_square = board.king(board.turn)
        if king_square is not None:
            col, row = get_draw_coords(king_square, sq_size, flip)
            pygame.draw.rect(
                screen,
                CHECK_COLOR,
                (col * sq_size, row * sq_size, sq_size, sq_size),
                5
            )

    if game_over and board.is_checkmate():
        losing_king_square = board.king(board.turn)

        if losing_king_square is not None:
            row = 7 - chess.square_rank(losing_king_square)
            col = chess.square_file(losing_king_square)

            red_overlay = pygame.Surface((SQ_SIZE, SQ_SIZE))
            red_overlay.set_alpha(120)  # Transparencia
            red_overlay.fill((255, 0, 0))

            screen.blit(red_overlay, (col * SQ_SIZE, row * SQ_SIZE))


# -------------------------------------------------
# CÍRCULOS DE MOVIMIENTO (Esto para el engine sobra creo)
# -------------------------------------------------
def draw_move_dots(screen, sq_size, board, selected_square, flip=False):
    if selected_square is None:
        return

    for move in board.legal_moves:
        if move.from_square == selected_square:
            col, row = get_draw_coords(move.to_square, sq_size, flip)
            center = (
                col * sq_size + sq_size // 2,
                row * sq_size + sq_size // 2
            )
            radius = sq_size // 8
            pygame.draw.circle(screen, MOVE_DOT_COLOR, center, radius)


# -------------------------------------------------
# DIBUJAR PIEZAS
# -------------------------------------------------
def draw_pieces(screen, sq_size, board, pieces,
                dragging_piece=None, selected_square=None,
                mouse_pos=None, flip=False):

    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece:
            if dragging_piece and square == selected_square:
                continue

            col, row = get_draw_coords(square, sq_size, flip)

            screen.blit(
                pieces[piece.symbol()],
                (col * sq_size, row * sq_size)
            )

    if dragging_piece and mouse_pos:
        x, y = mouse_pos
        screen.blit(
            pieces[dragging_piece.symbol()],
            (x - sq_size // 2, y - sq_size // 2)
        )

