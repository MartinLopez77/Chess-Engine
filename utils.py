import chess

# Obtiene la posición del ratón
def get_square_from_mouse(pos, SQ_SIZE, flip=False):
    x, y = pos

    file = x // SQ_SIZE
    rank = y // SQ_SIZE

    if flip:
        file = 7 - file      # invertir columnas
        rank = rank          # filas ya invertidas al dibujar
    else:
        rank = 7 - rank      # filas normales

    return chess.square(file, rank)


# Valores clásicos de piezas
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}


# Obtener el valor del movimiento

def score_move(board, move):
    score = 0

    # --- Capturas ---
    if board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)

        # Captura al paso
        if captured_piece is None:
            score += PIECE_VALUES[chess.PAWN]
        else:
            score += PIECE_VALUES[captured_piece.piece_type]

    # --- Simular movimiento para ver si es mate ---
    board.push(move)

    if board.is_checkmate():
        score += 100

    board.pop()  # Muy importante deshacer

    return score



# Optimizado sin lo del mate, no está funcionando bien
def score_move_evo(board, move):
    score = 0

    if board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)

        if captured_piece is None:
            score += PIECE_VALUES[chess.PAWN]
        else:
            score += PIECE_VALUES[captured_piece.piece_type]

    return score



def score_board(board, my_color):
    """Evalúa el tablero desde la perspectiva del motor (my_color)"""
    # Bonus/malus por mate
    if board.is_checkmate():
        if board.turn == my_color:
            return -1000  # Turno del motor y está en jaque mate → mal
        else:
            return 1000   # Motor da mate → bien
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    total = 0
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            val = PIECE_VALUES[piece.piece_type]
            if piece.color == my_color:
                total += val
            else:
                total -= val
    return total

def score_board_after_move(board, move, my_color):
    board.push(move)
    val = score_board(board, my_color)
    board.pop()
    return val