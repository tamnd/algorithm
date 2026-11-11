# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lee-brickell-algorithm/. The authors are listed in prov/XC780W.jsonl.
"""The Lee-Brickell information set decoder over GF(2).

A binary matrix is a list of rows, and each row is a Python int whose bit j is
the entry in column j. H has r = n - k rows, and the syndrome s is an int with
r bits (bit i belongs to row i).

lee_brickell() finds e with H e = s and weight w. Each round makes r random
columns the identity, as Prange's algorithm does, and then tries every set of
at most p columns of the other k positions as the part of the error outside
the identity. With p = 0 it is Prange's algorithm.

For study only. The code is not constant time, uses the random module, and
runs only on toy sizes. Use a vetted library, for example a FIPS 140
validated module, to protect real data.
"""

import random
from itertools import combinations
from math import comb
from typing import List, Optional, Sequence, Tuple


def weight(x: int) -> int:
    """Hamming weight of an int seen as a bit vector."""
    return bin(x).count("1")


def syndrome(h: Sequence[int], e: int) -> int:
    """H e over GF(2)."""
    s = 0
    for i, row in enumerate(h):
        if weight(row & e) & 1:
            s |= 1 << i
    return s


def rank(h: Sequence[int]) -> int:
    """Rank over GF(2) of the rows of H."""
    basis: List[int] = []
    for row in h:
        for b in basis:
            row = min(row, row ^ b)
        if row:
            basis.append(row)
            basis.sort(reverse=True)
    return len(basis)


def eliminate(h: Sequence[int], s: int, cols: Sequence[int]) -> Optional[Tuple[List[int], int]]:
    """Gauss-Jordan elimination that makes the columns `cols` of H the identity.

    Returns (H', s') = (U H, U s), with row i of H' pivoting on cols[i], or
    None if those columns are singular. Cost: O(r^2) row operations.
    """
    r = len(h)
    rows = list(h)
    synd = [(s >> i) & 1 for i in range(r)]
    for i, c in enumerate(cols):
        bit = 1 << c
        piv = next((j for j in range(i, r) if rows[j] & bit), None)
        if piv is None:
            return None
        rows[i], rows[piv] = rows[piv], rows[i]
        synd[i], synd[piv] = synd[piv], synd[i]
        for j in range(r):
            if j != i and rows[j] & bit:
                rows[j] ^= rows[i]
                synd[j] ^= synd[i]
    return rows, sum(b << i for i, b in enumerate(synd))


def column(rows: Sequence[int], j: int) -> int:
    """Column j of a matrix given by rows, as an int with one bit per row."""
    c = 0
    for i, row in enumerate(rows):
        c |= ((row >> j) & 1) << i
    return c


def lee_brickell(h: Sequence[int], s: int, n: int, w: int, p: int, rng: random.Random,
                 max_iter: int = 1_000_000) -> Tuple[Optional[int], int]:
    """The Lee-Brickell algorithm with parameter p.

    Precondition: H has r = n - k rows of n bits and rank r, 0 <= w <= n,
    0 <= p <= w. Returns (e, rounds) with H e = s and weight(e) = w, or
    (None, rounds) after max_iter rounds. Only rounds with an invertible
    column set are counted. One round costs one elimination plus
    sum_{i <= p} C(k, i) additions of r-bit columns.
    """
    r = len(h)
    rounds = draws = 0
    while rounds < max_iter and draws < 8 * max_iter:     # @line L1
        draws += 1
        cols = rng.sample(range(n), r)                    # @line L2
        info = [j for j in range(n) if j not in set(cols)]
        res = eliminate(h, s, cols)                       # @line L3
        if res is None:                                   # @line L4
            continue
        rounds += 1
        rows, s2 = res
        hcol = {j: column(rows, j) for j in info}
        for size in range(p + 1):                         # @line L5
            for a in combinations(info, size):
                t = s2
                for j in a:                               # @line L6
                    t ^= hcol[j]
                if weight(t) == w - size:                 # @line L7
                    e = 0
                    for i, c in enumerate(cols):          # @line L8
                        if (t >> i) & 1:
                            e |= 1 << c
                    for j in a:
                        e |= 1 << j
                    return e, rounds                      # @line L9
    return None, rounds


def success_probability(n: int, k: int, w: int, p: int) -> float:
    """sum_{i <= p} C(k, i) C(n - k, w - i) / C(n, w): at most p errors in the k positions."""
    return sum(comb(k, i) * comb(n - k, w - i) for i in range(min(p, w) + 1)) / comb(n, w)


def random_instance(n: int, k: int, w: int, rng: random.Random) -> Tuple[List[int], int, int]:
    """A random full rank (n - k) x n matrix H, a random e of weight w, and s = H e."""
    r = n - k
    while True:
        h = [rng.getrandbits(n) for _ in range(r)]
        if rank(h) == r:
            break
    e = 0
    for c in rng.sample(range(n), w):
        e |= 1 << c
    return h, syndrome(h, e), e
