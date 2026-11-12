# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/concatenated-codes/. The authors are listed in prov/5CDZ50.jsonl.
"""Concatenated codes: an outer Reed-Solomon code over GF(16) and an inner binary code.

Each GF(16) symbol is 4 bits (polynomial basis, modulus x^4 + x + 1). The inner code is
the Hamming [7,4,3] code (Forney concatenation) or, position by position, the Wozencraft
codes x -> (x, a_i x) (Justesen). Decoders: the plain two-stage decoder and Forney's
generalized minimum distance (GMD) decoder over an errors-and-erasures RS decoder
(Berlekamp-Welch on the positions that are not erased).
"""

from itertools import product
from typing import List, Optional, Sequence, Tuple

EXP = [0] * 30
LOG = [0] * 16
_x = 1
for _i in range(15):
    EXP[_i] = EXP[_i + 15] = _x
    LOG[_x] = _i
    _x <<= 1
    if _x & 0x10:
        _x ^= 0x13


def mul(a: int, b: int) -> int:
    return 0 if a == 0 or b == 0 else EXP[LOG[a] + LOG[b]]


def inv(a: int) -> int:
    return EXP[(15 - LOG[a]) % 15]


def poly_eval(p: Sequence[int], x: int) -> int:
    acc = 0
    for c in reversed(p):
        acc = mul(acc, x) ^ c
    return acc


# ---------- outer code: Reed-Solomon [n, k, n-k+1] over GF(16) ----------

def rs_points(n: int) -> List[int]:
    return [EXP[i] for i in range(n)]  # distinct nonzero elements, n <= 15


def rs_encode(msg: Sequence[int], n: int) -> List[int]:
    return [poly_eval(msg, a) for a in rs_points(n)]


def solve(rows: List[List[int]], rhs: List[int], nvars: int) -> Optional[List[int]]:
    """Any solution of a linear system over GF(16) (free variables set to 0), or None."""
    m = [r[:] + [b] for r, b in zip(rows, rhs)]
    piv, r = [], 0
    for c in range(nvars):
        p = next((i for i in range(r, len(m)) if m[i][c]), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        f = inv(m[r][c])
        m[r] = [mul(f, v) for v in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c]:
                g = m[i][c]
                m[i] = [v ^ mul(g, w) for v, w in zip(m[i], m[r])]
        piv.append(c)
        r += 1
    if any(row[-1] for row in m[r:]):
        return None
    x = [0] * nvars
    for i, c in enumerate(piv):
        x[c] = m[i][-1]
    return x


def poly_divmod(a: List[int], b: List[int]) -> Tuple[List[int], List[int]]:
    a = a[:]
    while b and b[-1] == 0:
        b = b[:-1]
    q = [0] * max(len(a) - len(b) + 1, 1)
    f = inv(b[-1])
    for i in range(len(a) - len(b), -1, -1):
        c = mul(a[i + len(b) - 1], f)
        q[i] = c
        for j, bj in enumerate(b):
            a[i + j] ^= mul(c, bj)
    return q, a[:len(b) - 1]


def rs_decode(word: Sequence[Optional[int]], k: int) -> Optional[List[int]]:
    """Errors-and-erasures decoding (None = erased). With s erasures it corrects e errors
    whenever 2e + s < n - k + 1. Returns the message or None."""
    n = len(word)
    pts = [(a, y) for a, y in zip(rs_points(n), word) if y is not None]
    e = (len(pts) - k) // 2
    if e < 0:
        return None
    # Berlekamp-Welch: Q(a) = y E(a) with E monic of degree e and deg Q < e + k
    rows, rhs = [], []
    for a, y in pts:
        row = [mul(y, EXP[(LOG[a] * j) % 15]) for j in range(e)]   # E_0..E_(e-1)
        row += [EXP[(LOG[a] * j) % 15] for j in range(e + k)]       # Q_0..Q_(e+k-1)
        rows.append(row)
        rhs.append(mul(y, EXP[(LOG[a] * e) % 15]))                  # moves y a^e
    sol = solve(rows, rhs, 2 * e + k)
    if sol is None:
        return None
    big_e = sol[:e] + [1]
    q = sol[e:]
    msg, rem = poly_divmod(q, big_e)
    if any(rem) or any(msg[k:]):
        return None
    msg = (msg + [0] * k)[:k]
    wrong = sum(poly_eval(msg, a) != y for a, y in pts)
    return msg if 2 * wrong + (n - len(pts)) < n - k + 1 else None


# ---------- inner code: Hamming [7, 4, 3] ----------

def hamming_encode(sym: int) -> int:
    d = [sym >> i & 1 for i in range(4)]
    p = [d[0] ^ d[1] ^ d[3], d[0] ^ d[2] ^ d[3], d[1] ^ d[2] ^ d[3]]
    return sym | p[0] << 4 | p[1] << 5 | p[2] << 6


HAMMING = [hamming_encode(s) for s in range(16)]


def nearest(block: int, table: Sequence[int]) -> Tuple[int, int]:
    """(symbol, distance) of the nearest inner codeword."""
    return min(((s, bin(block ^ c).count("1")) for s, c in enumerate(table)),
               key=lambda t: t[1])


# ---------- the concatenated code ----------

class Concatenated:
    """Outer RS [n, k] over GF(16); inner code given by a table per position."""

    def __init__(self, n: int, k: int, inner: Optional[List[List[int]]] = None, width: int = 7,
                 inner_distance: int = 3):
        self.n, self.k, self.width = n, k, width
        self.inner = inner or [HAMMING] * n
        self.d_in = inner_distance

    def encode(self, msg: Sequence[int]) -> int:
        word = 0
        for i, c in enumerate(rs_encode(msg, self.n)):
            word |= self.inner[i][c] << (self.width * i)
        return word

    def blocks(self, received: int) -> List[int]:
        mask = (1 << self.width) - 1
        return [received >> (self.width * i) & mask for i in range(self.n)]

    def decode_two_stage(self, received: int) -> Optional[List[int]]:
        syms = [nearest(b, self.inner[i])[0] for i, b in enumerate(self.blocks(received))]
        return rs_decode(syms, self.k)

    def decode_gmd(self, received: int) -> Optional[List[int]]:
        """Forney's GMD: erase the s least reliable inner decisions for each s, decode, and
        keep the candidate closest to the received word."""
        inner = [nearest(b, self.inner[i]) for i, b in enumerate(self.blocks(received))]
        order = sorted(range(self.n), key=lambda i: -min(inner[i][1], self.d_in / 2))
        best, best_dist = None, None
        for s in range(self.n - self.k + 1):  # s = 0 .. D - 1
            word: List[Optional[int]] = [sym for sym, _ in inner]
            for i in order[:s]:
                word[i] = None
            msg = rs_decode(word, self.k)
            if msg is not None:
                dist = bin(self.encode(msg) ^ received).count("1")
                if best is None or dist < best_dist:
                    best, best_dist = msg, dist
        return best

    def min_distance(self) -> int:
        """By enumeration of all 16^k messages (the code is linear over GF(2))."""
        return min(bin(self.encode(m)).count("1")
                   for m in product(range(16), repeat=self.k) if any(m))


def justesen(k: int) -> Concatenated:
    """Outer RS [15, k]; position i uses the inner code x -> (x, a_i x), a_i = EXP[i]."""
    pts = rs_points(15)
    inner = [[x | mul(a, x) << 4 for x in range(16)] for a in pts]
    return Concatenated(15, k, inner, width=8, inner_distance=1)
