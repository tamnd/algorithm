# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simplex-code/. The authors are listed in prov/KNDK1C.jsonl.

"""Simplex codes over GF(q), q prime, and the first order Reed-Muller code built from them.

The generator matrix of the simplex code S_r has one column for each
1-dimensional subspace of GF(q)^r (for q = 2: each nonzero vector), so it is
the parity-check matrix of the Hamming code of order r. The code is
[(q^r - 1)/(q - 1), r, q^(r - 1)] and each nonzero codeword has weight q^(r - 1).
"""

from itertools import product

Vector = tuple[int, ...]


def generator_matrix(r: int, q: int = 2) -> list[list[int]]:
    """Columns: nonzero vectors of length r with first nonzero entry 1, in lexicographic order."""
    cols = [v for v in product(range(q), repeat=r) if any(v) and next(x for x in v if x) == 1]
    return [[c[i] for c in cols] for i in range(r)]


def encode(message: Vector, g: list[list[int]], q: int = 2) -> Vector:
    """c = m G. For q = 2, entry j is the inner product of m with the j-th nonzero vector."""
    n = len(g[0])
    return tuple(sum(message[i] * g[i][j] for i in range(len(g))) % q for j in range(n))


def codewords(r: int, q: int = 2) -> list[Vector]:
    g = generator_matrix(r, q)
    return [encode(m, g, q) for m in product(range(q), repeat=r)]


def weight_distribution(words: list[Vector]) -> dict[int, int]:
    out: dict[int, int] = {}
    for c in words:
        w = sum(1 for x in c if x)
        out[w] = out.get(w, 0) + 1
    return dict(sorted(out.items()))


def first_order_reed_muller(r: int) -> list[Vector]:
    """RM(1, r): put a 0 in front of each simplex codeword, then add the all ones word."""
    base = [(0,) + c for c in codewords(r)]
    ones = (1,) * (1 << r)
    return base + [tuple(1 - x for x in c) for c in base if c != ones]


def griesmer_length(k: int, d: int, q: int = 2) -> int:
    """The Griesmer sum: sum over i < k of ceil(d / q^i)."""
    return sum(-(-d // q**i) for i in range(k))
