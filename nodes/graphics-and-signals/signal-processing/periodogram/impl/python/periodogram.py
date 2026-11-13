# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/periodogram/. The authors are listed in prov/6S1Y6B.jsonl.

"""The periodogram, raw or with a data window, on an L-point frequency grid.

The frequency of bin m is w_m = 2 pi m / L radians per sample, which is
m fs / L Hz for a sampling rate fs.
"""

import cmath
from typing import Sequence


def fft(a: Sequence[complex]) -> list[complex]:
    """Radix-2 iterative FFT, A[m] = sum of a[n] e^(-2 pi i m n / L). L must be a power of two."""
    size = len(a)
    if size == 0 or size & (size - 1):
        raise ValueError("length must be a power of two")
    out = [complex(v) for v in a]
    j = 0
    for i in range(1, size):
        bit = size >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            out[i], out[j] = out[j], out[i]
    length = 2
    while length <= size:
        w_len = cmath.exp(-2j * cmath.pi / length)
        half = length // 2
        for start in range(0, size, length):
            w = 1 + 0j
            for t in range(half):
                u = out[start + t]
                v = out[start + t + half] * w
                out[start + t] = u + v
                out[start + t + half] = u - v
                w *= w_len
        length <<= 1
    return out


def dft(a: Sequence[complex]) -> list[complex]:
    """The direct DFT of any length, in O(L^2) operations."""
    size = len(a)
    return [sum(v * cmath.exp(-2j * cmath.pi * m * k / size) for k, v in enumerate(a)) for m in range(size)]


def periodogram(x: Sequence[complex], size: int | None = None, window: Sequence[float] | None = None) -> list[float]:
    """Return P[0], ..., P[L - 1] with P[m] = |sum of w[n] x[n] e^(-i w_m n)|^2 / (N U).

    U = (1/N) sum of w[n]^2, so U = 1 for the rectangular window (the raw
    periodogram) and the estimate of white noise of variance s^2 has mean
    s^2 for every window. L defaults to N and must be >= N.
    Cost: O(L log L) when L is a power of two, else O(L^2) for the direct DFT.
    """
    n = len(x)  # @line L1
    if n == 0:
        raise ValueError("x must be non-empty")
    if size is None:
        size = n
    if size < n:
        raise ValueError("size must be at least N")
    if window is None:
        window = [1.0] * n
    if len(window) != n:
        raise ValueError("window must have N samples")
    u = sum(v * v for v in window) / n  # @line L2
    if u == 0:
        raise ValueError("window must not be all zero")
    a = [window[k] * x[k] for k in range(n)] + [0] * (size - n)  # @line L3
    spec = fft(a) if size & (size - 1) == 0 else dft(a)  # @line L4
    p = [abs(v) ** 2 / (n * u) for v in spec]  # @line L5
    return p  # @line L6


def frequencies(size: int) -> list[float]:
    """w_m = 2 pi m / L in radians per sample, mapped to [-pi, pi)."""
    out = []
    for m in range(size):
        w = 2 * cmath.pi * m / size
        out.append(w - 2 * cmath.pi if w >= cmath.pi else w)
    return out


def hann(n: int) -> list[float]:
    """The periodic Hann window 0.5 - 0.5 cos(2 pi k / N)."""
    return [0.5 - 0.5 * cmath.cos(2 * cmath.pi * k / n).real for k in range(n)]
