# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tsay-zero-skew/. The authors are listed in prov/J8K07F.jsonl.
"""Tsay's exact zero-skew merge, bottom up over a given binary topology.

Wires have resistance r and capacitance c per unit length, in the pi model.
A sink is ((x, y), load capacitance). A topology is a sink index or a pair of
topologies. Each subtree is summarised by its root point, its total
capacitance C and its Elmore delay t from the root to every sink (the same
for all its sinks). Exact with Fractions, except when a wire must be longer
than the distance (elongation), where a square root appears: it is exact when
the number under the root is a square of a rational, else it is rounded to
about 60 decimal digits.
"""

from fractions import Fraction
from math import isqrt


class Node:
    def __init__(self, pt, cap, t, kids, sink=None):
        self.pt, self.cap, self.t, self.kids, self.sink = pt, cap, t, kids, sink


def l1(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def sqrt_fraction(v, bits=200):
    """Exact root of a rational square, else a rational within 2^-bits."""
    v = Fraction(v)
    n, d = v.numerator, v.denominator
    rn, rd = isqrt(n), isqrt(d)
    if rn * rn == n and rd * rd == d:
        return Fraction(rn, rd)
    scale = 1 << (2 * bits)
    return Fraction(isqrt(n * scale // d), 1 << bits)


def point_along(p, q, s):
    """The point at L1 distance s from p on the path from p to q that runs
    horizontally first, then vertically."""
    dx = q[0] - p[0]
    if s <= abs(dx):
        return (p[0] + (s if dx >= 0 else -s), p[1])
    dy = q[1] - p[1]
    rest = s - abs(dx)
    return (q[0], p[1] + (rest if dy >= 0 else -rest))


def elongated(r, c, cap, dt):
    """Wire length L' >= 0 with r L' (c L' / 2 + cap) = dt, for dt >= 0."""
    if c == 0:
        return Fraction(dt) / (r * cap)
    disc = (r * cap) ** 2 + 2 * r * c * dt
    return (sqrt_fraction(disc) - r * cap) / (r * c)


def merge(a, b, r, c):
    """Join subtrees a and b at the tapping point of zero skew."""
    L = l1(a.pt, b.pt)  # @line L4
    if L > 0:
        x = (b.t - a.t + r * L * (b.cap + c * L / 2)) / (r * L * (c * L + a.cap + b.cap))  # @line L5
    else:
        x = Fraction(0) if a.t >= b.t else Fraction(1)
    if 0 <= x <= 1 and L > 0:  # @line L6
        la, lb = x * L, (1 - x) * L
        pt = point_along(a.pt, b.pt, la)
    elif x < 0 or (L == 0 and a.t >= b.t):  # @line L7
        la, lb = Fraction(0), elongated(r, c, b.cap, a.t - b.t)
        pt = a.pt
    else:  # @line L8
        la, lb = elongated(r, c, a.cap, b.t - a.t), Fraction(0)
        pt = b.pt
    t = a.t + r * la * (c * la / 2 + a.cap)  # @line L9
    return Node(pt, a.cap + b.cap + c * (la + lb), t, [(a, la), (b, lb)])


def zero_skew_tree(sinks, topo, r, c):
    """Return the root Node of the zero-skew tree on the given topology."""
    if not isinstance(topo, tuple):  # @line L1
        (x, y), load = sinks[topo]
        return Node((Fraction(x), Fraction(y)), Fraction(load), Fraction(0), [], sink=topo)  # @line L2
    left = zero_skew_tree(sinks, topo[0], r, c)  # @line L3
    right = zero_skew_tree(sinks, topo[1], r, c)
    return merge(left, right, r, c)


def wirelength(node):
    return sum(length + wirelength(k) for k, length in node.kids)
