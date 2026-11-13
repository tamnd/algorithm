# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/welch-method/. The authors are listed in prov/N8KZKA.jsonl.

"""Welch's averaged modified periodogram, and Bartlett's method as its special case.

Bin m of the output is the frequency w_m = 2 pi m / L radians per sample,
that is m fs / L Hz for a sampling rate fs.
"""

import cmath
import math
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


def hann(m: int) -> list[float]:
    """The periodic Hann window 0.5 - 0.5 cos(2 pi n / M)."""
    return [0.5 - 0.5 * math.cos(2 * math.pi * n / m) for n in range(m)]


def segment_count(n: int, m: int, d: int) -> int:
    """K = floor((N - M) / D) + 1 segments of length M with hop D fit in N samples."""
    if not 1 <= m <= n or d < 1:
        raise ValueError("need 1 <= M <= N and D >= 1")
    return (n - m) // d + 1


def welch(x: Sequence[complex], m: int, d: int, window: Sequence[float] | None = None, size: int | None = None) -> list[float]:
    """Average of the modified periodograms of the K segments x[iD .. iD + M - 1].

    Each segment is multiplied by the window, padded to L = size (default M,
    a power of two) and transformed; bin values are divided by M U with
    U = (1/M) sum of w^2. Samples after the last full segment are not used.
    Cost: O(K L log L) operations, K = floor((N - M) / D) + 1.
    """
    if window is None:
        window = [1.0] * m
    if len(window) != m:
        raise ValueError("window must have M samples")
    if size is None:
        size = m
    if size < m:
        raise ValueError("size must be at least M")
    k = segment_count(len(x), m, d)  # @line L1
    u = sum(v * v for v in window) / m  # @line L2
    if u == 0:
        raise ValueError("window must not be all zero")
    s = [0.0] * size  # @line L3
    for i in range(k):  # @line L4
        a = [window[t] * x[i * d + t] for t in range(m)] + [0] * (size - m)  # @line L5
        spec = fft(a)  # @line L6
        for b in range(size):  # @line L7
            s[b] += abs(spec[b]) ** 2 / (m * u)
    s = [v / k for v in s]  # @line L8
    return s  # @line L9


def bartlett(x: Sequence[complex], m: int, size: int | None = None) -> list[float]:
    """Bartlett's method: rectangular window and no overlap (D = M)."""
    return welch(x, m, m, None, size)


def overlap_correlation(window: Sequence[float], d: int, j: int) -> float:
    """rho_j = (sum of w[n] w[n + jD])^2 / (sum of w^2)^2, the correlation of segment
    periodograms j hops apart on white Gaussian noise (away from bins 0 and M/2)."""
    m = len(window)
    num = sum(window[t] * window[t + j * d] for t in range(m - j * d)) if j * d < m else 0.0
    den = sum(v * v for v in window)
    return (num / den) ** 2


def variance_factor(window: Sequence[float], d: int, k: int) -> float:
    """Var(S_hat) / S^2 for white Gaussian noise: (1/K) (1 + 2 sum_{j>=1} (1 - j/K) rho_j)."""
    total = 1.0
    for j in range(1, k):
        rho = overlap_correlation(window, d, j)
        if rho == 0:
            break
        total += 2 * (1 - j / k) * rho
    return total / k
