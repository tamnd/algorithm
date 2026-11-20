# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-doppler-processing/. The authors are listed in prov/YRN86W.jsonl.

"""Range-Doppler processing of a coherent pulse train.

X[p][n] is the complex baseband sample n (fast time, n = 0 .. N-1) of pulse p
(slow time, p = 0 .. P-1). The transmitted pulse is s[0..L-1], L <= N.

1. Fast time: the matched filter of each pulse, written as a correlation,
   z[p][r] = sum over l of conj(s[l]) X[p][r + l], r = 0 .. N - L.
   An echo that starts at sample r0 peaks at r = r0.
2. Slow time: in each range bin, a window w[p] and a DFT over the P pulses,
   D[k][r] = sum over p of w[p] z[p][r] e^(-j 2 pi k p / P), by a radix-2 FFT.

A target with Doppler frequency f_d at the pulse repetition frequency PRF
falls in Doppler bin round(f_d P / PRF) mod P. The DFT has no 1/P factor.
"""

import cmath
import math
from typing import Sequence


def fft(x: Sequence[complex]) -> list[complex]:
    """X[k] = sum_n x[n] e^(-j 2 pi k n / P), iterative radix-2, P a power of two.

    Cost: Theta(P log P) complex operations, Theta(P) space.
    """
    n = len(x)
    if n == 0 or n & (n - 1):
        raise ValueError("the length must be a power of two")
    a = [complex(v) for v in x]
    j = 0
    for i in range(1, n):  # bit reversal permutation
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    while size <= n:
        step = cmath.exp(-2j * math.pi / size)
        half = size // 2
        tw = [step ** t for t in range(half)]
        for start in range(0, n, size):
            for t in range(half):
                u = a[start + t]
                v = a[start + t + half] * tw[t]
                a[start + t] = u + v
                a[start + t + half] = u - v
        size *= 2
    return a


def hamming(p_count: int) -> list[float]:
    """The Hamming window 0.54 - 0.46 cos(2 pi p / (P - 1)), p = 0 .. P-1."""
    if p_count == 1:
        return [1.0]
    return [0.54 - 0.46 * math.cos(2 * math.pi * p / (p_count - 1)) for p in range(p_count)]


def range_doppler(x: Sequence[Sequence[complex]], s: Sequence[complex],
                  w: Sequence[float] | None = None) -> list[list[complex]]:
    """The range-Doppler map D[k][r], k = 0 .. P-1 (Doppler bin), r = 0 .. N-L (range bin).

    x holds P pulses of N samples each, P a power of two; s is the pulse of
    length L <= N; w is the slow-time window (default: all ones).
    Cost: Theta(P (N - L + 1) L) for the matched filters plus
    Theta((N - L + 1) P log P) for the FFTs; Theta(P N) space.
    """
    p_count = len(x)
    if p_count == 0:
        return []
    n = len(x[0])
    length = len(s)
    if not 1 <= length <= n or any(len(row) != n for row in x):
        raise ValueError("need 1 <= L <= N and pulses of equal length")
    if w is None:
        w = [1.0] * p_count
    sc = [complex(v).conjugate() for v in s]
    bins = n - length + 1
    z = [[0j] * bins for _ in range(p_count)]
    for p in range(p_count):  # @line L1
        row = x[p]
        for r in range(bins):  # @line L2
            z[p][r] = sum(sc[l] * row[r + l] for l in range(length))  # @line L3
    d =[[0j] * bins for _ in range(p_count)]
    for r in range(bins):  # @line L4
        u = [w[p] * z[p][r] for p in range(p_count)]  # @line L5
        col = fft(u)  # @line L6
        for k in range(p_count):
            d[k][r] = col[k]
    return d  # @line L7


def range_doppler_direct(x, s, w=None) -> list[list[complex]]:
    """The same map by the double sum over pulses and pulse samples, without an FFT."""
    p_count, n, length = len(x), len(x[0]), len(s)
    if w is None:
        w = [1.0] * p_count
    bins = n - length + 1
    out = [[0j] * bins for _ in range(p_count)]
    for k in range(p_count):
        for r in range(bins):
            acc = 0j
            for p in range(p_count):
                ph = cmath.exp(-2j * math.pi * k * p / p_count)
                for l in range(length):
                    acc += w[p] * complex(s[l]).conjugate() * x[p][r + l] * ph
            out[k][r] = acc
    return out


def point_target(p_count: int, n: int, s: Sequence[complex], delay: int, fd_over_prf: float,
                 amplitude: complex = 1.0) -> list[list[complex]]:
    """The echo a s[n - delay] e^(j 2 pi f_d p / PRF) of one point target, with no noise."""
    out = []
    for p in range(p_count):
        ph = amplitude * cmath.exp(2j * math.pi * fd_over_prf * p)
        out.append([ph * s[i - delay] if 0 <= i - delay < len(s) else 0j for i in range(n)])
    return out


def doppler_bin(fd: float, prf: float, p_count: int) -> int:
    """The Doppler bin round(f_d P / PRF) mod P of a target with Doppler frequency f_d."""
    return round(fd * p_count / prf) % p_count


def radial_velocity(fd: float, wavelength: float) -> float:
    """v = f_d lambda / 2, positive for an approaching target."""
    return fd * wavelength / 2.0
