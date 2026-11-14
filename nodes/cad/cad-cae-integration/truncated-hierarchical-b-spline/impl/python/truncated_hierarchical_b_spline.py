# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/truncated-hierarchical-b-spline/. The authors are listed in prov/EY36RH.jsonl.

"""Bivariate truncated hierarchical B-splines (THB-splines), in exact arithmetic.

The levels and domains are those of the hierarchical-b-spline page. Level l
has the open uniform knot vector of degree p on [0, n0] with spacing 2^-l in
each direction. Omega^0 = [0, n0]^2, Omega^l is a union of cells of level
l - 1 inside Omega^(l-1), and Omega^L is empty. Kraft's rule selects the
B-splines of level l that lie in Omega^l but not in Omega^(l+1).

The truncated function of a selected B-spline of level l is found level by
level: write it in the B-splines of level k = l + 1, ..., L - 1 and drop the
terms whose support lies in Omega^k. The result is kept as coefficients on
the tensor B-splines of the finest level.
"""

from fractions import Fraction


def open_knots(n0, p, level):
    k = 2**level
    return [Fraction(0)] * p + [Fraction(a, k) for a in range(n0 * k + 1)] + [Fraction(n0)] * p


def insert_knot(knots, coeffs, u, p):
    """Boehm's rule on a whole coefficient vector: the same spline with u added."""
    k = max(i for i in range(len(knots) - 1) if knots[i] <= u < knots[i + 1])
    new = []
    for i in range(len(coeffs) + 1):
        if i <= k - p:
            new.append(coeffs[i])
        elif i > k:
            new.append(coeffs[i - 1])
        else:
            a = (u - knots[i]) / (knots[i + p] - knots[i])
            new.append(a * coeffs[i] + (1 - a) * coeffs[i - 1])
    return sorted(knots + [u]), new


def two_scale(n0, p, level):
    """R[i] = {j: c}: B-spline i of the level is sum_j c N_j of the next level."""
    coarse = open_knots(n0, p, level)
    new = sorted(set(open_knots(n0, p, level + 1)) - set(coarse))
    R = []
    for i in range(len(coarse) - p - 1):
        knots, c = list(coarse), [Fraction(int(r == i)) for r in range(len(coarse) - p - 1)]
        for u in new:
            knots, c = insert_knot(knots, c, u, p)
        R.append({j: x for j, x in enumerate(c) if x})
    return R


def bspline(knots, i, p, x):
    """N_i of degree p on the knots at x, by Cox-de Boor; closed at the right end."""
    last = knots[-1]
    vals = [Fraction(int(knots[k] <= x < knots[k + 1] or (x == last and knots[k] < knots[k + 1] == last))) for k in range(i, i + p + 1)]
    for d in range(1, p + 1):
        vals = [
            ((x - knots[i + k]) / (knots[i + k + d] - knots[i + k]) * vals[k] if knots[i + k + d] != knots[i + k] else 0)
            + ((knots[i + k + d + 1] - x) / (knots[i + k + d + 1] - knots[i + k + 1]) * vals[k + 1] if knots[i + k + d + 1] != knots[i + k + 1] else 0)
            for k in range(len(vals) - 1)
        ]
    return vals[0]


class THB:
    def __init__(self, n0, p, levels):
        self.n0, self.p, self.L = n0, p, levels
        self.knots = [open_knots(n0, p, l) for l in range(levels)]
        self.R = [two_scale(n0, p, l) for l in range(levels - 1)]
        self.omega = [{(a, b) for a in range(n0) for b in range(n0)}] + [set() for _ in range(levels - 1)]

    def size(self, level):
        return self.n0 * 2**level + self.p

    def cells(self, level, i):
        return range(max(i - self.p, 0), min(i, self.n0 * 2**level - 1) + 1)

    def inside(self, level, B, m):
        """Does the support of the level-`level` B-spline B lie in Omega^m (m >= level)?"""
        if m >= self.L:
            return False
        r = 2 ** (m - level)
        return all(
            (r * a + x, r * b + y) in self.omega[m]
            for a in self.cells(level, B[0])
            for b in self.cells(level, B[1])
            for x in range(r)
            for y in range(r)
        )

    def refine(self, level, coarse_cells):
        """Add to Omega^level the given cells of level - 1, which must lie in Omega^(level-1)."""
        for a, b in coarse_cells:
            if (a, b) not in self.omega[level - 1]:
                raise ValueError("Omega^l must lie inside Omega^(l-1)")
            self.omega[level] |= {(2 * a + x, 2 * b + y) for x in (0, 1) for y in (0, 1)}

    def kraft(self):
        return [
            (l, (i, j))
            for l in range(self.L)
            for i in range(self.size(l))
            for j in range(self.size(l))
            if self.inside(l, (i, j), l) and not self.inside(l, (i, j), l + 1)
        ]

    def lift(self, c, level):
        """Coefficients on level `level` B-splines to coefficients on level `level` + 1."""
        out = {}
        R = self.R[level]
        for (i, j), x in c.items():
            for a, u in R[i].items():
                for b, v in R[j].items():
                    out[(a, b)] = out.get((a, b), Fraction(0)) + x * u * v
        return out

    def to_finest(self, c, level):
        for k in range(level, self.L - 1):
            c = self.lift(c, k)
        return c

    def basis(self):
        """{(level, (i, j)): truncated function as finest-level coefficients}."""
        out = {}
        for l, B in self.kraft():  # @line L1
            c = {B: Fraction(1)}  # @line L2
            for k in range(l + 1, self.L):  # @line L3
                c = self.lift(c, k - 1)  # @line L4
                c = {g: x for g, x in c.items() if not self.inside(k, g, k)}  # @line L5
            out[(l, B)] = self.to_finest(c, self.L - 1) if c else {}  # @line L6
        return out

    def evaluate(self, coeffs, x, y):
        """sum over {(i, j): c} of c times the finest-level tensor B-spline at (x, y)."""
        kn, p = self.knots[-1], self.p
        total = Fraction(0)  # @line L7
        for (i, j), c in coeffs.items():  # @line L8
            total += c * bspline(kn, i, p, x) * bspline(kn, j, p, y)  # @line L9
        return total  # @line L10

    def plain(self, level, B):
        """The untruncated B-spline in the finest level, for comparison."""
        return self.to_finest({B: Fraction(1)}, level)


def rank(vectors):
    """Exact rank of sparse vectors given as dicts, by incremental elimination."""
    pivots = {}
    for v in vectors:
        v = {k: x for k, x in v.items() if x}
        while v:
            k = min(v)
            if k not in pivots:
                pivots[k] = v
                break
            p = pivots[k]
            f = v[k] / p[k]
            for kk, x in p.items():
                v[kk] = v.get(kk, Fraction(0)) - f * x
            v = {kk: x for kk, x in v.items() if x}
    return len(pivots)
