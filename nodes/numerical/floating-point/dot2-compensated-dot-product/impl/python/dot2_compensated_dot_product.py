# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dot2-compensated-dot-product/. The authors are listed in prov/7CXZPB.jsonl.

"""Dot2 (Ogita, Rump and Oishi, 2005): a dot product as accurate as if computed in twice the precision.

Every product is split exactly into p + e by TwoProduct, the running sum is split exactly into
p + q by TwoSum, and all the small parts are added in ordinary floating point.
"""

import math
from collections.abc import Sequence

SPLITTER = 134217729.0  # 2^27 + 1, Veltkamp's constant for binary64


def two_sum(a: float, b: float) -> tuple[float, float]:
    """Knuth's TwoSum: s = fl(a + b) and e with a + b = s + e exactly (no overflow). Cost: 6 flops."""
    s = a + b
    z = s - a
    return s, (a - (s - z)) + (b - z)


def two_product_fma(a: float, b: float) -> tuple[float, float]:
    """p = fl(a b) and e = a b - p exactly, by one FMA (exact when there is no underflow). Cost: 2 flops."""
    p = a * b
    return p, math.fma(a, b, -p)


def _split(a: float) -> tuple[float, float]:
    c = SPLITTER * a
    hi = c - (c - a)
    return hi, a - hi


def two_product_dekker(a: float, b: float) -> tuple[float, float]:
    """Dekker's TwoProduct with Veltkamp splitting, without FMA (exact when there is no
    underflow and |a|, |b| < 2^996). Cost: 17 flops."""
    p = a * b
    ah, al = _split(a)
    bh, bl = _split(b)
    return p, al * bl - (((p - ah * bh) - al * bh) - ah * bl)


def dot2(x: Sequence[float], y: Sequence[float], fma: bool = True) -> float:
    """The dot product sum(x[i] * y[i]) with Dot2.

    Precondition: len(x) == len(y) == n, finite entries, n u < 1, no underflow in the products
    and no overflow. Then |result - x.y| <= u |x.y| + (1 + u) gamma_n^2 sum |x[i] y[i]| (proved).
    Cost: 25n - 7 flops with fma=False, 10n - 8 with fma=True; O(1) extra space.
    """
    if len(x) != len(y):
        raise ValueError("vectors of different lengths")
    if not x:
        return 0.0
    two_product = two_product_fma if fma else two_product_dekker
    p, s = two_product(x[0], y[0])  # @line L1
    for i in range(1, len(x)):  # @line L2
        h, r = two_product(x[i], y[i])  # @line L3
        p, q = two_sum(p, h)  # @line L4
        s = s + (q + r)  # @line L5
    return p + s  # @line L6


def naive_dot(x: Sequence[float], y: Sequence[float]) -> float:
    """Recursive dot product in working precision, for comparison. Cost: 2n flops."""
    s = 0.0
    for a, b in zip(x, y):
        s += a * b
    return s
