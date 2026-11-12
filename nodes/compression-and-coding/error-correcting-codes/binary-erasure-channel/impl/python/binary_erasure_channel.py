# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-erasure-channel/. The authors are listed in prov/6KVV6B.jsonl.
"""The binary erasure channel BEC(eps): each bit is erased with probability eps, independently.

A received word is a list whose entries are 0, 1 or None (an erasure). The module simulates
the channel and decodes a binary linear code by Gaussian elimination over GF(2): the message
is the unique solution of the equations that the bits that were not erased give, if there is one.
"""

import random
from typing import List, Optional, Sequence

Bit = Optional[int]


def transmit(word: Sequence[int], eps: float, rng: random.Random) -> List[Bit]:
    """Send a word through BEC(eps): each bit becomes None with probability eps."""
    return [None if rng.random() < eps else b for b in word]


def capacity(eps: float) -> float:
    """C = 1 - eps bits per channel use, reached by the uniform input."""
    return 1.0 - eps


def encode(g: Sequence[Sequence[int]], m: Sequence[int]) -> List[int]:
    """The codeword m G over GF(2) for a k x n generator matrix g."""
    n = len(g[0])
    return [sum(m[i] & g[i][j] for i in range(len(g))) & 1 for j in range(n)]


def decode(g: Sequence[Sequence[int]], received: Sequence[Bit]) -> Optional[List[int]]:
    """Recover the message from a word with erasures, or return None if it is not unique.

    Each position j that is not erased gives one linear equation sum_i m_i g[i][j] = y_j.
    Gaussian elimination over GF(2) on these equations finds m when the columns of g at
    the positions that were not erased have rank k; otherwise two messages fit and the
    decoder returns None. This is maximum likelihood decoding on the erasure channel.
    Cost: O(k^2 n) bit operations, or O(k n) word operations with packed rows.
    """
    k = len(g)
    # each equation is an integer: bits 0 .. k-1 are the coefficients, bit k is the right side
    rows = []
    for j, y in enumerate(received):
        if y is None:
            continue
        eq = 0
        for i in range(k):
            if g[i][j]:
                eq |= 1 << i
        rows.append(eq | (y << k))
    pivots = []  # (column, row)
    r = 0
    for col in range(k):
        sel = next((i for i in range(r, len(rows)) if rows[i] >> col & 1), None)
        if sel is None:
            return None  # a free variable: the message is not unique
        rows[r], rows[sel] = rows[sel], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> col & 1:
                rows[i] ^= rows[r]
        pivots.append((col, r))
        r += 1
    m = [0] * k
    for col, row in pivots:
        m[col] = rows[row] >> k & 1
    return m


def recoverable(g: Sequence[Sequence[int]], erased: Sequence[int]) -> bool:
    """True if every message survives this erasure pattern: the kept columns of g have rank k."""
    n = len(g[0])
    kept = [j for j in range(n) if j not in set(erased)]
    basis: List[int] = []  # rank of the k x |kept| submatrix over GF(2), rows as integers
    for i in range(len(g)):
        v = sum(g[i][j] << t for t, j in enumerate(kept))
        for b in basis:  # basis vectors have distinct leading bits, largest first
            v = min(v, v ^ b)
        if v:
            basis.append(v)
            basis.sort(reverse=True)
    return len(basis) == len(g)
