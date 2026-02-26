import numpy as np

# -------------------------------------------------------------
# BITBOARDS INICIALES
# -------------------------------------------------------------
bitboards = {
    ("P", "W"): np.uint64(0x000000000000FF00),  # peones blancos
    ("N", "W"): np.uint64(0x0000000000000042),  # caballos
    ("B", "W"): np.uint64(0x0000000000000024),  # alfiles
    ("R", "W"): np.uint64(0x0000000000000081),  # torres
    ("Q", "W"): np.uint64(0x0000000000000008),  # dama
    ("K", "W"): np.uint64(0x0000000000000010),  # rey
    ("P", "B"): np.uint64(0x00FF000000000000),  # peones negros
    ("N", "B"): np.uint64(0x4200000000000000),
    ("B", "B"): np.uint64(0x2400000000000000),
    ("R", "B"): np.uint64(0x8100000000000000),
    ("Q", "B"): np.uint64(0x0800000000000000),
    ("K", "B"): np.uint64(0x1000000000000000),
}

# -------------------------------------------------------------
# FUNCIONES DE OCUPACIÓN
# -------------------------------------------------------------
def occupied(bitboards):
    total = np.uint64(0)
    for bb in bitboards.values():
        total |= bb
    return total

def occupied_white(bitboards):
    total = np.uint64(0)
    for key, bb in bitboards.items():
        if key[1] == "W":
            total |= bb
    return total

def occupied_black(bitboards):
    total = np.uint64(0)
    for key, bb in bitboards.items():
        if key[1] == "B":
            total |= bb
    return total

# -------------------------------------------------------------
# FUNCIONES AUXILIARES
# -------------------------------------------------------------
def bit_scan_forward(bb):
    """Devuelve el índice del primer bit a 1, o -1 si ninguno"""
    if bb == 0:
        return -1
    return int(np.log2(bb & -bb))

def pop_bit(bb, index):
    """Quita un bit específico y devuelve el nuevo bitboard"""
    return bb & ~(np.uint64(1) << np.uint64(index))

def set_bit(bb, index):
    """Pone un bit específico"""
    return bb | (np.uint64(1) << np.uint64(index))

def print_board(bitboards):
    """Imprime tablero en consola"""
    board = ["." for _ in range(64)]
    for (piece, color), bb in bitboards.items():
        bb_copy = bb
        while bb_copy:
            sq = bit_scan_forward(bb_copy)
            bb_copy = pop_bit(bb_copy, sq)
            symbol = piece.lower() if color == "B" else piece.upper()
            board[sq] = symbol
    for r in range(7, -1, -1):
        print(" ".join(board[r*8:(r+1)*8]))
    print("\n")

# -------------------------------------------------------------
# MOVIMIENTOS SIMPLES (PEONES, CABALLOS, TORRES)
# -------------------------------------------------------------
def pawn_moves(square, color, all_occ, enemy_occ):
    """Devuelve un bitboard con los posibles movimientos de un peón"""
    moves = np.uint64(0)
    if color == "W":
        # Avance normal
        if not (all_occ & (1 << (square + 8))):
            moves |= (1 << (square + 8))
        # Capturas
        if square % 8 != 0:
            moves |= (1 << (square + 7)) & enemy_occ
        if square % 8 != 7:
            moves |= (1 << (square + 9)) & enemy_occ
    else:
        if not (all_occ & (1 << (square - 8))):
            moves |= (1 << (square - 8))
        if square % 8 != 0:
            moves |= (1 << (square - 9)) & enemy_occ
        if square % 8 != 7:
            moves |= (1 << (square - 7)) & enemy_occ
    return moves

def knight_moves(square, all_occ, color):
    """Devuelve un bitboard con movimientos de caballo"""
    # Máscara general (sin bordes)
    moves = np.uint64(0)
    r, f = square // 8, square % 8
    shifts = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    enemy_occ = occupied_black(bitboards) if color == "W" else occupied_white(bitboards)
    own_occ = occupied_white(bitboards) if color == "W" else occupied_black(bitboards)
    for dr, df in shifts:
        nr, nf = r + dr, f + df
        if 0 <= nr < 8 and 0 <= nf < 8:
            sq = nr*8 + nf
            if not (own_occ & (1 << sq)):
                moves |= (1 << sq)
    return moves

# -------------------------------------------------------------
# MOVER PIEZA
# -------------------------------------------------------------
def move_piece(bitboards, from_sq, to_sq, piece, color):
    bb = bitboards[(piece, color)]
    bb = pop_bit(bb, from_sq)
    bb = set_bit(bb, to_sq)
    bitboards[(piece, color)] = bb

    # Captura
    for key, bb2 in bitboards.items():
        if key[1] != color:
            if bb2 & (1 << to_sq):
                bitboards[key] = pop_bit(bb2, to_sq)

# -------------------------------------------------------------
# EJEMPLO DE USO
# -------------------------------------------------------------
print("Tablero inicial:")
print_board(bitboards)

# Mover peón blanco de e2 (bit12) a e4 (bit28)
move_piece(bitboards, 12, 28, "P", "W")

print("Después de mover e2->e4:")
print_board(bitboards)

# Calcular movimientos de un peón en e4
all_occ = occupied(bitboards)
enemy_occ = occupied_black(bitboards)
moves = pawn_moves(28, "W", all_occ, enemy_occ)
print(f"Posibles movimientos del peón en e4: {bin(moves)}")