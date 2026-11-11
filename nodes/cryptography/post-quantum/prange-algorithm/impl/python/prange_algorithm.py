# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prange-algorithm/. The authors are listed in prov/HA6A5G.jsonl.
"""Prange's information set decoding over GF(2).

A binary matrix is a list of rows, and each row is a Python int whose bit j is
the entry in column j. A vector of length n is an int with n bits. The parity
check matrix H has r = n - k rows, and the syndrome s is an int with r bits
(bit i belongs to row i).

prange() finds e with H e = s and weight w, if it finds one within max_iter
iterations. Each iteration picks r random columns, makes them the identity by
Gaussian elimination, and hopes that the whole error lies on them.

For study only. The code is not constant time, uses the random module, and
runs only on toy sizes. It is an attack tool for small examples, not a
library. Use a vetted library, for example a FIPS 140 validated module, to
protect real data.
"""

import random
from math import comb
from typing import List, Optional, Sequence, Tuple


def weight(x: int) -> int:
    """Hamming weight of an int seen as a bit vector."""
    return bin(x).count("1")


def syndrome(h: Sequence[int], e: int) -> int:
    """H e over GF(2): bit i is the parity of row i AND e."""
    s = 0
    for i, row in enumerate(h):
        if weight(row & e) & 1:
            s |= 1 << i
    return s


def rank(h: Sequence[int]) -> int:
    """Rank over GF(2) of the rows of H (rows as ints)."""
    basis: List[int] = []
    for row in h:
        for b in basis:
            row = min(row, row ^ b)
        if row:
            basis.append(row)
            basis.sort(reverse=True)
    return len(basis)


def eliminate(h: Sequence[int], s: int, cols: Sequence[int]) -> Optional[Tuple[List[int], int]]:
    """Gaussian elimination that turns the columns `cols` of H into the identity.

    Returns (H', s') with H' = U H and s' = U s for an invertible U, where row i
    of H' has a 1 in column cols[i] and 0 in the other columns of `cols`.
    Returns None if the r x r submatrix on `cols` is singular. Cost: O(r^2)
    row operations on n-bit ints.
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
    s2 = 0
    for i in range(r):
        s2 |= synd[i] << i
    return rows, s2


def prange(h: Sequence[int], s: int, n: int, w: int, rng: random.Random,
           max_iter: int = 1_000_000) -> Tuple[Optional[int], int]:
    """Prange's algorithm.

    Precondition: H has r = n - k rows of n bits, s has r bits, 0 <= w <= r.
    Returns (e, iterations): e has weight w and H e = s, or e is None when
    max_iter iterations fail. Only iterations whose r columns are independent
    are counted. Expected count: C(n, w) / C(r, w) when the solution is unique.
    """
    r = len(h)
    iterations = draws = 0
    while iterations < max_iter and draws < 8 * max_iter:  # @line L1
        draws += 1
        cols = rng.sample(range(n), r)                 # @line L2
        res = eliminate(h, s, cols)                    # @line L3
        if res is None:                                # @line L4
            continue
        iterations += 1
        _, s2 = res                                    # @line L5
        if weight(s2) == w:                            # @line L6
            e = 0
            for i, c in enumerate(cols):               # @line L7
                if (s2 >> i) & 1:
                    e |= 1 << c
            return e, iterations                       # @line L8
    return None, iterations


def success_probability(n: int, k: int, w: int) -> float:
    """C(n - k, w) / C(n, w): the chance that a random set of n - k positions holds all w errors."""
    return comb(n - k, w) / comb(n, w)


def random_instance(n: int, k: int, w: int, rng: random.Random) -> Tuple[List[int], int, int]:
    """A uniform random (n - k) x n matrix H of full rank n - k, a random e of weight w, and s = H e."""
    r = n - k
    while True:
        h = [rng.getrandbits(n) for _ in range(r)]
        if rank(h) == r:
            break
    e = 0
    for c in rng.sample(range(n), w):
        e |= 1 << c
    return h, syndrome(h, e), e
