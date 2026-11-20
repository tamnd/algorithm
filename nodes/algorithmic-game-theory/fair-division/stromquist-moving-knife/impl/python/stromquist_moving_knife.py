# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stromquist-moving-knife/. The authors are listed in prov/PK1D3M.jsonl.

"""An exact simulation of the Stromquist moving knife for three agents.

The knives move continuously, so this is not a finite protocol. For
piecewise-constant valuations with positive densities on the same k equal
segments, each knife position k_i(x) and the median knife y(x) are
continuous and piecewise affine in the sword position x. The simulation
splits [0, 1] at every point where one of these functions can bend, and on
each part it solves the shout condition, which is then affine, exactly.
"""

from bisect import bisect_right
from fractions import Fraction

from agtcake import Valuation

Interval = tuple[Fraction, Fraction]


class _Cdf:
    """F(x) = V([0, x]) and its inverse, for positive piecewise-constant densities."""

    def __init__(self, v: Valuation) -> None:
        self.d = list(v)
        self.k = len(v)
        self.pre = [Fraction(0)]
        for dj in self.d:
            self.pre.append(self.pre[-1] + dj / self.k)

    def f(self, x: Fraction) -> Fraction:
        j = min(int(x * self.k), self.k - 1)
        return self.pre[j] + self.d[j] * (x - Fraction(j, self.k))

    def inv(self, t: Fraction) -> Fraction:
        j = min(bisect_right(self.pre, t) - 1, self.k - 1)
        return Fraction(j, self.k) + (t - self.pre[j]) / self.d[j]

    def knife(self, x: Fraction) -> Fraction:
        """The point that splits [x, 1] into two halves of equal value."""
        return self.inv((1 + self.f(x)) / 2)


def _breakpoints(cdfs: list[_Cdf]) -> list[Fraction]:
    k = cdfs[0].k
    pts = {Fraction(j, k) for j in range(k + 1)}  # the density at x changes
    for c in cdfs:
        for j in range(1, k):
            t = 2 * c.pre[j] - 1
            if t > 0:
                pts.add(c.inv(t))  # this knife crosses j/k
    base = sorted(pts)
    knives = [[c.knife(p) for c in cdfs] for p in base]
    more = set(base)
    for s in range(len(base) - 1):
        p, q = base[s], base[s + 1]
        kp, kq = knives[s], knives[s + 1]
        for i in range(3):
            for m in range(i + 1, 3):
                dp, dq = kp[i] - kp[m], kq[i] - kq[m]
                if dp * dq < 0:
                    more.add(p + (q - p) * dp / (dp - dq))  # two knives cross
    return sorted(more)


def _nonneg_part(hp: Fraction, hq: Fraction, p: Fraction, q: Fraction):
    """The part of [p, q] where an affine h with h(p) = hp, h(q) = hq is >= 0."""
    if hp >= 0 and hq >= 0:
        return p, q
    if hp < 0 and hq < 0:
        return None
    r = p + (q - p) * hp / (hp - hq)
    return (p, r) if hp >= 0 else (r, q)


def _gaps(c: _Cdf, x: Fraction, y: Fraction) -> tuple[Fraction, Fraction]:
    """V([0, x]) - V([x, y]) and V([0, x]) - V([y, 1])."""
    fx, fy = c.f(x), c.f(y)
    return 2 * fx - fy, fx - 1 + fy


def stromquist(vals: list[Valuation]) -> tuple[dict[int, Interval], Fraction, Fraction, int]:
    """Run the knives. Return (pieces, x, y, shouter); agents are 0, 1 and 2."""
    if len(vals) != 3 or len({len(v) for v in vals}) != 1:
        raise ValueError("three valuations on the same segments are needed")
    if any(d <= 0 for v in vals for d in v):
        raise ValueError("the simulation needs positive densities")
    cdfs = [_Cdf(v) for v in vals]
    pts = _breakpoints(cdfs)  # @line L1
    found = None
    yq = sorted(c.knife(pts[0]) for c in cdfs)[1]
    for p, q in zip(pts, pts[1:]):  # @line L2
        yp = yq  # @line L3
        yq = sorted(c.knife(q) for c in cdfs)[1]  # @line L4
        best = None
        for i, c in enumerate(cdfs):  # @line L5
            a1, a2 = _gaps(c, p, yp)
            b1, b2 = _gaps(c, q, yq)
            s1 = _nonneg_part(a1, b1, p, q)
            s2 = _nonneg_part(a2, b2, p, q)
            if s1 is None or s2 is None:
                continue
            lo, hi = max(s1[0], s2[0]), min(s1[1], s2[1])
            if lo <= hi and (best is None or lo < best[0]):
                best = (lo, i)  # @line L6
        if best is not None:
            found = best
            break
    assert found is not None  # someone shouts before x reaches 1
    x, s = found
    ks = [c.knife(x) for c in cdfs]
    y = sorted(ks)[1]
    pieces: dict[int, Interval] = {s: (Fraction(0), x)}  # @line L7
    a, b = sorted((i for i in range(3) if i != s), key=lambda i: (ks[i], i))
    pieces[a] = (x, y)  # @line L8
    pieces[b] = (y, Fraction(1))  # @line L9
    return pieces, x, y, s
