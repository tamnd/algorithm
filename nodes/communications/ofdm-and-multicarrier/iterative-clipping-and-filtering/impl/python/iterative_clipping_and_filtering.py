# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-clipping-and-filtering/. The authors are listed in prov/CVZ52Y.jsonl.

"""Iterative clipping and filtering of an oversampled OFDM symbol (Armstrong 2002).

The symbol x = sqrt(L) F^H Z is oversampled by L: Z is X with (L - 1) N zeros
in the middle, so that the bins k >= N/2 of X stay the negative frequencies.
Each iteration clips the magnitude of every sample to A, keeps its phase, and
then removes the spectral regrowth by setting the out-of-band bins of the FFT
of size L N to zero. Clipping is the projection onto the set of signals with
|x[m]| <= A for all m, and filtering is the orthogonal projection onto the
band-limited signals, so the iteration is a method of alternating projections.
The FFT is a radix-2 FFT, so N and L must be powers of two.
"""

import cmath
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
    """sqrt(L) F^H Z for the N in-band symbols X: the symbol oversampled by L."""
    n = len(X)
    z = [0j] * (L * n)
    z[: n // 2] = [complex(v) for v in X[: n // 2]]
    z[L * n - n + n // 2:] = [complex(v) for v in X[n // 2:]]
    s = 1.0 / math.sqrt(n)
    return [v * s for v in fft(z, inverse=True)]


def to_bins(x: Sequence[complex], L: int) -> list[complex]:
    """F x / sqrt(L): all L N bins of an oversampled block, scaled like X. The inverse of to_time."""
    s = 1.0 / (L * math.sqrt(len(x) // L))
    return [v * s for v in fft(x)]


def in_band(c: Sequence[complex], n: int) -> list[complex]:
    """The N in-band bins (the first N/2 and the last N/2) of an L N point spectrum."""
    return list(c[: n // 2]) + list(c[len(c) - n // 2:])


def clip(x: Sequence[complex], a: float) -> list[complex]:
    """Limit each magnitude to a and keep the phase: the nearest point with |c[m]| <= a."""
    return [v if abs(v) <= a else a * v / abs(v) for v in x]


def clipped_energy(x: Sequence[complex], a: float) -> float:
    """sum over m of (|x[m]| - a)^2 for |x[m]| > a, the squared distance to the clipping set."""
    return sum((abs(v) - a) ** 2 for v in x if abs(v) > a)


def iterative_clipping_and_filtering(X: Sequence[complex], L: int, cr: float, iterations: int) -> tuple[list[complex], list[complex], list[float]]:
    """Clip and filter an OFDM symbol `iterations` times.

    cr is the clipping ratio A / sqrt(mean |x|^2) of the original symbol. Returns
    the final oversampled symbol, its N in-band symbols and the squared distances
    from the clipping set before each clip (the clipped-off energies).
    """
    n = len(X)
    x = to_time(X, L)  # @line L1
    a = cr * math.sqrt(sum(abs(v) ** 2 for v in x) / len(x))  # @line L2
    energies = []
    for _ in range(iterations):  # @line L3
        energies.append(clipped_energy(x, a))
        c = clip(x, a)  # @line L4
        cf = fft(c)  # @line L5
        for k in range(n // 2, L * n - n // 2):  # @line L6
            cf[k] = 0j
        x = [v / (L * n) for v in fft(cf, inverse=True)]  # @line L7
    return x, in_band(to_bins(x, L), n), energies  # @line L8
