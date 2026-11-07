# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laderman-algorithm/. The authors are listed in prov/JHP9MS.jsonl.

from typing import Optional

Matrix = list[list[int]]

# The 23 products M_r = (sum of c * A_ij) (sum of c * B_jk), with 1-based block indices.
# Each factor is a list of (coefficient, row, column).
PRODUCTS: list[tuple[list[tuple[int, int, int]], list[tuple[int, int, int]]]] = [
    ([(1, 1, 1), (1, 1, 2), (1, 1, 3), (-1, 2, 1), (-1, 2, 2), (-1, 3, 2), (-1, 3, 3)], [(1, 2, 2)]),
    ([(1, 1, 1), (-1, 2, 1)], [(-1, 1, 2), (1, 2, 2)]),
    ([(1, 2, 2)], [(-1, 1, 1), (1, 1, 2), (1, 2, 1), (-1, 2, 2), (-1, 2, 3), (-1, 3, 1), (1, 3, 3)]),
    ([(-1, 1, 1), (1, 2, 1), (1, 2, 2)], [(1, 1, 1), (-1, 1, 2), (1, 2, 2)]),
    ([(1, 2, 1), (1, 2, 2)], [(-1, 1, 1), (1, 1, 2)]),
    ([(1, 1, 1)], [(1, 1, 1)]),
    ([(-1, 1, 1), (1, 3, 1), (1, 3, 2)], [(1, 1, 1), (-1, 1, 3), (1, 2, 3)]),
    ([(-1, 1, 1), (1, 3, 1)], [(1, 1, 3), (-1, 2, 3)]),
    ([(1, 3, 1), (1, 3, 2)], [(-1, 1, 1), (1, 1, 3)]),
    ([(1, 1, 1), (1, 1, 2), (1, 1, 3), (-1, 2, 2), (-1, 2, 3), (-1, 3, 1), (-1, 3, 2)], [(1, 2, 3)]),
    ([(1, 3, 2)], [(-1, 1, 1), (1, 1, 3), (1, 2, 1), (-1, 2, 2), (-1, 2, 3), (-1, 3, 1), (1, 3, 2)]),
    ([(-1, 1, 3), (1, 3, 2), (1, 3, 3)], [(1, 2, 2), (1, 3, 1), (-1, 3, 2)]),
    ([(1, 1, 3), (-1, 3, 3)], [(1, 2, 2), (-1, 3, 2)]),
    ([(1, 1, 3)], [(1, 3, 1)]),
    ([(1, 3, 2), (1, 3, 3)], [(-1, 3, 1), (1, 3, 2)]),
    ([(-1, 1, 3), (1, 2, 2), (1, 2, 3)], [(1, 2, 3), (1, 3, 1), (-1, 3, 3)]),
    ([(1, 1, 3), (-1, 2, 3)], [(1, 2, 3), (-1, 3, 3)]),
    ([(1, 2, 2), (1, 2, 3)], [(-1, 3, 1), (1, 3, 3)]),
    ([(1, 1, 2)], [(1, 2, 1)]),
    ([(1, 2, 3)], [(1, 3, 2)]),
    ([(1, 2, 1)], [(1, 1, 3)]),
    ([(1, 3, 1)], [(1, 1, 2)]),
    ([(1, 3, 3)], [(1, 3, 3)]),
]

# C_ik is the sum of the products with these numbers (1-based); all coefficients are +1.
OUTPUTS: dict[tuple[int, int], list[int]] = {
    (1, 1): [6, 14, 19],
    (1, 2): [1, 4, 5, 6, 12, 14, 15],
    (1, 3): [6, 7, 9, 10, 14, 16, 18],
    (2, 1): [2, 3, 4, 6, 14, 16, 17],
    (2, 2): [2, 4, 5, 6, 20],
    (2, 3): [14, 16, 17, 18, 21],
    (3, 1): [6, 7, 8, 11, 12, 13, 14],
    (3, 2): [12, 13, 14, 15, 22],
    (3, 3): [6, 7, 8, 9, 23],
}


