# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/empirical-transfer-function-estimate/. The authors are listed in prov/H22G0R.jsonl.

"""Empirical transfer function estimate (ETFE), raw and smoothed.

For N samples of input u and output y, with the discrete Fourier transforms

    U_k = sum over t of u(t) e^(-i w_k t),  Y_k = the same for y,
    w_k = 2 pi k / N,

the raw ETFE at w_k is G_k = Y_k / U_k. It is undefined where U_k = 0.

The smoothed ETFE with a Hann window of half width gamma is

    G_k = sum_j W_j Y_(k+j) conj(U_(k+j)) / sum_j W_j |U_(k+j)|^2,
    W_j = (1 + cos(pi j / (gamma + 1))) / 2 for |j| <= gamma,

with the indices taken modulo N. This is the |U|^2-weighted average of
the raw values over nearby frequencies.

Precondition: len(y) == len(u) = N >= 1 and 0 <= gamma < N / 2.

Cost: O(N log N) for the transforms when N is a power of 2 (O(N^2) by the
direct sum otherwise), O(N) for the raw ratios and O(N gamma) for the
smoothing, in the real RAM.
"""

import cmath
import math
from typing import List, Optional, Sequence, Tuple


def dft(x: Sequence) -> List[complex]:
    """Return X_k = sum_t x(t) e^(-2 pi i k t / N) for k = 0, ..., N-1.

    Uses the iterative radix-2 FFT when N is a power of 2, and the direct
    O(N^2) sum otherwise.
    """
    n = len(x)
    if n == 0:
        return []
    if n & (n - 1):
        return [sum(x[t] * cmath.exp(-2j * math.pi * k * t / n) for t in range(n)) for k in range(n)]
    a = [complex(v) for v in x]
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    while size <= n:
        w_step = cmath.exp(-2j * math.pi / size)
        half = size // 2
        for start in range(0, n, size):
            w = 1 + 0j
            for k in range(half):
                p = a[start + k]
                q = a[start + k + half] * w
                a[start + k] = p + q
                a[start + k + half] = p - q
                w *= w_step
        size *= 2
    return a


def etfe(y: Sequence, u: Sequence, gamma: int = 0,
         tol: float = 1e-12) -> List[Tuple[float, Optional[complex]]]:
    """Return [(w_k, G_k)] for k = 0, ..., N // 2.

    gamma = 0 gives the raw ETFE; G_k is None where |U_k| <= tol * max|U|.
    gamma > 0 gives the smoothed ETFE; G_k is None where the weighted sum of
    |U|^2 is 0.
    """
    n = len(u)
    if len(y) != n or n == 0:
        raise ValueError("y and u must have the same positive length")
    if gamma < 0 or (gamma > 0 and 2 * gamma >= n):
        raise ValueError("need 0 <= gamma < N / 2")
    yk = dft(y)  # @line L1
    uk = dft(u)
    big = max(abs(v) for v in uk)
    out = []
    for k in range(n // 2 + 1):  # @line L2
        w = 2 * math.pi * k / n
        if gamma == 0:
            if abs(uk[k]) <= tol * big:  # @line L3
                out.append((w, None))
            else:
                out.append((w, yk[k] / uk[k]))  # @line L4
            continue
        num = 0j  # @line L5
        den = 0.0
        for j in range(-gamma, gamma + 1):
            wj = 0.5 * (1 + math.cos(math.pi * j / (gamma + 1)))
            m = (k + j) % n
            num += wj * yk[m] * uk[m].conjugate()  # @line L6
            den += wj * abs(uk[m]) ** 2
        out.append((w, num / den if den > 0 else None))
    return out  # @line L7
