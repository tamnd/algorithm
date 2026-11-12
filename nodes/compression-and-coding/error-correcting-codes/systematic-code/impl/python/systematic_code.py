# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/systematic-code/. The authors are listed in prov/9C8353.jsonl.

"""Systematic generator matrices over GF(q), q prime.

systematic_form row reduces G with Gauss-Jordan elimination, taking the
pivots from left to right. The pivot columns form an information set S. The
column permutation that puts S first turns the reduced matrix into
[I_k | P]. When the first k columns are independent, S = {0, ..., k - 1},
the permutation is the identity, and the code itself is systematic on its
first k positions.
"""

from itertools import combinations

Matrix = list[list[int]]


def rref(rows: Matrix, q: int) -> tuple[Matrix, list[int]]:
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


def systematic_form(g: Matrix, q: int = 2) -> tuple[Matrix, list[int]]:
    """Return (G_s, perm): G_s = [I_k | P], and column j of G_s is column perm[j] of the code.

    Precondition: G has full rank k. Cost: O(k^2 n) field operations.
    """
    red, pivots = rref(g, q)
    if len(pivots) < len(g):
        raise ValueError("G does not have full rank")
    perm = pivots + [j for j in range(len(g[0])) if j not in pivots]
    return [[row[j] for j in perm] for row in red], perm


def encode(message: list[int], gs: Matrix, perm: list[int], q: int = 2) -> list[int]:
    """Codeword of the original code: the message sits at the positions perm[0..k-1]."""
    k, n = len(gs), len(gs[0])
    c_perm = [sum(message[i] * gs[i][j] for i in range(k)) % q for j in range(n)]
    c = [0] * n
    for j, x in zip(perm, c_perm):
        c[j] = x
    return c


def is_information_set(g: Matrix, positions: tuple[int, ...], q: int = 2) -> bool:
    """True when the k columns at these positions are linearly independent."""
    return len(positions) == len(g) and len(rref([[row[j] for j in positions] for row in g], q)[1]) == len(g)


def information_sets(g: Matrix, q: int = 2) -> list[tuple[int, ...]]:
    return [s for s in combinations(range(len(g[0])), len(g)) if is_information_set(g, s, q)]
