# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-wavelet-transform/. The authors are listed in prov/CM5P8S.jsonl.

"""Multilevel discrete wavelet transform with a two-channel filter bank.

A filter is a dict that maps a tap index (which may be negative) to a
coefficient. The analysis filters ht (low-pass) and gt (high-pass) act by
correlation and downsampling, the synthesis filters h and g by upsampling and
convolution. Indices wrap around (periodic extension), so each level needs an
even length. The code works for any number type with + and *, for example
float, Fraction, or an exact type for numbers a + b sqrt(2).
"""

from fractions import Fraction
from typing import Any

Filter = dict[int, Any]


def analysis_step(a: list, ht: Filter, gt: Filter) -> tuple[list, list]:
    """One level: s[i] = sum_l ht[l] a[2i + l], d[i] = sum_l gt[l] a[2i + l], indices mod len(a)."""
    m = len(a)
    if m % 2:
        raise ValueError("each level needs an even length")
    s, d = [], []
    for i in range(m // 2):  # @line L6
        acc_s = 0
        for l, c in ht.items():  # @line L7
            acc_s = acc_s + c * a[(2 * i + l) % m]
        acc_d = 0
        for l, c in gt.items():  # @line L8
            acc_d = acc_d + c * a[(2 * i + l) % m]
        s.append(acc_s)
        d.append(acc_d)
    return s, d  # @line L9


def synthesis_step(s: list, d: list, h: Filter, g: Filter) -> list:
    """Inverse of one level: out[2i + l] += h[l] s[i] + g[l] d[i], indices mod 2 len(s)."""
    m = 2 * len(s)
    out: list = [0] * m  # @line L13
    for i in range(len(s)):  # @line L14
        for l, c in h.items():  # @line L15
            out[(2 * i + l) % m] = out[(2 * i + l) % m] + c * s[i]
        for l, c in g.items():
            out[(2 * i + l) % m] = out[(2 * i + l) % m] + c * d[i]
    return out  # @line L16


def dwt(x: list, ht: Filter, gt: Filter, levels: int) -> tuple[list, list[list]]:
    """Return (a, details): the coarse approximation after `levels` levels and the
    detail blocks, finest first. len(x) must be divisible by 2**levels."""
    if levels < 0 or len(x) % (1 << levels):
        raise ValueError("len(x) must be divisible by 2**levels")
    a = list(x)  # @line L1
    details: list[list] = []
    for _ in range(levels):  # @line L2
        a, d = analysis_step(a, ht, gt)  # @line L3
        details.append(d)  # @line L4
    return a, details  # @line L5


def idwt(a: list, details: list[list], h: Filter, g: Filter) -> list:
    """Invert dwt: run the synthesis steps from the coarsest level to the finest."""
    a = list(a)
    for d in reversed(details):  # @line L10
        a = synthesis_step(a, d, h, g)  # @line L11
    return a  # @line L12


def orthonormal_bank(h: list) -> tuple[Filter, Filter, Filter, Filter]:
    """Analysis and synthesis filters of an orthonormal wavelet with low-pass h.

    The high-pass filter is g[l] = (-1)^l h[L-1-l]. Synthesis uses the same
    filters, so the inverse is the transpose."""
    n = len(h)
    lo = {l: h[l] for l in range(n)}
    hi = {l: (h[n - 1 - l] if l % 2 == 0 else -h[n - 1 - l]) for l in range(n)}
    return lo, hi, lo, hi


# Haar by averages: s = (a + b)/2, d = (a - b)/2. Exact over the rationals.
HAAR_AVG = (
    {0: Fraction(1, 2), 1: Fraction(1, 2)},
    {0: Fraction(1, 2), 1: Fraction(-1, 2)},
    {0: 1, 1: 1},
    {0: 1, 1: -1},
)

# LeGall 5/3 (Cohen-Daubechies-Feauveau 5/3) biorthogonal filters, the
# reversible filter pair of JPEG 2000 before rounding.
LEGALL_53 = (
    {-2: Fraction(-1, 8), -1: Fraction(1, 4), 0: Fraction(3, 4), 1: Fraction(1, 4), 2: Fraction(-1, 8)},
    {0: Fraction(-1, 2), 1: Fraction(1), 2: Fraction(-1, 2)},
    {-1: Fraction(1, 2), 0: Fraction(1), 1: Fraction(1, 2)},
    {-1: Fraction(-1, 8), 0: Fraction(-1, 4), 1: Fraction(3, 4), 2: Fraction(-1, 4), 3: Fraction(-1, 8)},
)
