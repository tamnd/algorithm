# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parametric-continuity/. The authors are listed in prov/WGBTZC.jsonl.

"""Order of parametric (C^k) and geometric (G^1, G^2) continuity at a joint.

A segment is a polynomial curve on the local parameter u in [0, 1], stored as a
list of coefficient vectors: seg[i] is the vector coefficient of u^i. The segment
covers a global parameter interval of length h, so the global derivative of
order j is the local one divided by h^j. Segment A ends where segment B starts.
With Fraction (or int) coefficients every test is exact.
"""

from math import inf
from typing import List, Optional, Sequence, Tuple

Vec = Tuple


def derivative_at(seg: Sequence[Vec], u, j: int, h=1) -> Vec:
    """The j-th derivative of the segment with respect to the global parameter, at local u."""
    d = len(seg[0])
    acc = [u - u] * d
    for i in range(len(seg) - 1, j - 1, -1):
        # Horner on sum_{i >= j} i!/(i-j)! seg[i] u^(i-j)
        f = 1
        for r in range(i - j + 1, i + 1):
            f *= r
        acc = [a * u + f * c for a, c in zip(acc, seg[i])]
    scale = h ** j
    return tuple(a / scale if scale != 1 else a for a in acc)


def continuity_order(A: Sequence[Vec], B: Sequence[Vec], ha=1, hb=1):
    """The largest k with A^(j)(end) = B^(j)(start) for j = 0..k; -1 if the pieces do not meet.

    Returns math.inf when every derivative agrees, that is, A and B are pieces
    of one polynomial curve.
    """
    top = max(len(A), len(B))
    one = (A[0][0] - A[0][0]) + 1
    for j in range(top):
        if derivative_at(A, one, j, ha) != derivative_at(B, one - one, j, hb):
            return j - 1
    return inf


def _ratio(w: Vec, v: Vec):
    """The number r with w = r v, or None if there is none (v must be nonzero)."""
    i = next(k for k, x in enumerate(v) if x != 0)
    r = w[i] / v[i]
    if all(a == r * b for a, b in zip(w, v)):
        return r
    return None


def g1_beta(A: Sequence[Vec], B: Sequence[Vec]) -> Optional[object]:
    """beta1 > 0 with B'(0) = beta1 A'(1) if the joint is G^1 and regular, else None."""
    one = (A[0][0] - A[0][0]) + 1
    zero = one - one
    if derivative_at(A, one, 0) != derivative_at(B, zero, 0):
        return None
    a1 = derivative_at(A, one, 1)
    b1 = derivative_at(B, zero, 1)
    if all(x == 0 for x in a1) or all(x == 0 for x in b1):
        return None  # a zero velocity: the beta form needs a regular joint
    r = _ratio(b1, a1)
    if r is None or r <= 0:
        return None
    return r


def g2_betas(A: Sequence[Vec], B: Sequence[Vec]) -> Optional[Tuple[object, object]]:
    """(beta1, beta2) with B'(0) = beta1 A'(1) and B''(0) = beta1^2 A''(1) + beta2 A'(1), else None."""
    b1 = g1_beta(A, B)
    if b1 is None:
        return None
    one = (A[0][0] - A[0][0]) + 1
    zero = one - one
    a1 = derivative_at(A, one, 1)
    a2 = derivative_at(A, one, 2) if len(A) > 2 else tuple(zero for _ in a1)
    c2 = derivative_at(B, zero, 2) if len(B) > 2 else tuple(zero for _ in a1)
    w = tuple(c - b1 * b1 * a for c, a in zip(c2, a2))
    b2 = _ratio(w, a1)
    if b2 is None:
        return None
    return b1, b2


def bezier_to_power(ctrl: Sequence[Vec]) -> List[Vec]:
    """Power coefficients of the Bezier curve with the given control points."""
    n = len(ctrl) - 1
    d = len(ctrl[0])
    out = []
    for i in range(n + 1):
        # coefficient of u^i: C(n, i) * sum_k (-1)^(i-k) C(i, k) P_k
        cni = 1
        for r in range(i):
            cni = cni * (n - r) // (r + 1)
        acc = [ctrl[0][0] - ctrl[0][0]] * d
        cik = 1
        for k in range(i + 1):
            sign = -1 if (i - k) % 2 else 1
            acc = [a + sign * cik * c for a, c in zip(acc, ctrl[k])]
            cik = cik * (i - k) // (k + 1)
        out.append(tuple(cni * a for a in acc))
    return out
