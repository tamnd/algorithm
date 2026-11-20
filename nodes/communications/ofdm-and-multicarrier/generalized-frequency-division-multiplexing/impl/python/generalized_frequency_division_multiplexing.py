# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-frequency-division-multiplexing/. The authors are listed in prov/36P3DR.jsonl.

"""GFDM: K subcarriers and M subsymbols in one block of N = K M samples.

The data symbol d[k + m K] rides on the pulse

    a_{k,m}[n] = g[(n - m K) mod N] e^(j 2 pi k n / K),

a circular shift of the prototype g by m K samples, modulated to subcarrier
k. The block is x = A d, where the columns of A are these pulses, and one
cyclic prefix protects the whole block. The prototype here is a raised cosine
in frequency with roll-off alpha, made circular over the block. The receiver
equalizes the channel with one N-point DFT and then applies the zero-forcing
(A^-1), matched-filter (A^H) or MMSE receiver. The matrices use the shared
helper cbb.
"""

import cmath
import math
from typing import Sequence

import cbb


def rc_prototype(k: int, m: int, alpha: float) -> list[complex]:
    """The circular raised-cosine prototype of length N = K M with unit energy."""
    n = k * m
    G = []
    for i in range(n):
        f = abs((i if i <= n // 2 else i - n) / m)
        if f <= (1 - alpha) / 2:
            G.append(1.0)
        elif f <= (1 + alpha) / 2:
            G.append(0.5 * (1 + math.cos(math.pi / alpha * (f - (1 - alpha) / 2))))
        else:
            G.append(0.0)
    g = cbb.idft([complex(v) for v in G])
    e = math.sqrt(cbb.norm2(g))
    return [v / e for v in g]


def modulation_matrix(g: Sequence[complex], k: int, m: int) -> list[list[complex]]:
    """The N by N matrix A whose column k + m K is the pulse a_{k,m}."""
    n = k * m
    cols = []
    for mm in range(m):
        for kk in range(k):
            cols.append([g[(t - mm * k) % n] * cmath.exp(2j * math.pi * kk * t / k) for t in range(n)])  # @line L1
    return [[cols[c][r] for c in range(n)] for r in range(n)]


def transmit(A: Sequence[Sequence[complex]], d: Sequence[complex], cp: int) -> list[complex]:
    """One GFDM block with its cyclic prefix."""
    x = cbb.matvec(A, list(d))  # @line L2
    return x[len(x) - cp:] + x  # @line L3


def equalize(r: Sequence[complex], n: int, cp: int, h: Sequence[complex]) -> list[complex]:
    """Remove the prefix and undo a channel of at most cp + 1 taps with one N-point DFT."""
    y = cbb.dft(list(r[cp: cp + n]))  # @line L4
    hf = cbb.dft(list(h) + [0j] * (n - len(h)))
    return cbb.idft([a / b for a, b in zip(y, hf)])


def zero_forcing(A: Sequence[Sequence[complex]], x: Sequence[complex]) -> list[complex]:
    """d = A^-1 x. Raises ValueError if A is singular."""
    return cbb.solve([list(r) for r in A], list(x))  # @line L5


def matched_filter(A: Sequence[Sequence[complex]], x: Sequence[complex]) -> list[complex]:
    """A^H x: each output correlates x with one pulse."""
    return cbb.matvec(cbb.herm([list(r) for r in A]), list(x))


def mmse(A: Sequence[Sequence[complex]], x: Sequence[complex], noise_var: float) -> list[complex]:
    """(A^H A + noise_var I)^-1 A^H x, for unit-energy data."""
    Ah = cbb.herm([list(r) for r in A])
    B = cbb.add(cbb.matmul(Ah, [list(r) for r in A]), cbb.scale(noise_var, cbb.eye(len(A))))
    return cbb.solve(B, cbb.matvec(Ah, list(x)))


def channel(x: Sequence[complex], h: Sequence[complex]) -> list[complex]:
    """Linear convolution with h, cut to the length of x."""
    return cbb.conv(list(x), list(h))[: len(x)]
