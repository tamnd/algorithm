# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stern-algorithm/. The authors are listed in prov/3YXVP5.jsonl.
"""Stern's information set decoder over GF(2), in the syndrome form.

A binary matrix is a list of rows, and each row is a Python int whose bit j is
the entry in column j. H has r = n - k rows, and the syndrome s is an int with
r bits (bit i belongs to row i).

stern() finds e with H e = s and weight w. Each round makes r random columns
the identity, splits the other k columns into two halves, and looks for p
error positions in each half whose column sums agree with s' on a window of
l rows. A dictionary finds the agreeing pairs (a birthday collision). The rest
of the error, w - 2p positions, must lie on the other r - l identity columns.

This is the syndrome decoding form of Stern's algorithm, as used by Bernstein,
Lange and Peters (2008). Stern's 1989 paper states the same method for finding
a low weight codeword.

For study only. The code is not constant time, uses the random module, and
runs only on toy sizes. Use a vetted library, for example a FIPS 140
validated module, to protect real data.
"""

import random
from itertools import combinations
from math import comb
from typing import Dict, List, Optional, Sequence, Tuple


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

    Returns (U H, U s), with row i pivoting on cols[i], or None if the columns
    are singular.
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


def build(cols: Sequence[int], t: int, a: Sequence[int]) -> int:
    """The vector with e_I = t (in pivot order) and ones on the positions a."""
    e = 0
    for i, c in enumerate(cols):
        if (t >> i) & 1:
            e |= 1 << c
    for j in a:
        e |= 1 << j
    return e


def stern(h: Sequence[int], s: int, n: int, w: int, p: int, l: int, rng: random.Random,
          max_iter: int = 1_000_000) -> Tuple[Optional[int], int, int]:
    """Stern's algorithm with parameters p and l.

    Precondition: H has r = n - k rows of n bits and rank r, 2p <= w, l <= r.
    Returns (e, rounds, work): e has H e = s and weight w, or e is None after
    max_iter rounds. Only rounds with an invertible column set are counted.
    work counts the column sums formed: the list entries and the collisions.
    """
    r = len(h)
    window = (1 << l) - 1                                  # rows 0 .. l-1
    rounds = draws = work = 0
    while rounds < max_iter and draws < 8 * max_iter:      # @line L1
        draws += 1
        cols = rng.sample(range(n), r)                     # @line L2
        chosen = set(cols)
        info = [j for j in range(n) if j not in chosen]
        rng.shuffle(info)
        j1, j2 = info[: len(info) // 2], info[len(info) // 2:]
        res = eliminate(h, s, cols)                        # @line L3
        if res is None:                                    # @line L4
            continue
        rounds += 1
        rows, s2 = res
        hcol = {j: column(rows, j) for j in info}
        table: Dict[int, List[Tuple[Tuple[int, ...], int]]] = {}
        for a1 in combinations(j1, p):                     # @line L5
            v = s2
            for j in a1:
                v ^= hcol[j]
            table.setdefault(v & window, []).append((a1, v))
            work += 1
        for a2 in combinations(j2, p):                     # @line L6
            u = 0
            for j in a2:
                u ^= hcol[j]
            work += 1
            for a1, v in table.get(u & window, ()):        # @line L7
                t = v ^ u                                  # @line L8
                work += 1
                if weight(t) == w - 2 * p:                 # @line L9
                    return build(cols, t, a1 + a2), rounds, work  # @line L10
    return None, rounds, work


def success_probability(n: int, k: int, w: int, p: int, l: int) -> float:
    """C(k1, p) C(k2, p) C(n - k - l, w - 2p) / C(n, w), with k1 = k // 2 and k2 = k - k1."""
    k1 = k // 2
    k2 = k - k1
    return comb(k1, p) * comb(k2, p) * comb(n - k - l, w - 2 * p) / comb(n, w)


def lee_brickell(h: Sequence[int], s: int, n: int, w: int, p: int, rng: random.Random,
                 max_iter: int = 1_000_000) -> Tuple[Optional[int], int, int]:
    """A local copy of the Lee-Brickell algorithm, for the comparison in the tests.

    Returns (e, rounds, work), where work counts the candidate vectors formed.
    """
    r = len(h)
    rounds = draws = work = 0
    while rounds < max_iter and draws < 8 * max_iter:
        draws += 1
        cols = rng.sample(range(n), r)
        chosen = set(cols)
        info = [j for j in range(n) if j not in chosen]
        res = eliminate(h, s, cols)
        if res is None:
            continue
        rounds += 1
        rows, s2 = res
        hcol = {j: column(rows, j) for j in info}
        for size in range(p + 1):
            for a in combinations(info, size):
                t = s2
                for j in a:
                    t ^= hcol[j]
                work += 1
                if weight(t) == w - size:
                    return build(cols, t, a), rounds, work
    return None, rounds, work


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
