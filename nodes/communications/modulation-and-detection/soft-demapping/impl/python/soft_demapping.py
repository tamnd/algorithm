# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soft-demapping/. The authors are listed in prov/N96EQ7.jsonl.

"""Exact soft demapping: the bit log-likelihood ratios of one received symbol.

The model is y = h x + w with w ~ CN(0, N0), a known gain h and x one of the
M points of a constellation. points[i] is the point with the bit label i, and
bit k of the label (k = 0 is the most significant bit) is (i >> (m - 1 - k)) & 1
with m = log2 M, as in constel.py. The LLR of bit k is

    L_k = ln P(b_k = 0 | y) / P(b_k = 1 | y),

so a positive value favors the bit 0. Optional prior LLRs la[k] of the same
sign convention enter as the factor exp(+-la[k] / 2) of each point.
"""

import math


def max_star(a: float, b: float) -> float:
    """ln(e^a + e^b), computed as max(a, b) + ln(1 + e^-|a - b|) so it never overflows."""
    if a == -math.inf:
        return b
    if b == -math.inf:
        return a
    return max(a, b) + math.log1p(math.exp(-abs(a - b)))


def label_bit(i: int, k: int, m: int) -> int:
    """Bit k (most significant first) of the m-bit label i."""
    return (i >> (m - 1 - k)) & 1


def metrics(y: complex, points: list[complex], n0: float, h: complex = 1, la: list[float] | None = None) -> list[float]:
    """The log metric d_i = -|y - h a_i|^2 / N0 + sum_k (1 - 2 b_k(i)) la_k / 2 of every point."""
    m = len(points).bit_length() - 1
    d = []
    for i, a in enumerate(points):  # @line L1
        di = -abs(y - h * a) ** 2 / n0  # @line L2
        if la is not None:
            di += sum((1 - 2 * label_bit(i, k, m)) * la[k] / 2.0 for k in range(m))
        d.append(di)
    return d


def soft_demap(y: complex, points: list[complex], n0: float, h: complex = 1, la: list[float] | None = None) -> list[float]:
    """The exact a posteriori LLRs L_0, ..., L_{m-1} of the bits of one symbol."""
    big_m = len(points)
    if big_m < 2 or big_m & (big_m - 1):
        raise ValueError("the number of points must be a power of two")
    if n0 <= 0:
        raise ValueError("N0 must be positive")
    m = big_m.bit_length() - 1
    d = metrics(y, points, n0, h, la)
    out = []
    for k in range(m):  # @line L3
        acc = [-math.inf, -math.inf]  # @line L4
        for i in range(big_m):  # @line L5
            b = label_bit(i, k, m)
            acc[b] = max_star(acc[b], d[i])  # @line L6
        out.append(acc[0] - acc[1])  # @line L7
    return out


def extrinsic(y: complex, points: list[complex], n0: float, h: complex = 1, la: list[float] | None = None) -> list[float]:
    """The extrinsic LLRs L_k - la_k, which a turbo loop passes back to the decoder."""
    post = soft_demap(y, points, n0, h, la)
    if la is None:
        return post
    return [p - a for p, a in zip(post, la)]  # @line L8


def soft_demap_block(ys: list[complex], points: list[complex], n0: float, h: complex = 1) -> list[float]:
    """The LLRs of a block of symbols, concatenated in symbol order."""
    out = []
    for y in ys:
        out.extend(soft_demap(y, points, n0, h))
    return out
