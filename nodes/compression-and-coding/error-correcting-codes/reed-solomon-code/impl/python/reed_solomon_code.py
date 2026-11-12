# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reed-solomon-code/. The authors are listed in prov/G5ZPZ8.jsonl.
"""Reed-Solomon codes over GF(2^m): the cyclic view, the evaluation view,
and the dual basis map of CCSDS 131.0-B.

Polynomials and codewords are lists, lowest degree first. A codeword
c = [c_0, ..., c_{n-1}] is c(x) = sum c_i x^i. Standards that send the
highest power first (QR codes, CCSDS) send reversed(c).
"""

from gf import GF2m


def rs_generator(field: GF2m, nsym: int, b: int = 1, step: int = 1) -> list[int]:
    """g(x) = prod_{j=b}^{b+nsym-1} (x - beta^j) with beta = alpha^step.

    QR codes: b = 0, step = 1. CCSDS 131.0-B: b = 128 - E, step = 11, nsym = 2E.
    """
    g = [1]
    for j in range(b, b + nsym):
        g = field.pmul(g, [field.alpha(step * j), 1])  # minus is plus in GF(2^m)
    return g


def encode_systematic(field: GF2m, msg: list[int], g: list[int]) -> list[int]:
    """c(x) = x^r m(x) - (x^r m(x) mod g(x)), r = deg g.

    msg[i] is the coefficient of x^i of m(x). The check symbols are c_0 .. c_{r-1},
    the message is c_r .. c_{r+k-1}. A message shorter than n - r gives a
    shortened code: the missing top symbols are zero and are not sent.
    """
    r = len(g) - 1
    shifted = [0] * r + list(msg)
    _, rem = field.pdivmod(shifted, g)
    rem = rem + [0] * (r - len(rem))
    return rem + list(msg)  # in characteristic 2, minus is plus


def encode_evaluation(field: GF2m, msg: list[int], points: list[int]) -> list[int]:
    """c_i = f(points[i]) with f(x) = sum msg[j] x^j, deg f < k (Reed and Solomon, 1960)."""
    return [field.peval(msg, a) for a in points]


def syndromes(field: GF2m, word: list[int], nsym: int, b: int = 1, step: int = 1) -> list[int]:
    """S_j = word(beta^(b + j)) for j = 0 .. nsym - 1; all zero exactly for codewords."""
    return [field.peval(word, field.alpha(step * (b + j))) for j in range(nsym)]


# ---- CCSDS 131.0-B-5, Annex F: Berlekamp (dual basis) and conventional representations.
# Row i of T_AL is the dual basis form of alpha^(7 - i). A byte u = [u7 .. u0] in the
# conventional basis maps to z = [z0 .. z7] = u T_AL. Bytes are written as in the annex,
# with the leftmost bit as the most significant bit of the int.
T_AL = [0b10001101, 0b11101111, 0b11101100, 0b10000110,
        0b11111010, 0b10011001, 0b10101111, 0b01111011]
T_AL_INV = [0b11000101, 0b01000010, 0b00101110, 0b11111101,
            0b11110000, 0b01111001, 0b10101100, 0b11001100]


def _row_times_matrix(v: int, rows: list[int]) -> int:
    out = 0
    for i in range(8):
        if (v >> (7 - i)) & 1:
            out ^= rows[i]
    return out


def conventional_to_dual(u: int) -> int:
    """[u7 .. u0] -> [z0 .. z7] = [u7 .. u0] T_AL."""
    return _row_times_matrix(u, T_AL)


def dual_to_conventional(z: int) -> int:
    """[z0 .. z7] -> [u7 .. u0] = [z0 .. z7] T_AL^-1."""
    return _row_times_matrix(z, T_AL_INV)


def ccsds_encode(msg_dual: list[int], e: int = 16) -> list[int]:
    """Encode one CCSDS codeword given and returned in the dual basis, highest power first.

    The first message byte is the coefficient of x^(n-1). The conventional encoder
    of Annex F, Figure F-1, sits between the two basis changes.
    """
    field = GF2m(8, 0x187)
    g = rs_generator(field, 2 * e, 128 - e, 11)
    msg = [dual_to_conventional(z) for z in reversed(msg_dual)]
    c = encode_systematic(field, msg, g)
    return [conventional_to_dual(u) for u in reversed(c)]
