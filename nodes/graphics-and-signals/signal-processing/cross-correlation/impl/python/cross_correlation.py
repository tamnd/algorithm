# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cross-correlation/. The authors are listed in prov/ST8WA2.jsonl.

"""Cross-correlation of two finite signals, by the defining sum and by the FFT.

The convention is r_xy[k] = sum over n of x[n + k] conj(y[n]), so a peak at
a positive lag k means that x is y delayed by k samples. The lags run from
-(len(y) - 1) to len(x) - 1; outside that range every term is zero.
"""

import cmath
from typing import Sequence


def _conj(v):
    return v.conjugate() if isinstance(v, complex) else v


def cross_correlation(x: Sequence, y: Sequence) -> tuple[list[int], list]:
    """Return (lags, r) with r[i] = sum over n of x[n + lags[i]] conj(y[n]).

    No scaling is applied. With int or Fraction input the result is exact.
    Cost: O(len(x) len(y)) operations.
    """
    nx, ny = len(x), len(y)
    if nx == 0 or ny == 0:
        return [], []
    lags = list(range(-(ny - 1), nx))
    out = []
    for k in lags:
        s = 0
        for j in range(max(0, -k), min(ny, nx - k)):
            s += x[j + k] * _conj(y[j])
        out.append(s)
    return lags, out


def fft(a: Sequence[complex], inverse: bool = False) -> list[complex]:
    """Radix-2 iterative FFT. len(a) must be a power of two. Cost: O(L log L)."""
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
    sign = 1 if inverse else -1
    length = 2
    while length <= size:
        w_len = cmath.exp(sign * 2j * cmath.pi / length)
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
    if inverse:
        out = [v / size for v in out]
    return out


def cross_correlation_fft(x: Sequence[complex], y: Sequence[complex]) -> tuple[list[int], list[complex]]:
    """The same values as cross_correlation, from the inverse DFT of X conj(Y).

    Both signals are padded to a power of two L >= len(x) + len(y) - 1,
    so the circular correlation has no wrap-around; the negative lags sit
    at the end of the inverse DFT. Cost: O(L log L).
    """
    nx, ny = len(x), len(y)
    if nx == 0 or ny == 0:
        return [], []
    size = 1
    while size < nx + ny - 1:
        size <<= 1
    fx = fft(list(x) + [0] * (size - nx))
    fy = fft(list(y) + [0] * (size - ny))
    raw = fft([a * b.conjugate() for a, b in zip(fx, fy)], inverse=True)
    real_input = all(not isinstance(v, complex) for v in list(x) + list(y))
    lags = list(range(-(ny - 1), nx))
    out = [raw[k % size].real if real_input else raw[k % size] for k in lags]
    return lags, out


def estimate_delay(x: Sequence, y: Sequence) -> int:
    """The lag k that maximizes |r_xy[k]|: the delay of x against y.

    Ties go to the smallest lag. Cost: that of cross_correlation_fft.
    """
    lags, r = cross_correlation_fft(x, y)
    if not lags:
        raise ValueError("both signals must be non-empty")
    best = 0
    for i in range(1, len(r)):
        if abs(r[i]) > abs(r[best]):
            best = i
    return lags[best]


def correlation_coefficient(x: Sequence[float], y: Sequence[float]) -> tuple[list[int], list[float]]:
    """r_xy[k] divided by sqrt(r_xx[0] r_yy[0]); each value lies in [-1, 1].

    This is the global normalization of two whole signals, by Cauchy-Schwarz.
    It is not the windowed normalization of image template matching.
    """
    ex = sum(abs(v) ** 2 for v in x)
    ey = sum(abs(v) ** 2 for v in y)
    if ex == 0 or ey == 0:
        raise ValueError("both signals must have nonzero energy")
    lags, r = cross_correlation(x, y)
    scale = (ex * ey) ** 0.5
    return lags, [v / scale for v in r]
