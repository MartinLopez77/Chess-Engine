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

# Evaluación del tablero según el color
def score_board(board, my_color):

    if board.is_checkmate():
        if board.turn == my_color:
            return -100  # Turno del motor y está en jaque mate → mal
        else:
            return 100   # Motor da mate → bien
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
