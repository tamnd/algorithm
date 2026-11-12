# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-codeword-problem/. The authors are listed in prov/XEFEQH.jsonl.

"""The nearest codeword problem over GF(2): exact search, the syndrome form, and
the reduction from three dimensional matching of Berlekamp, McEliece and van Tilborg.

Vectors are rows of 0 and 1. A code is given by a k x n generator matrix G,
or by an r x n parity-check matrix H.
"""

from itertools import combinations, product

Vector = tuple[int, ...]
Matrix = list[list[int]]


def nearest_codeword(g: Matrix, y: Vector) -> tuple[Vector, int]:
    """Exact search over all 2^k codewords. Cost: Θ(2^k n k) bit operations."""
    k, n = len(g), len(g[0])
    best: tuple[Vector, int] | None = None
    for m in product(range(2), repeat=k):
        c = tuple(sum(m[i] * g[i][j] for i in range(k)) % 2 for j in range(n))
        d = sum(a != b for a, b in zip(c, y))
        if best is None or d < best[1]:
            best = (c, d)
    assert best is not None
    return best


def coset_weight(h: Matrix, s: Vector, w: int) -> Vector | None:
    """Return e with weight at most w and H e^T = s, or None. Tries errors by weight."""
    n = len(h[0])
    for size in range(w + 1):
        for pos in combinations(range(n), size):
            if tuple(sum(h[i][j] for j in pos) % 2 for i in range(len(h))) == tuple(s):
                return tuple(1 if j in pos else 0 for j in range(n))
    return None


def solve_and_kernel(h: Matrix, s: Vector) -> tuple[Vector, Matrix] | None:
    """Gauss-Jordan over GF(2): one y with H y^T = s, and a basis G of the kernel of H."""
    r, n = len(h), len(h[0])
    m = [list(h[i]) + [s[i]] for i in range(r)]
    pivots: list[int] = []
    row = 0
    for col in range(n):
        piv = next((i for i in range(row, r) if m[i][col]), None)
        if piv is None:
            continue
        m[row], m[piv] = m[piv], m[row]
        for i in range(r):
            if i != row and m[i][col]:
                m[i] = [a ^ b for a, b in zip(m[i], m[row])]
        pivots.append(col)
        row += 1
    if any(m[i][n] for i in range(row, r)):
        return None
    y = [0] * n
    for i, col in enumerate(pivots):
        y[col] = m[i][n]
    free = [j for j in range(n) if j not in pivots]
    basis = []
    for f in free:
        v = [0] * n
        v[f] = 1
        for i, col in enumerate(pivots):
            v[col] = m[i][f]
        basis.append(v)
    return tuple(y), basis


def three_dm_to_coset_weight(q: int, triples: list[tuple[int, int, int]]) -> tuple[Matrix, Vector, int]:
    """Berlekamp, McEliece and van Tilborg: H is the 3q x t incidence matrix, s = all ones, w = q.

    Element x of X is row x, element y of Y is row q + y, element z of Z is row 2q + z.
    """
    h = [[0] * len(triples) for _ in range(3 * q)]
    for j, (x, y, z) in enumerate(triples):
        h[x][j] = 1
        h[q + y][j] = 1
        h[2 * q + z][j] = 1
    return h, (1,) * (3 * q), q


def has_perfect_matching(q: int, triples: list[tuple[int, int, int]]) -> bool:
    """Brute force three dimensional matching: q triples that cover X, Y and Z."""
    for chosen in combinations(triples, q):
        if all(len({t[i] for t in chosen}) == q for i in range(3)):
            return True
    return False
