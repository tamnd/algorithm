# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/erasure-decoding/. The authors are listed in prov/GWSB3B.jsonl.
"""Erasure decoding of a linear code over a prime field GF(p) by Gaussian elimination.

A word is a list whose entries are field elements or None (an erasure). The code is the
null space of the parity-check matrix H: H c^T = 0. With E the erased positions and S the
others, the erased symbols satisfy H_E c_E^T = -H_S c_S^T. They are determined if and only
if the columns of H at E are linearly independent. This is also the maximum likelihood
decoder on an erasure channel.
"""

from typing import List, Optional, Sequence, Tuple

Word = List[Optional[int]]


def solve_mod_p(a: List[List[int]], b: List[int], p: int) -> Tuple[Optional[List[int]], int]:
    """Solve a x = b over GF(p). Returns (x, rank); x is None if the solution is not unique
    or if there is none. Gauss-Jordan elimination, O(rows * cols * min(rows, cols))."""
    rows, cols = len(a), (len(a[0]) if a else 0)
    m = [[v % p for v in a[i]] + [b[i] % p] for i in range(rows)]
    pivots = []
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if m[i][c]), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        f = pow(m[r][c], p - 2, p)
        m[r] = [v * f % p for v in m[r]]
        for i in range(rows):
            if i != r and m[i][c]:
                t = m[i][c]
                m[i] = [(v - t * w) % p for v, w in zip(m[i], m[r])]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    if any(m[i][cols] for i in range(r, rows)):
        return None, r  # inconsistent: the word is not a codeword with erasures
    if r < cols:
        return None, r  # a free variable: more than one codeword fits
    x = [0] * cols
    for i, c in enumerate(pivots):
        x[c] = m[i][cols]
    return x, r


def decode(h: Sequence[Sequence[int]], y: Word, p: int) -> Optional[List[int]]:
    """Fill the erasures of y. None if the erasure pattern is not uniquely decodable."""
    erased = [j for j, v in enumerate(y) if v is None]
    if not erased:
        return list(y)
    a = [[row[j] for j in erased] for row in h]
    b = [-sum(row[j] * y[j] for j in range(len(y)) if y[j] is not None) % p for row in h]
    x, _ = solve_mod_p(a, b, p)
    if x is None:
        return None
    c = list(y)
    for j, v in zip(erased, x):
        c[j] = v
    return c


def correctable(h: Sequence[Sequence[int]], erased: Sequence[int], p: int) -> bool:
    """True if the columns of H at the erased positions are linearly independent."""
    a = [[row[j] for j in erased] for row in h]
    _, r = solve_mod_p(a, [0] * len(h), p)
    return r == len(erased)


def null_space(g: Sequence[Sequence[int]], p: int) -> List[List[int]]:
    """A basis of {x : g x^T = 0}, the rows of a parity-check matrix for the code spanned by g."""
    k, n = len(g), len(g[0])
    m = [[v % p for v in row] for row in g]
    pivots, r = [], 0
    for c in range(n):
        piv = next((i for i in range(r, k) if m[i][c]), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        f = pow(m[r][c], p - 2, p)
        m[r] = [v * f % p for v in m[r]]
        for i in range(k):
            if i != r and m[i][c]:
                t = m[i][c]
                m[i] = [(v - t * w) % p for v, w in zip(m[i], m[r])]
        pivots.append(c)
        r += 1
    free = [c for c in range(n) if c not in pivots]
    basis = []
    for fcol in free:
        x = [0] * n
        x[fcol] = 1
        for i, c in enumerate(pivots):
            x[c] = -m[i][fcol] % p
        basis.append(x)
    return basis


def reed_solomon_generator(n: int, k: int, p: int) -> List[List[int]]:
    """k x n Vandermonde generator over GF(p): row i is (a_0^i, ..., a_(n-1)^i), a_j = j."""
    return [[pow(j, i, p) for j in range(n)] for i in range(k)]


def encode(m: Sequence[int], g: Sequence[Sequence[int]], p: int) -> List[int]:
    return [sum(mi * row[j] for mi, row in zip(m, g)) % p for j in range(len(g[0]))]
