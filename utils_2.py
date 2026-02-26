import chess

# Valores básicos de las piezas
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0  # No se puede capturar
}

# Casillas centrales
CENTER_SQUARES = [
    chess.D4, chess.D5, chess.E4, chess.E5,
    chess.C3, chess.C4, chess.C5, chess.C6,
    chess.F3, chess.F4, chess.F5, chess.F6
]

# Bonus/penalización
CENTER_BONUS = 0.1
KING_MOVE_PENALTY = 0.1
UNPROTECTED_PENALTY = 0.1

# -----------------------------------------------------------
# Función de evaluación completa
# -----------------------------------------------------------
def score_board_advanced(board, my_color):
    if board.is_checkmate():
        return 100 if board.turn != my_color else -100
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    king_moved = not board.has_castling_rights(my_color)

    # Precalcular atacantes/defensores
    attack_map = {sq: board.attackers(not my_color, sq) for sq in chess.SQUARES}
    defense_map = {sq: board.attackers(my_color, sq) for sq in chess.SQUARES}

    center_bb = chess.BB_D4 | chess.BB_D5 | chess.BB_E4 | chess.BB_E5
    my_center = center_bb & board.occupied_co[my_color]
    opp_center = center_bb & board.occupied_co[not my_color]
    score += CENTER_BONUS * bin(my_center).count("1")
    score -= CENTER_BONUS * bin(opp_center).count("1")

    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            val = PIECE_VALUES[piece.piece_type]
            score += val if piece.color == my_color else -val

            if piece.color == my_color:
                if attack_map[sq] and not defense_map[sq]:
                    score -= UNPROTECTED_PENALTY

    if king_moved:
        score -= KING_MOVE_PENALTY

    return score