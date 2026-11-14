# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iso-planar-toolpath/. The authors are listed in prov/4X99MA.jsonl.

"""Iso-planar toolpath on a bilinear patch, with exact arithmetic.

The drive planes are x = c_k = xmin + g/2 + k g. On the bilinear patch
S(u, v), the coordinate x is A + B u + C v + D u v. The code needs
x_v = C + D u > 0 for 0 <= u <= 1, so that each plane meets the patch in one
curve v(u) = (c - A - B u) / (C + D u). This is a rational function, so every
point of the cut curve has rational coordinates and lies exactly on the plane
and on the patch.

Each curve is cut into chords by a recursive midpoint test: a chord is kept
when the curve point at the middle parameter is within eps of the chord.
This test is a heuristic. It does not bound the deviation at every point of
the curve, although on these smooth curves it does so in practice.
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


def dist2_segment(p, a, b) -> Fraction:
    d = sub(b, a)
    dd = dot(d, d)
    t = 0 if dd == 0 else min(Fraction(1), max(Fraction(0), dot(sub(p, a), d) / dd))
    q = tuple(x + t * y - z for x, y, z in zip(a, d, p))
    return dot(q, q)


class BilinearPatch:
    def __init__(self, p00, p10, p01, p11):
        self.p00, self.p10, self.p01, self.p11 = map(_pt, (p00, p10, p01, p11))
        x00, x10, x01, x11 = self.p00[0], self.p10[0], self.p01[0], self.p11[0]
        self.A, self.B, self.C = x00, x10 - x00, x01 - x00
        self.D = x00 - x10 - x01 + x11
        if self.C <= 0 or self.C + self.D <= 0:
            raise ValueError("x must grow with v on the whole patch")

    def at(self, u, v) -> Point:
        return lerp(lerp(self.p00, self.p10, u), lerp(self.p01, self.p11, u), v)

    def v_on_plane(self, c, u) -> Fraction:
        return (c - self.A - self.B * u) / (self.C + self.D * u)

    def u_range(self, c):
        """The u for which the plane x = c meets the patch at 0 <= v <= 1, or None."""
        lo, hi = Fraction(0), Fraction(1)
        # v >= 0:  (c - A) - B u >= 0;  v <= 1:  (C - c + A) + (D + B) u >= 0
        for a, b in ((-self.B, c - self.A), (self.D + self.B, self.C - c + self.A)):
            if a == 0:
                if b < 0:
                    return None
            elif a > 0:
                lo = max(lo, -b / a)
            else:
                hi = min(hi, -b / a)
        return (lo, hi) if lo <= hi else None

    def x_range(self):
        xs = [p[0] for p in (self.p00, self.p10, self.p01, self.p11)]
        return min(xs), max(xs)


def _refine(curve, u0, u1, eps2, depth, out):
    """Append the chord ends for the curve between u0 and u1, without the start point."""
    um = (u0 + u1) / 2
    if depth > 0 and dist2_segment(curve(um), curve(u0), curve(u1)) > eps2:
        _refine(curve, u0, um, eps2, depth - 1, out)
        _refine(curve, um, u1, eps2, depth - 1, out)
    else:
        out.append(u1)


def iso_planar(patch: BilinearPatch, g, eps, max_depth=30):
    """The passes of an iso-planar path, as (c, [(u, point), ...]) from the lowest plane up.

    Even passes run in the direction of growing u, odd passes the other way.
    """
    g, eps = Fraction(g), Fraction(eps)
    if g <= 0 or eps <= 0:
        raise ValueError("g and eps must be positive")
    xmin, xmax = patch.x_range()
    passes = []
    k = 0
    c = xmin + g / 2
    while c < xmax:  # @line L1
        rng = patch.u_range(c)  # @line L2
        if rng is None:  # @line L3
            k, c = k + 1, c + g
            continue

        def curve(u, c=c):  # @line L4
            return patch.at(u, patch.v_on_plane(c, u))

        lo, hi = rng
        us = [lo]
        if hi > lo:
            _refine(curve, lo, hi, eps * eps, max_depth, us)  # @line L5
        pts = [(u, curve(u)) for u in us]
        passes.append((c, pts if k % 2 == 0 else pts[::-1]))  # @line L6
        k, c = k + 1, c + g
    return passes  # @line L7
