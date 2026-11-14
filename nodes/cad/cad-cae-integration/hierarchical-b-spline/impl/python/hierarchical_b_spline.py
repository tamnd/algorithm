# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierarchical-b-spline/. The authors are listed in prov/4MZ00N.jsonl.

"""Bivariate hierarchical B-splines with Kraft's selection, in exact arithmetic.

Level l has the open uniform knot vector of degree p on [0, n0] with spacing
2^-l in each direction, so the spline spaces of the levels are nested. A
B-spline of level l is a pair (i, j) of indices into that knot vector. A cell
of level l is a pair (a, b) for the square [a, a + 1] x [b, b + 1] scaled by
2^-l.

The domains Omega^0 = [0, n0]^2 and Omega^1, ..., Omega^(L-1) are sets of
cells, Omega^l a union of cells of level l - 1 inside Omega^(l-1).
Omega^L is empty. The hierarchical basis has the B-splines of level l whose
support lies in Omega^l but not in Omega^(l+1).
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
    fine = open_knots(n0, p, level + 1)
    new = sorted(set(fine) - set(coarse))
    R = []
    for i in range(len(coarse) - p - 1):
        knots, c = list(coarse), [Fraction(int(r == i)) for r in range(len(coarse) - p - 1)]
        for u in new:
            knots, c = insert_knot(knots, c, u, p)
        assert knots == fine
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


class Hierarchy:
    def __init__(self, n0, p, levels):
        self.n0, self.p, self.L = n0, p, levels
        self.knots = [open_knots(n0, p, l) for l in range(levels)]
        self.R = [two_scale(n0, p, l) for l in range(levels - 1)]
        self.omega = [{(a, b) for a in range(n0) for b in range(n0)}] + [set() for _ in range(levels - 1)]

    def size(self, level):
        return self.n0 * 2**level + self.p

    def cells(self, level, i):
        """The cells of the level, in one direction, where N_i is not zero."""
        return range(max(i - self.p, 0), min(i, self.n0 * 2**level - 1) + 1)

    def support(self, level, B):
        i, j = B
        return [(a, b) for a in self.cells(level, i) for b in self.cells(level, j)]

    def inside(self, level, B, m):
        """Does the support of the level-`level` function B lie in Omega^m (m = level or level + 1)?"""
        if m >= self.L:
            return False
        if m == level:
            return all(c in self.omega[m] for c in self.support(level, B))
        return all((2 * a + x, 2 * b + y) in self.omega[m] for a, b in self.support(level, B) for x in (0, 1) for y in (0, 1))

    def refine(self, level, coarse_cells):
        """Add to Omega^level the given cells of level - 1, which must lie in Omega^(level-1)."""
        for a, b in coarse_cells:
            if (a, b) not in self.omega[level - 1]:
                raise ValueError("Omega^l must lie inside Omega^(l-1)")
            self.omega[level] |= {(2 * a + x, 2 * b + y) for x in (0, 1) for y in (0, 1)}

    def basis(self):
        """Kraft's selection: a list of (level, (i, j))."""
        H = []
        for l in range(self.L):  # @line L1
            for i in range(self.size(l)):  # @line L2
                for j in range(self.size(l)):
                    if self.inside(l, (i, j), l) and not self.inside(l, (i, j), l + 1):  # @line L3
                        H.append((l, (i, j)))  # @line L4
        return H

    def evaluate(self, coeffs, x, y):
        """sum of c * B(x, y) over a dict {(level, (i, j)): c}."""
        total = Fraction(0)  # @line L5
        for (l, (i, j)), c in coeffs.items():  # @line L6
            total += c * bspline(self.knots[l], i, self.p, x) * bspline(self.knots[l], j, self.p, y)  # @line L7
        return total  # @line L8

    def finest(self, level, B):
        """B as {(i, j): c} in the tensor B-splines of the finest level, by the two-scale relation."""
        cs, ct = {B[0]: Fraction(1)}, {B[1]: Fraction(1)}
        for l in range(level, self.L - 1):
            cs = _apply(self.R[l], cs)
            ct = _apply(self.R[l], ct)
        return {(a, b): x * y for a, x in cs.items() for b, y in ct.items()}


def _apply(R, c):
    out = {}
    for i, x in c.items():
        for j, y in R[i].items():
            out[j] = out.get(j, Fraction(0)) + x * y
    return out


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
