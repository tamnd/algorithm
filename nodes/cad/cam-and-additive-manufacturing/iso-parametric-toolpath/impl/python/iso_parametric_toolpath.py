# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iso-parametric-toolpath/. The authors are listed in prov/SQ9VDF.jsonl.

"""Iso-parametric toolpath on a bilinear patch, with exact arithmetic.

The patch is S(u, v) = (1-u)(1-v) P00 + u(1-v) P10 + (1-u) v P01 + u v P11
for 0 <= u, v <= 1. The passes are the iso-v curves v = j / N. On a bilinear
patch every iso-parametric curve is a straight segment, so each pass is
exact and needs no forward step.

For a fixed u the patch is linear in v, with S_v(u) = (1-u)(P01 - P00) +
u(P11 - P10). The gap between the passes v_j and v_j+1 at u is therefore
exactly |S_v(u)| / N. Its square is a convex quadratic in u, so the gap is
largest at u = 0 or u = 1, and N is the smallest integer with
max(|S_v(0)|, |S_v(1)|) <= N w.

The path is a list of contact points on the surface (the CC path). The
cutter location points come from it by an offset along the surface normal.
"""

from fractions import Fraction

Point = tuple[Fraction, Fraction, Fraction]


def _pt(p) -> Point:
    if len(p) != 3:
        raise ValueError("a corner needs 3 coordinates")
    return tuple(Fraction(c) for c in p)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def lerp(a, b, t):
    return tuple(x + t * (y - x) for x, y in zip(a, b))


class BilinearPatch:
    def __init__(self, p00, p10, p01, p11):
        self.p00, self.p10, self.p01, self.p11 = map(_pt, (p00, p10, p01, p11))

    def at(self, u, v) -> Point:
        u, v = Fraction(u), Fraction(v)
        return lerp(lerp(self.p00, self.p10, u), lerp(self.p01, self.p11, u), v)

    def s_v(self, u) -> Point:
        """The derivative in v, which does not depend on v."""
        return lerp(sub(self.p01, self.p00), sub(self.p11, self.p10), Fraction(u))


def pass_count(patch: BilinearPatch, w) -> int:
    """The smallest N such that the gap between neighbouring iso-v passes is at most w."""
    w = Fraction(w)
    if w <= 0:
        raise ValueError("the path interval must be positive")
    m = max(dot(patch.s_v(0), patch.s_v(0)), dot(patch.s_v(1), patch.s_v(1)))  # @line L1
    n = 1
    while m > n * n * w * w:  # @line L2
        n += 1
    return n


def iso_parametric(patch: BilinearPatch, w) -> list[Point]:
    """The zigzag CC path: passes v = j / N, linked along the boundary curves u = 0 and u = 1."""
    n = pass_count(patch, w)
    path = []
    for j in range(n + 1):  # @line L3
        v = Fraction(j, n)
        a, b = patch.at(0, v), patch.at(1, v)
        # The pass is the straight segment from a to b, run back and forth.
        seg = [a, b] if j % 2 == 0 else [b, a]  # @line L4
        # Moving from the last point of one pass to the first point of the next
        # runs along the boundary curve u = 0 or u = 1, which is straight too.
        path.extend(seg)  # @line L5
    return path  # @line L6


def path_segments(path):
    return list(zip(path, path[1:]))
