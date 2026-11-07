# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-wavelet-transform/. The authors are listed in prov/H8RGV6.jsonl.

import math

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)

HAAR = [1 / SQRT2, 1 / SQRT2]
DAUBECHIES4 = [
    (1 + SQRT3) / (4 * SQRT2),
    (3 + SQRT3) / (4 * SQRT2),
    (3 - SQRT3) / (4 * SQRT2),
    (1 - SQRT3) / (4 * SQRT2),
]


def _check(n: int, h: list[float], levels: int) -> None:
    if len(h) < 2 or len(h) % 2:
        raise ValueError("the filter length must be even and at least 2")
    if levels < 0 or n < 1 or n % (1 << levels):
        raise ValueError("the length must be divisible by 2**levels")


def fwt(x: list[float], h: list[float], levels: int) -> list[float]:
    """Return the periodic orthogonal wavelet transform of x with `levels` levels.

    h is an orthonormal low-pass filter of even length L, that is
    sum(h[l] * h[l + 2s]) is 1 for s = 0 and 0 otherwise; the high-pass filter
    is g[l] = (-1)**l * h[L - 1 - l]. len(x) must be divisible by 2**levels.
    The output is [a_J, d_J, d_(J-1), ..., d_1], coarsest first.
    Cost: at most 2Ln multiplications and 2(L - 1)n additions, so O(n).
    """
    n, big_l = len(x), len(h)  # @line L1
    _check(n, h, levels)
    g = [(-1) ** l * h[big_l - 1 - l] for l in range(big_l)]  # @line L2
    a, m = [float(v) for v in x], n  # @line L3
    y = [0.0] * n
    for _ in range(levels):  # @line L4
        half = m // 2
        s = [0.0] * half
        d = [0.0] * half
        for i in range(half):  # @line L5
            s[i] = sum(h[l] * a[(2 * i + l) % m] for l in range(big_l))  # @line L6
            d[i] = sum(g[l] * a[(2 * i + l) % m] for l in range(big_l))  # @line L7
        y[half:m], a, m = d, s, half  # @line L8
    y[0:m] = a  # @line L9
    return y  # @line L10


def inverse_fwt(y: list[float], h: list[float], levels: int) -> list[float]:
    """Return x with fwt(x, h, levels) == y, by the transposed filter bank.

    Same preconditions as fwt. Cost: the same as fwt.
    """
    n, big_l = len(y), len(h)
    _check(n, h, levels)
    g = [(-1) ** l * h[big_l - 1 - l] for l in range(big_l)]
    m = n >> levels  # @line L11
    a = [float(v) for v in y[0:m]]
    for _ in range(levels):  # @line L12
        b = [0.0] * (2 * m)  # @line L13
        for i in range(m):  # @line L14
            for l in range(big_l):
                b[(2 * i + l) % (2 * m)] += h[l] * a[i] + g[l] * y[m + i]
        a, m = b, 2 * m  # @line L15
    return a  # @line L16
