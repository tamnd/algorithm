# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vc-dimension/. The authors are listed in prov/08SW3R.jsonl.

"""Brute force shattering checks and the VC dimension of a class on a finite set of points.

A class is given by a test realizable(points, labels) that says whether some hypothesis
of the class gives the labels (0 or 1) to the points. All tests are exact: they use
integers and fractions.Fraction, never floats.
"""

from fractions import Fraction
from itertools import combinations, product


def is_shattered(points, realizable):
    """True when the class gives all 2^k labelings to the k points."""
    k = len(points)
    return all(realizable(points, labels) for labels in product((0, 1), repeat=k))  # @line L5


def vc_dimension_on(domain, realizable):
    """The largest k such that some k points of the domain are shattered.

    A subset of a shattered set is shattered, so the search stops at the first size
    with no shattered set."""
    best = 0  # @line L1
    for k in range(1, len(domain) + 1):  # @line L2
        found = False  # @line L3
        for c in combinations(domain, k):  # @line L4
            if is_shattered(list(c), realizable):  # @line L5
                found = True
                break
        if not found:  # @line L6
            return best
        best = k  # @line L7
    return best  # @line L8


def finite_class(hypotheses):
    """A finite class over domain indices: each hypothesis is a tuple of labels."""
    def realizable(points, labels):
        return any(all(h[p] == l for p, l in zip(points, labels)) for h in hypotheses)
    return realizable


def interval_realizable(points, labels):
    """Intervals [a, b] on the line: label 1 inside, 0 outside."""
    pos = [p for p, l in zip(points, labels) if l == 1]
    if not pos:
        return True
    lo, hi = min(pos), max(pos)
    return all(not (lo <= p <= hi) for p, l in zip(points, labels) if l == 0)


def rectangle_realizable(points, labels):
    """Axis aligned rectangles in the plane: label 1 inside, 0 outside."""
    pos = [p for p, l in zip(points, labels) if l == 1]
    if not pos:
        return True
    x0, x1 = min(p[0] for p in pos), max(p[0] for p in pos)
    y0, y1 = min(p[1] for p in pos), max(p[1] for p in pos)
    return all(not (x0 <= p[0] <= x1 and y0 <= p[1] <= y1)
               for p, l in zip(points, labels) if l == 0)


def _feasible(rows):
    """Fourier-Motzkin elimination for a system of rows (a, c) that means a . v >= c.
    Returns True when some real vector v satisfies all rows. Exact over Fraction."""
    rows = [([Fraction(x) for x in a], Fraction(c)) for a, c in rows]
    nvars = len(rows[0][0]) if rows else 0
    for j in range(nvars):
        pos = [r for r in rows if r[0][j] > 0]
        neg = [r for r in rows if r[0][j] < 0]
        new = [r for r in rows if r[0][j] == 0]
        for ap, cp in pos:
            for aq, cq in neg:
                sp, sq = ap[j], -aq[j]
                a = [x / sp + y / sq for x, y in zip(ap, aq)]
                new.append((a, cp / sp + cq / sq))
        rows = new
    return all(c <= 0 for _, c in rows)


def halfspace_realizable(points, labels, bias=True):
    """Halfspaces x -> 1[w . x + b >= 0] in R^d (b = 0 when bias is False).

    With a bias, a labeling of a finite set is realizable exactly when some (w, b)
    gives y (w . x + b) >= 1 for all points, with y = +1 or -1: shift b and scale.
    Without a bias, this tests strict separation, sign(w . x) = y on each point."""
    rows = []
    for p, l in zip(points, labels):
        y = 1 if l == 1 else -1
        a = [y * Fraction(x) for x in p] + ([y] if bias else [])
        rows.append((a, 1))
    return _feasible(rows)


def homogeneous_halfspace_realizable(points, labels):
    return halfspace_realizable(points, labels, bias=False)


def sine_label(theta_over_pi, x):
    """h_theta(x) = 1 when sin(theta x) > 0, else 0, for rational theta / pi and x.

    sin(pi r) > 0 exactly when r is not an integer and floor(r) is even."""
    r = Fraction(theta_over_pi) * Fraction(x)
    if r.denominator == 1:
        return 0
    return 1 if (r.numerator // r.denominator) % 2 == 0 else 0


def sine_points(k):
    """The points x_i = 10^(-i), i = 1 .. k."""
    return [Fraction(1, 10 ** i) for i in range(1, k + 1)]


def sine_theta_over_pi(labels):
    """theta / pi = 1 + sum of 10^i over the points i with label 0. Then h_theta gives
    the labels to sine_points(len(labels))."""
    return 1 + sum(10 ** i for i, l in enumerate(labels, start=1) if l == 0)


def sine_realizable(points, labels):
    """Realizability for the sine class on the points sine_points(k), by the witness."""
    t = sine_theta_over_pi(labels)
    return all(sine_label(t, x) == l for x, l in zip(points, labels))
