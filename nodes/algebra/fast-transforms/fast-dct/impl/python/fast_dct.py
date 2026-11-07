# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-dct/. The authors are listed in prov/EWEX4W.jsonl.

import cmath
import math


def _fft(x: list[complex], inverse: bool = False) -> None:
    """In-place iterative radix-2 FFT with the root exp(-2j*pi/n), or its inverse.

    len(x) must be a power of two. The inverse includes the factor 1/n.
    """
    n = len(x)
    t = n.bit_length() - 1
    sign = 1.0 if inverse else -1.0
    table = [cmath.exp(sign * 2j * math.pi * k / n) for k in range(max(n // 2, 1))]
    rev = [0] * n
    for j in range(1, n):
        rev[j] = (rev[j >> 1] >> 1) | ((j & 1) << (t - 1))
    for j in range(n):
        if j < rev[j]:
            x[j], x[rev[j]] = x[rev[j]], x[j]
    h = 1
    while h < n:
        step = n // (2 * h)
        for s in range(0, n, 2 * h):
            for k in range(h):
                u = x[s + k]
                v = table[k * step] * x[s + k + h]
                x[s + k] = u + v
                x[s + k + h] = u - v
        h *= 2
    if inverse:
        for j in range(n):
            x[j] /= n


def fast_dct(x: list[float]) -> list[float]:
    """Return the DCT-II, X[k] = sum of x[j] * cos(pi * (2j + 1) * k / (2n)).

    Precondition: n = len(x) is a power of two and the entries are real.
    Method of Makhoul (1980): reorder, one complex FFT of length n, and a
    rotation of each output. Cost: one complex FFT of length n, about
    5 n lg n real operations, plus 3n real operations for the rotations.
    """
    n = len(x)  # @line L1
    if n < 1 or n & (n - 1):
        raise ValueError("the length must be a power of two")
    if n == 1:  # @line L2
        return [float(x[0])]
    v = [0j] * n
    for j in range(n // 2):  # @line L3
        v[j] = complex(x[2 * j])  # @line L4
        v[n - 1 - j] = complex(x[2 * j + 1])  # @line L5
    _fft(v)  # @line L6
    out = [0.0] * n
    for k in range(n):  # @line L7
        out[k] = (cmath.exp(-1j * math.pi * k / (2 * n)) * v[k]).real  # @line L8
    return out  # @line L9


def inverse_fast_dct(big_x: list[float]) -> list[float]:
    """Return x with fast_dct(x) == big_x (the scaled DCT-III).

    Precondition: as for fast_dct. Cost: one inverse complex FFT of length
    n and O(n) further real operations.
    """
    n = len(big_x)
    if n < 1 or n & (n - 1):
        raise ValueError("the length must be a power of two")
    if n == 1:
        return [float(big_x[0])]
    w = [complex(big_x[0])] + [
        cmath.exp(1j * math.pi * k / (2 * n)) * complex(big_x[k], -big_x[n - k])
        for k in range(1, n)
    ]  # @line L10
    _fft(w, inverse=True)  # @line L11
    x = [0.0] * n
    for j in range(n // 2):  # @line L12
        x[2 * j] = w[j].real
        x[2 * j + 1] = w[n - 1 - j].real
    return x
