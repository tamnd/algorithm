# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/max-log-demapping/. The authors are listed in prov/BTM11T.jsonl.

"""Max-log demapping: approximate bit log-likelihood ratios without exponentials.

The model is y = h x + w with w ~ CN(0, N0), a known gain h and x one of the
M points of a constellation. points[i] is the point with the bit label i, and
bit k of the label (k = 0 is the most significant bit) is (i >> (m - 1 - k)) & 1
with m = log2 M, as in constel.py. The max-log LLR of bit k is

    L_k = max_{b_k(i) = 0} d_i - max_{b_k(i) = 1} d_i,
    d_i = -|y - h a_i|^2 / N0 + sum_k (1 - 2 b_k(i)) la_k / 2,

which without priors is (min over bit 1 of |y - h a|^2 - min over bit 0) / N0.
A positive value favors the bit 0.
"""

import math


def label_bit(i: int, k: int, m: int) -> int:
    """Bit k (most significant first) of the m-bit label i."""
    return (i >> (m - 1 - k)) & 1


def _check(points: list[complex], n0: float) -> int:
    big_m = len(points)
    if big_m < 2 or big_m & (big_m - 1):
        raise ValueError("the number of points must be a power of two")
    if n0 <= 0:
        raise ValueError("N0 must be positive")
    return big_m.bit_length() - 1


def max_log_demap(y: complex, points: list[complex], n0: float, h: complex = 1, la: list[float] | None = None) -> list[float]:
    """The max-log LLRs L_0, ..., L_{m-1} of the bits of one symbol."""
    m = _check(points, n0)
    d = []
    for i, a in enumerate(points):  # @line L1
        di = -abs(y - h * a) ** 2 / n0  # @line L2
        if la is not None:
            di += sum((1 - 2 * label_bit(i, k, m)) * la[k] / 2.0 for k in range(m))
        d.append(di)
    out = []
    for k in range(m):  # @line L3
        best = [-math.inf, -math.inf]  # @line L4
        for i in range(len(points)):  # @line L5
            b = label_bit(i, k, m)
            if d[i] > best[b]:
                best[b] = d[i]  # @line L6
        out.append(best[0] - best[1])  # @line L7
    return out


def max_log_extrinsic(y: complex, points: list[complex], n0: float, h: complex = 1, la: list[float] | None = None) -> list[float]:
    """The extrinsic values L_k - la_k of the max-log demapper."""
    post = max_log_demap(y, points, n0, h, la)
    if la is None:
        return post
    return [p - a for p, a in zip(post, la)]  # @line L8


def _gray_inv(g: int) -> int:
    n = 0
    while g:
        n ^= g
        g >>= 1
    return n


def _axis(u: float, side: int) -> list[float]:
    """Per-axis max-log values (min over bit 1 of (u - c)^2 minus min over bit 0) on Gray side-PAM.

    The level with label lab has the raw amplitude side - 1 - 2 gray^-1(lab).
    """
    q = side.bit_length() - 1
    best = [[math.inf, math.inf] for _ in range(q)]
    for lab in range(side):
        c = side - 1 - 2 * _gray_inv(lab)
        dist = (u - c) ** 2
        for k in range(q):
            b = label_bit(lab, k, q)
            if dist < best[k][b]:
                best[k][b] = dist
    return [b1 - b0 for b0, b1 in best]


def max_log_square_qam(y: complex, big_m: int, n0: float, h: complex = 1) -> list[float]:
    """Max-log LLRs for Gray square M-QAM (as constel.qam), one axis at a time in O(sqrt(M) log M)."""
    q2 = big_m.bit_length() - 1
    if big_m < 4 or big_m & (big_m - 1) or q2 % 2:
        raise ValueError("square QAM needs M = 4^k")
    if n0 <= 0:
        raise ValueError("N0 must be positive")
    if h == 0:
        raise ValueError("the gain must be nonzero")
    side = 1 << (q2 // 2)
    s2 = 2.0 * (big_m - 1) / 3.0
    z = y / h
    s = math.sqrt(s2)
    scale = abs(h) ** 2 / (s2 * n0)
    return [scale * v for v in _axis(s * z.real, side) + _axis(s * z.imag, side)]


def max_log_16qam_closed_form(y: complex, n0: float, h: complex = 1) -> list[float]:
    """The closed form for Gray 16-QAM: per axis with u = sqrt(10) Re(y / h) (and the same for Im),
    Lambda_0 = 4u if |u| <= 2 else 8(u - sign u), Lambda_1 = 4(|u| - 2), and L = |h|^2 Lambda / (10 N0)."""
    if n0 <= 0:
        raise ValueError("N0 must be positive")
    z = y / h
    scale = abs(h) ** 2 / (10.0 * n0)
    out0, out1 = [], []
    for u in (math.sqrt(10.0) * z.real, math.sqrt(10.0) * z.imag):
        if abs(u) <= 2.0:
            lam0 = 4.0 * u
        else:
            lam0 = 8.0 * (u - math.copysign(1.0, u))
        out0.append(lam0)
        out1.append(4.0 * (abs(u) - 2.0))
    return [scale * out0[0], scale * out1[0], scale * out0[1], scale * out1[1]]
