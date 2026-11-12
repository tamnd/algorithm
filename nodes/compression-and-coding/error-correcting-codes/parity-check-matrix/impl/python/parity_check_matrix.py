# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parity-check-matrix/. The authors are listed in prov/TTGQBS.jsonl.

"""Parity-check matrices over GF(q), q prime.

Vectors are rows. For a k x n generator matrix G of rank k, a parity-check
matrix H is an (n - k) x n matrix of rank n - k with G H^T = 0. Then
C = { v : H v^T = 0 }. The minimum distance d of C is the least number of
columns of H that are linearly dependent.
"""

from itertools import combinations

Matrix = list[list[int]]


def rref(rows: Matrix, q: int) -> tuple[Matrix, list[int]]:
    """Reduced row echelon form over GF(q) and the pivot columns. Zero rows are dropped."""
    m = [list(r) for r in rows]
    pivots: list[int] = []
    rank = 0
    for col in range(len(m[0]) if m else 0):
        piv = next((i for i in range(rank, len(m)) if m[i][col] % q), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        inv = pow(m[rank][col], q - 2, q)
        m[rank] = [x * inv % q for x in m[rank]]
        for i in range(len(m)):
            if i != rank and m[i][col]:
                f = m[i][col]
                m[i] = [(x - f * y) % q for x, y in zip(m[i], m[rank])]
        pivots.append(col)
        rank += 1
    return m[:rank], pivots


def rank(rows: Matrix, q: int) -> int:
    return len(rref(rows, q)[1]) if rows else 0


def parity_check_from_systematic(g: Matrix, q: int = 2) -> Matrix:
    """For G = [I_k | P], return H = [-P^T | I_(n-k)]."""
    k, n = len(g), len(g[0])
    p = [row[k:] for row in g]
    return [[(-p[i][r]) % q for i in range(k)] + [1 if r == j else 0 for j in range(n - k)] for r in range(n - k)]


def parity_check_matrix(g: Matrix, q: int = 2) -> Matrix:
    """A basis of the null space of G, one row per free column of the RREF of G."""
    n = len(g[0])
    red, pivots = rref(g, q)
    free = [j for j in range(n) if j not in pivots]
    h = []
    for f in free:
        v = [0] * n
        v[f] = 1
        for i, col in enumerate(pivots):
            v[col] = (-red[i][f]) % q
        h.append(v)
    return h


def syndrome(h: Matrix, v: list[int], q: int = 2) -> tuple[int, ...]:
    return tuple(sum(a * b for a, b in zip(row, v)) % q for row in h)


def min_dependent_columns(h: Matrix, q: int = 2) -> int | None:
    """Least s such that some s columns of H are linearly dependent; None if all n are independent."""
    n = len(h[0])
    cols = [[h[i][j] for i in range(len(h))] for j in range(n)]
    for s in range(1, n + 1):
        for subset in combinations(range(n), s):
            if rank([cols[j] for j in subset], q) < s:
                return s
    return None
