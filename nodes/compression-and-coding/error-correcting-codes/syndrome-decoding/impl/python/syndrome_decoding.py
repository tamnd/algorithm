# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/syndrome-decoding/. The authors are listed in prov/4Q2QZ4.jsonl.

"""Syndrome decoding of a linear code over GF(q), q prime.

Vectors are rows (tuples of integers in 0..q-1). H is an (n - k) x n
parity-check matrix, given as a list of rows. The table maps each syndrome
H e^T to a coset leader e of least weight. The first error pattern of least
weight in a fixed order wins, so the decoder is deterministic.
"""

from itertools import combinations, product

Vector = tuple[int, ...]
Matrix = list[list[int]]


def syndrome(h: Matrix, v: Vector, q: int = 2) -> Vector:
    """Return H v^T as a tuple. Cost: (n - k) n multiplications mod q."""
    return tuple(sum(a * b for a, b in zip(row, v)) % q for row in h)


def rank_mod(rows: Matrix, q: int) -> int:
    """Rank of a matrix over GF(q), q prime, by Gaussian elimination."""
    m = [list(r) for r in rows]
    rank, ncols = 0, len(m[0]) if m else 0
    for col in range(ncols):
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
        rank += 1
    return rank


def error_patterns(n: int, w: int, q: int):
    """All vectors of length n and weight w: positions in lexicographic order, then values."""
    for pos in combinations(range(n), w):
        for vals in product(range(1, q), repeat=w):
            e = [0] * n
            for p, a in zip(pos, vals):
                e[p] = a
            yield tuple(e)


def build_table(h: Matrix, q: int = 2) -> dict[Vector, Vector]:
    """Map each syndrome to a coset leader of least weight.

    Precondition: q is prime and h has n columns. The loop stops as soon as
    all q^rank(H) syndromes have a leader, so it enumerates the error
    patterns of weight at most the covering radius of the code.
    """
    n = len(h[0])
    size = q ** rank_mod(h, q)
    table: dict[Vector, Vector] = {}  # @line L1
    for w in range(n + 1):  # @line L2
        for e in error_patterns(n, w, q):  # @line L3
            s = syndrome(h, e, q)  # @line L4
            if s not in table:  # @line L5
                table[s] = e
        if len(table) == size:  # @line L6
            return table
    return table  # @line L7


def decode(table: dict[Vector, Vector], h: Matrix, r: Vector, q: int = 2) -> Vector:
    """Return the codeword r - e, where e is the coset leader of r.

    Cost: one syndrome, (n - k) n multiplications, and one table lookup.
    """
    s = syndrome(h, r, q)  # @line L8
    e = table[s]  # @line L9
    return tuple((a - b) % q for a, b in zip(r, e))  # @line L10
