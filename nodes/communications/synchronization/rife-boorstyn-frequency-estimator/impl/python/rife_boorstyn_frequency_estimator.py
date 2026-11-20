# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rife-boorstyn-frequency-estimator/. The authors are listed in prov/749SAD.jsonl.

"""Rife and Boorstyn maximum likelihood frequency estimation of one complex tone.

For r[t] = A e^(j(omega t + phi)) + w[t], t = 0, ..., N-1, with unknown A, phi
and omega, and white circular Gaussian noise, the maximum likelihood estimate
of omega is the frequency that maximizes the periodogram

  P(omega) = |sum_t r[t] e^(-j omega t)|^2 / N.

The search is done in two steps: a coarse search on a zero-padded FFT grid of
K >= 4N points, then a golden-section search on the two grid cells around the
largest grid value. The result is in radians per sample, in [-pi, pi).
"""

import cmath
import math
from typing import Sequence


def fft(x: Sequence[complex]) -> list[complex]:
    """Radix-2 decimation-in-time FFT, X[k] = sum_t x[t] e^(-2 pi j k t / K); len(x) a power of 2."""
    n = len(x)
    if n & (n - 1):
        raise ValueError("length must be a power of two")
    a = list(x)
    j = 0
    for i in range(1, n):  # bit-reversal permutation
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    while size <= n:
        w = cmath.exp(-2j * math.pi / size)
        for s in range(0, n, size):
            wk = 1 + 0j
            for k in range(size // 2):
                u, v = a[s + k], a[s + k + size // 2] * wk
                a[s + k], a[s + k + size // 2] = u + v, u - v
                wk *= w
        size *= 2
    return a


def periodogram(r: Sequence[complex], omega: float) -> float:
    """P(omega) = |sum_t r[t] e^(-j omega t)|^2 / N."""
    s = sum(x * cmath.exp(-1j * omega * t) for t, x in enumerate(r))
    return abs(s) ** 2 / len(r)


def golden_max(f, a: float, b: float, tol: float) -> float:
    """The maximizer of a unimodal f on [a, b], to within tol, by golden-section search."""
    g = (math.sqrt(5.0) - 1.0) / 2.0
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = f(c), f(d)
    while b - a > tol:
        if fc >= fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = f(d)
    return (a + b) / 2.0


def rb_estimate(r: Sequence[complex], oversample: int = 4, tol: float = 1e-10) -> float:
    """The ML frequency estimate in radians per sample, in [-pi, pi)."""
    n = len(r)
    k = 1
    while k < oversample * n:
        k *= 2
    x = fft(list(r) + [0j] * (k - n))  # @line L1
    best = max(range(k), key=lambda i: abs(x[i]))  # @line L2
    a, b = 2.0 * math.pi * (best - 1) / k, 2.0 * math.pi * (best + 1) / k  # @line L3
    omega = golden_max(lambda w: periodogram(r, w), a, b, tol)  # @line L4
    return (omega + math.pi) % (2.0 * math.pi) - math.pi  # @line L5


def crb(n: int, snr: float) -> float:
    """The Cramer-Rao bound 6 / (SNR N (N^2 - 1)) on the variance of omega_hat."""
    return 6.0 / (snr * n * (n * n - 1))
