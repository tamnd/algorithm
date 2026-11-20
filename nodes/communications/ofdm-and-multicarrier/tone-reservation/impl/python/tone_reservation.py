# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tone-reservation/. The authors are listed in prov/N335YA.jsonl.

"""Tone reservation (Tellado) with the peak-cancelling kernel.

A set R of subcarriers carries no data. The transmitter adds a signal c whose
spectrum lies only on R, so the data subcarriers are untouched and the receiver
simply ignores R. The kernel p is the oversampled time signal of the indicator
of R, scaled so that p[0] = 1. A circular shift of p by m samples still has its
spectrum on R. Each iteration finds the largest sample of x + c and subtracts
the shifted kernel times the excess over the threshold A, which sets that
sample to magnitude A exactly. The FFT is a radix-2 FFT, so N and L must be
powers of two.
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


def kernel(n: int, reserved: Sequence[int], L: int) -> list[complex]:
    """The oversampled time signal of the indicator of the reserved set, with p[0] = 1."""
    ind = [0j] * n
    for k in reserved:
        ind[k] = 1 + 0j
    s = math.sqrt(n) / len(reserved)
    return [v * s for v in to_time(ind, L)]


def tone_reservation(X: Sequence[complex], reserved: Sequence[int], L: int, a: float, iterations: int) -> tuple[list[complex], list[complex]]:
    """Return the oversampled symbol x + c and the N subcarrier values of c (zero off the reserved set).

    X must be zero on the reserved subcarriers. a is the target peak magnitude.
    """
    if any(X[k] != 0 for k in reserved):
        raise ValueError("the reserved subcarriers must carry no data")
    x = to_time(X, L)  # @line L1
    p = kernel(len(X), reserved, L)  # @line L2
    size = len(x)
    c = [0j] * size  # @line L3
    for _ in range(iterations):  # @line L4
        m = max(range(size), key=lambda t: abs(x[t] + c[t]))  # @line L5
        v = x[m] + c[m]
        if abs(v) <= a:  # @line L6
            break
        alpha = v * (1.0 - a / abs(v))  # @line L7
        for t in range(size):  # @line L8
            c[t] -= alpha * p[(t - m) % size]
    return [u + w for u, w in zip(x, c)], to_bins(c, L)  # @line L9
