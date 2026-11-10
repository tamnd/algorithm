# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shared-memory-bank-conflicts/.
"""Bank conflicts of shared memory with 32 banks of 4-byte words.

Model (CUDA Programming Guide v13.5, Section 2.3.4.2): word address a is in bank a mod 32. One warp
access is served in as many passes as the largest number of distinct words that its lanes request
from one bank. Lanes that read the same word share one broadcast.
"""

from math import gcd

WARP_SIZE = 32
BANKS = 32


def degree(word_addrs):
    """The conflict degree of one warp access: max over banks of the distinct words in that bank."""
    per_bank = {}
    for a in word_addrs:
        per_bank.setdefault(a % BANKS, set()).add(a)
    return max((len(v) for v in per_bank.values()), default=0)


def strided_degree(stride):
    """Lane l reads word stride * l (stride >= 1). The degree is gcd(stride, 32)."""
    return gcd(stride, BANKS)


def transpose_tile(tile, pad):
    """Transpose a 32 x 32 tile through shared memory, as one block of 32 x 32 threads.

    Phase 1: thread (x, y) writes tile[y][x] to smem[y * width + x].
    __syncthreads()
    Phase 2: thread (x, y) reads smem[x * width + y] and writes it to out[y][x].
    The rows of threads (fixed y, x = 0..31) are the warps. Returns (out, degrees of phase 1,
    degrees of phase 2), one degree per warp.
    """
    n = WARP_SIZE
    width = n + pad
    smem = [None] * (n * width)
    d1, d2 = [], []
    for y in range(n):  # phase 1, warp y
        addrs = [y * width + x for x in range(n)]
        for x, a in enumerate(addrs):
            smem[a] = tile[y][x]
        d1.append(degree(addrs))
    out = [[None] * n for _ in range(n)]  # the barrier: phase 2 starts after all of phase 1
    for y in range(n):  # phase 2, warp y
        addrs = [x * width + y for x in range(n)]
        for x, a in enumerate(addrs):
            out[y][x] = smem[a]
        d2.append(degree(addrs))
    return out, d1, d2


def column_degree(width, rows=WARP_SIZE, col=0):
    """Degree of a warp that reads column col of a row-major array with the given row width."""
    return degree([r * width + col for r in range(rows)])
