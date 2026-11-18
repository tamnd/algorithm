# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variance-shadow-maps/. The authors are listed in prov/BNWA0B.jsonl.

"""Variance shadow maps (Donnelly and Lauritzen 2006).

A depth map s is a list of h rows of w depths, s[j][i], i the column and j the
row. Depth is in [0, 1] (the Direct3D clip range), smaller is nearer to the
light. The moment map holds (E[z], E[z^2]) per texel after a filter. The
lookup returns an upper bound on the lit fraction, the fraction of the
filtered depths d with d >= t for the receiver depth t (Cantelli's inequality).
With Fraction input and min_var = 0 every result is exact.
"""

from fractions import Fraction


def moments(s):
    """The raw moment map: (d, d^2) per texel."""
    return [[(d, d * d) for d in row] for row in s]  # @line L1


def summed_area(m):
    """Summed-area tables of both moments, with a zero first row and column."""
    h, w = len(m), len(m[0])
    t1 = [[0] * (w + 1) for _ in range(h + 1)]
    t2 = [[0] * (w + 1) for _ in range(h + 1)]
    for j in range(h):
        a1 = a2 = 0
        for i in range(w):
            a1 += m[j][i][0]
            a2 += m[j][i][1]
            t1[j + 1][i + 1] = t1[j][i + 1] + a1
            t2[j + 1][i + 1] = t2[j][i + 1] + a2
    return t1, t2


def box_filter(m, r):
    """The (2r + 1) x (2r + 1) box filter of the moments, clamped at the border,
    computed from summed-area tables in O(1) per texel."""
    h, w = len(m), len(m[0])
    t1, t2 = summed_area(m)
    out = []
    for j in range(h):
        row = []
        for i in range(w):
            x0, x1 = max(i - r, 0), min(i + r + 1, w)
            y0, y1 = max(j - r, 0), min(j + r + 1, h)
            n = (x1 - x0) * (y1 - y0)
            m1 = t1[y1][x1] - t1[y0][x1] - t1[y1][x0] + t1[y0][x0]
            m2 = t2[y1][x1] - t2[y0][x1] - t2[y1][x0] + t2[y0][x0]
            row.append((Fraction(m1) / n, Fraction(m2) / n) if isinstance(m1, (int, Fraction))
                       else (m1 / n, m2 / n))
        out.append(row)
    return out  # @line L2


def chebyshev_upper_bound(m1, m2, t, min_var=0):
    """p_max of the paper: 1 when t <= m1, else var / (var + (t - m1)^2)."""
    if t <= m1:  # @line L4
        return 1
    var = max(m2 - m1 * m1, min_var)  # @line L5
    d = t - m1
    return var / (var + d * d)  # @line L6


def reduce_bleeding(p, amount):
    """Light bleeding reduction: map [amount, 1] linearly onto [0, 1]."""
    if amount == 0:
        return p
    return min(max((p - amount) / (1 - amount), 0), 1)  # @line L7


def vsm_lookup(fm, i, j, t, min_var=0, amount=0):
    """The lit estimate at texel (i, j) of the filtered moment map fm."""
    m1, m2 = fm[j][i]  # @line L3
    return reduce_bleeding(chebyshev_upper_bound(m1, m2, t, min_var), amount)


def lit_fraction(depths, t):
    """The true lit fraction of a list of depths for the receiver depth t."""
    return Fraction(sum(1 for d in depths if d >= t), len(depths))
