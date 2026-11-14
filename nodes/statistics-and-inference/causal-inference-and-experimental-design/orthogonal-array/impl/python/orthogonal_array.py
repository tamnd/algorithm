# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orthogonal-array/. The authors are listed in prov/5Q12GA.jsonl.
"""Orthogonal arrays OA(N, k, s, t): checking, the Rao bound, and constructions.

An N x k array on s symbols has strength t when, in every choice of t columns, each of
the s^t possible rows occurs equally often (lambda = N / s^t times).
"""

from collections import Counter
from collections.abc import Sequence
from itertools import combinations, product
from math import comb

Array = list[tuple[int, ...]]


def has_strength(rows: Sequence[Sequence[int]], s: int, t: int) -> bool:
    """True if every t columns show each of the s^t tuples equally often."""
    n = len(rows)
    k = len(rows[0]) if rows else 0
    if t == 0:
        return True
    if n % s ** t:
        return False
    lam = n // s ** t
    for cols in combinations(range(k), t):
        cnt = Counter(tuple(r[c] for c in cols) for r in rows)
        if len(cnt) != s ** t or any(v != lam for v in cnt.values()):
            return False
    return True


def strength(rows: Sequence[Sequence[int]], s: int) -> int:
    """The largest t such that the array has strength t (strength t implies t - 1)."""
    k = len(rows[0])
    t = 0
    while t < k and has_strength(rows, s, t + 1):
        t += 1
    return t


def rao_bound(k: int, s: int, t: int) -> int:
    """Rao's lower bound on the number of runs N of an OA(N, k, s, t)."""
    u = t // 2
    bound = sum(comb(k, i) * (s - 1) ** i for i in range(u + 1))
    if t % 2:
        bound += comb(k - 1, u) * (s - 1) ** (u + 1)
    return bound


def from_linear_code(generator: Sequence[Sequence[int]], p: int) -> Array:
    """The codewords of the linear code over GF(p) (p prime) spanned by the generator
    rows, as the rows of an array: an OA of strength d' - 1, where d' is the minimum
    distance of the dual code."""
    m = len(generator)
    k = len(generator[0])
    return sorted({tuple(sum(a * g[j] for a, g in zip(msg, generator)) % p for j in range(k))
                   for msg in product(range(p), repeat=m)})


def dual_distance(generator: Sequence[Sequence[int]], p: int) -> int:
    """The minimum weight of a nonzero word orthogonal to every generator row (brute force)."""
    k = len(generator[0])
    best = k + 1
    for w in product(range(p), repeat=k):
        if any(w) and all(sum(a * b for a, b in zip(w, g)) % p == 0 for g in generator):
            best = min(best, sum(1 for a in w if a))
    return best


def from_mols(squares: Sequence[Sequence[Sequence[int]]]) -> Array:
    """An OA(n^2, m + 2, n, 2) from m mutually orthogonal Latin squares of order n:
    rows (i, j, L_1(i, j), ..., L_m(i, j))."""
    n = len(squares[0])
    return [(i, j) + tuple(sq[i][j] for sq in squares) for i in range(n) for j in range(n)]
