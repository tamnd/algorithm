# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-transmit-sequence/. The authors are listed in prov/JND5P6.jsonl.

"""Partial transmit sequences (PTS) for the PAPR of OFDM (Muller and Huber 1997).

The N subcarriers are split into V disjoint subblocks. Each subblock is
transformed on its own, giving V partial sequences x_v of the symbol
oversampled by L. By linearity, rotating every subcarrier of subblock v by the
same factor b_v gives the time signal sum_v b_v x_v, so each candidate costs
O(V L N) and no new FFT. The search tries every vector b in W^(V-1) with
b_1 = 1 and keeps the one with the lowest PAPR. The FFT is a radix-2 FFT, so
N and L must be powers of two.
"""

import cmath
import itertools
import math
from typing import Sequence


def fft(a: Sequence[complex], inverse: bool = False) -> list[complex]:
    """Radix-2 FFT with no scale factor: sum_n a[n] e^(-+ j 2 pi k n / n_len)."""
    n = len(a)
    if n == 0 or n & (n - 1):
        raise ValueError("the length must be a power of two")
    out = [complex(v) for v in a]
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            out[i], out[j] = out[j], out[i]
    sign = 1 if inverse else -1
    size = 2
    while size <= n:
        half = size // 2
        tw = [cmath.exp(sign * 2j * math.pi * k / size) for k in range(half)]
        for s in range(0, n, size):
            for k in range(half):
                u = out[s + k]
                v = out[s + k + half] * tw[k]
                out[s + k] = u + v
                out[s + k + half] = u - v
        size *= 2
    return out


def to_time(X: Sequence[complex], L: int) -> list[complex]:
    """sqrt(L) F^H Z: the OFDM symbol of X oversampled by L, zeros in the middle of the spectrum."""
    n = len(X)
    z = [0j] * (L * n)
    z[: n // 2] = [complex(v) for v in X[: n // 2]]
    z[L * n - n + n // 2:] = [complex(v) for v in X[n // 2:]]
    s = 1.0 / math.sqrt(n)
    return [v * s for v in fft(z, inverse=True)]


def to_bins(x: Sequence[complex], L: int) -> list[complex]:
    """The N in-band subcarrier values of an oversampled symbol: the inverse of to_time."""
    n = len(x) // L
    c = fft(x)
    s = 1.0 / (L * math.sqrt(n))
    return [v * s for v in c[: n // 2] + c[L * n - n // 2:]]


def papr(x: Sequence[complex]) -> float:
    """max |x[m]|^2 over the time average of |x[m]|^2."""
    p = [abs(v) ** 2 for v in x]
    return max(p) / (sum(p) / len(p))


def adjacent_partition(n: int, v: int) -> list[int]:
    """Subblock label of each subcarrier: V runs of N / V adjacent subcarriers."""
    return [k * v // n for k in range(n)]


def interleaved_partition(n: int, v: int) -> list[int]:
    """Subblock label of each subcarrier: subcarrier k goes to subblock k mod V."""
    return [k % v for k in range(n)]


def partial_transmit_sequence(X: Sequence[complex], labels: Sequence[int], phases: Sequence[complex], L: int = 4) -> tuple[list[complex], list[complex], float]:
    """Exhaustive PTS search. Returns the factors b (b[0] = 1), the oversampled symbol and its PAPR."""
    nv = max(labels) + 1
    parts = []
    for v in range(nv):  # @line L1
        parts.append(to_time([x if lab == v else 0j for x, lab in zip(X, labels)], L))  # @line L2
    best, best_b, best_x = math.inf, None, None  # @line L3
    for tail in itertools.product(phases, repeat=nv - 1):  # @line L4
        b = (1 + 0j,) + tail
        x = [sum(bv * p[m] for bv, p in zip(b, parts)) for m in range(len(parts[0]))]  # @line L5
        r = papr(x)  # @line L6
        if r < best:  # @line L7
            best, best_b, best_x = r, list(b), x
    return best_b, best_x, best  # @line L8


def pts_receive(Y: Sequence[complex], labels: Sequence[int], b: Sequence[complex]) -> list[complex]:
    """Undo the factor of each subblock on the equalized subcarrier values Y (|b_v| = 1)."""
    return [y * b[lab].conjugate() for y, lab in zip(Y, labels)]