def _classical(a: Matrix, b: Matrix, p: int, mod: Optional[int]) -> Matrix:
    c = [[0] * p for _ in range(len(a))]
    for i, row in enumerate(a):
        ci = c[i]
        for k, aik in enumerate(row):
            if aik:
                bk = b[k]
                for j in range(p):
                    ci[j] += aik * bk[j]
        if mod is not None:
            c[i] = [x % mod for x in ci]
    return c


def _combine(blocks: dict[tuple[int, int], Matrix], terms: list[tuple[int, int, int]],
             rows: int, cols: int, mod: Optional[int]) -> Matrix:
    out = [[0] * cols for _ in range(rows)]
    for coef, i, j in terms:
        blk = blocks[(i, j)]
        for r in range(rows):
            orow, brow = out[r], blk[r]
            for s in range(cols):
                orow[s] += coef * brow[s]
    if mod is not None:
        out = [[x % mod for x in row] for row in out]
    return out


def laderman_algorithm(a: Matrix, b: Matrix, p: Optional[int] = None, mod: Optional[int] = None,
                       n0: int = 1) -> Matrix:
    """Return a * b by Laderman's 23-product recursion on 3 x 3 grids of blocks.

    a is n x m and b is m x p (lists of rows); pass p when m = 0. The ring is
    Z, or Z/mod Z when mod is set; commutativity is not used. Inputs with a
    side of at most n0 (n0 >= 1) use the classical product; other sides are
    padded with zeros to a multiple of 3 at each level. Cost: O(n^(log3 23))
    ring operations for n x n inputs; recursion depth O(log max(n, m, p)).
    """
    if n0 < 1:
        raise ValueError("the cutoff n0 must be at least 1")
    n, m = len(a), len(b)
    if p is None:
        p = len(b[0]) if m > 0 else 0
    if any(len(row) != m for row in a) or any(len(row) != p for row in b):
        raise ValueError("the shapes do not match")
    return _laderman(a, b, n, m, p, mod, n0)


def _laderman(a: Matrix, b: Matrix, n: int, m: int, p: int, mod: Optional[int], n0: int) -> Matrix:
    if min(n, m, p) <= n0:  # @line L1
        return _classical(a, b, p, mod)
    if n % 3 or m % 3 or p % 3:  # @line L2
        n3, m3, p3 = -(-n // 3) * 3, -(-m // 3) * 3, -(-p // 3) * 3
        ap = [row + [0] * (m3 - m) for row in a] + [[0] * m3 for _ in range(n3 - n)]
        bp = [row + [0] * (p3 - p) for row in b] + [[0] * p3 for _ in range(m3 - m)]
        cp = _laderman(ap, bp, n3, m3, p3, mod, n0)
        return [row[:p] for row in cp[:n]]
    h, k, q = n // 3, m // 3, p // 3  # @line L3
    ab = {(i + 1, j + 1): [row[j * k:(j + 1) * k] for row in a[i * h:(i + 1) * h]]
          for i in range(3) for j in range(3)}
    bb = {(i + 1, j + 1): [row[j * q:(j + 1) * q] for row in b[i * k:(i + 1) * k]]
          for i in range(3) for j in range(3)}
    prods = []
    for left, right in PRODUCTS:  # @line L4
        x = _combine(ab, left, h, k, mod)
        y = _combine(bb, right, k, q, mod)
        prods.append(_laderman(x, y, h, k, q, mod, n0))
    cb = {}
    for (i, j), idx in OUTPUTS.items():  # @line L5
        cb[(i, j)] = _combine({(r, 0): prods[r - 1] for r in idx}, [(1, r, 0) for r in idx], h, q, mod)
    out = []  # @line L6
    for i in range(1, 4):
        for r in range(h):
            out.append(cb[(i, 1)][r] + cb[(i, 2)][r] + cb[(i, 3)][r])
    return out


def count_multiplications(n: int, n0: int = 1) -> int:
    """Scalar multiplications for n x n inputs with n = 3^t * s, s <= n0: 23 T(n/3), base n^3."""
    if n <= n0:
        return n ** 3
    return 23 * count_multiplications(n // 3, n0)
