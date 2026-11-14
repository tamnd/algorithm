# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lr-b-spline/. The authors are listed in prov/G8C6QC.jsonl.

"""Bivariate LR B-splines (Dokken, Lyche and Pettersen), in exact arithmetic.

An LR B-spline is a tensor product B-spline of bidegree (p, q) given by its
local knot vectors x0 <= ... <= x(p+1) and y0 <= ... <= y(q+1), with a
positive weight g and a coefficient c. The spline is sum g * c * B, and the
weights make sum g * B = 1.

The mesh is a set of axis-parallel segments of multiplicity one. A vertical
segment ("v", a, lo, hi) is the line x = a for lo <= y <= hi; a horizontal
segment ("h", b, lo, hi) is y = b for lo <= x <= hi. Collinear segments that
overlap or touch are merged.

A segment traverses a B-spline when its value lies strictly inside the
support in one direction, is not one of the local knots in that direction,
and the segment covers the whole support in the other direction. Inserting
the value into the local knot vector then splits the B-spline into two.
"""

from fractions import Fraction


def split_knots(t, a):
    """One-knot insertion in a single B-spline: B[t] = a1 B[t1] + a2 B[t2]."""
    p = len(t) - 2
    tau = sorted(t + (a,))
    a1 = min(Fraction(1), (a - t[0]) / (t[p] - t[0])) if t[p] > t[0] else Fraction(1)
    a2 = min(Fraction(1), (t[p + 1] - a) / (t[p + 1] - t[1])) if t[p + 1] > t[1] else Fraction(1)
    return (tuple(tau[: p + 2]), a1), (tuple(tau[1:]), a2)


def local_bspline(t, x, end):
    """B-spline on the local knots t at x, by Cox-de Boor; closed at the domain end."""
    p = len(t) - 2
    vals = [Fraction(int(t[k] <= x < t[k + 1] or (x == end and t[k] < t[k + 1] == end))) for k in range(p + 1)]
    for d in range(1, p + 1):
        vals = [
            ((x - t[k]) / (t[k + d] - t[k]) * vals[k] if t[k + d] != t[k] else 0)
            + ((t[k + d + 1] - x) / (t[k + d + 1] - t[k + 1]) * vals[k + 1] if t[k + d + 1] != t[k + 1] else 0)
            for k in range(len(vals) - 1)
        ]
    return vals[0]


class LRSpline:
    def __init__(self, xknots, yknots, p, q, coeffs=None):
        """Start from a tensor product spline on open knot vectors.

        coeffs[i][j] is the coefficient of the tensor B-spline (i, j); the
        default is 0.
        """
        self.p, self.q = p, q
        self.xend, self.yend = xknots[-1], yknots[-1]
        self.box = (xknots[0], xknots[-1], yknots[0], yknots[-1])
        self.funcs = {}
        for i in range(len(xknots) - p - 1):
            for j in range(len(yknots) - q - 1):
                c = Fraction(coeffs[i][j]) if coeffs else Fraction(0)
                self.funcs[(tuple(xknots[i : i + p + 2]), tuple(yknots[j : j + q + 2]))] = [Fraction(1), c]
        self.lines = {}
        for a in sorted(set(xknots)):
            self._add(("v", a, yknots[0], yknots[-1]))
        for b in sorted(set(yknots)):
            self._add(("h", b, xknots[0], xknots[-1]))

    def _add(self, seg):
        d, v, lo, hi = seg
        spans = self.lines.setdefault((d, v), [])
        spans.append((lo, hi))
        spans.sort()
        merged = [spans[0]]
        for s, e in spans[1:]:
            if s <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], e))
            else:
                merged.append((s, e))
        self.lines[(d, v)] = merged

    def _covers(self, d, v, lo, hi):
        return any(s <= lo and hi <= e for s, e in self.lines.get((d, v), []))

    def traversing(self, key):
        """A mesh line that traverses the B-spline: ("v" or "h", value), or None."""
        xk, yk = key
        for (d, v), spans in self.lines.items():
            if d == "v" and xk[0] < v < xk[-1] and v not in xk and self._covers(d, v, yk[0], yk[-1]):
                return d, v
            if d == "h" and yk[0] < v < yk[-1] and v not in yk and self._covers(d, v, xk[0], xk[-1]):
                return d, v
        return None

    def _merge_in(self, key, g, c):
        if key in self.funcs:
            g0, c0 = self.funcs[key]
            self.funcs[key] = [g0 + g, (g0 * c0 + g * c) / (g0 + g)]
            return False
        self.funcs[key] = [g, c]
        return True

    def insert(self, seg):
        """Insert a mesh segment and split until no B-spline is traversed."""
        d, v, lo, hi = seg
        x0, x1, y0, y1 = self.box
        if not (lo < hi and ((d == "v" and x0 < v < x1 and y0 <= lo and hi <= y1) or (d == "h" and y0 < v < y1 and x0 <= lo and hi <= x1))):
            raise ValueError("the segment must lie inside the domain")
        before = dict(self.funcs)
        lines = {k: list(s) for k, s in self.lines.items()}
        self._add(seg)  # @line L1
        queue = list(self.funcs)  # @line L2
        split = 0
        while queue:  # @line L3
            key = queue.pop()
            if key not in self.funcs:
                continue
            hit = self.traversing(key)  # @line L4
            if hit is None:
                continue
            g, c = self.funcs.pop(key)  # @line L5
            split += 1
            xk, yk = key
            if hit[0] == "v":
                parts = [((t, yk), a) for t, a in split_knots(xk, hit[1])]  # @line L6
            else:
                parts = [((xk, t), a) for t, a in split_knots(yk, hit[1])]
            for child, a in parts:  # @line L7
                self._merge_in(child, g * a, c)  # @line L8
                queue.append(child)  # @line L9
        if split == 0:
            self.funcs, self.lines = before, lines
            raise ValueError("an LR refinement must split at least one B-spline")
        return split

    def evaluate(self, x, y, weights_only=False):
        """sum g * c * B(x, y), or sum g * B(x, y) when weights_only is set."""
        s = Fraction(0)
        for (xk, yk), (g, c) in self.funcs.items():
            b = local_bspline(xk, x, self.xend)
            if b:
                b *= local_bspline(yk, y, self.yend)
                s += g * b * (1 if weights_only else c)
        return s
