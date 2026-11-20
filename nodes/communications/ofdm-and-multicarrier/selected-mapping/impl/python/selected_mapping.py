# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selected-mapping/. The authors are listed in prov/GWPD9C.jsonl.

"""Selected mapping (SLM) for the PAPR of OFDM (Bauml, Fischer and Huber 1996).

The transmitter and the receiver share U phase sequences P_1, ..., P_U of
length N with entries of magnitude 1; P_1 is all ones, so plain OFDM is one of
the candidates. The transmitter multiplies the data X by each P_u, builds each
candidate symbol oversampled by L, and sends the one with the lowest PAPR and
its index. The receiver divides by the chosen sequence, which is exact because
|P_u[k]| = 1. The FFT is a radix-2 FFT, so N and L must be powers of two.
"""

import cmath
import math
import random
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


def phase_table(u: int, n: int, seed: int) -> list[list[complex]]:
    """U phase sequences with entries in {1, -1, j, -j}; the first is all ones."""
    rng = random.Random(seed)
    table = [[1 + 0j] * n]
    for _ in range(u - 1):
        table.append([rng.choice((1 + 0j, -1 + 0j, 1j, -1j)) for _ in range(n)])
    return table


def selected_mapping(X: Sequence[complex], table: Sequence[Sequence[complex]], L: int = 4) -> tuple[int, list[complex], list[float]]:
    """Return the chosen index u (0-based), its oversampled symbol and the PAPR of every candidate."""
    best, best_x, ratios = -1, None, []
    for u, p in enumerate(table):  # @line L1
        xu = [a * b for a, b in zip(X, p)]  # @line L2
        x = to_time(xu, L)  # @line L3
        r = papr(x)  # @line L4
        ratios.append(r)
        if best < 0 or r < ratios[best]:  # @line L5
            best, best_x = u, x
    return best, best_x, ratios  # @line L6


def slm_receive(Y: Sequence[complex], table: Sequence[Sequence[complex]], u: int) -> list[complex]:
    """Undo the phase sequence u on the equalized subcarrier values Y."""
    return [y * p.conjugate() for y, p in zip(Y, table[u])]
