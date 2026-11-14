# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kinematic-fixture-analysis/. The authors are listed in prov/E79S9A.jsonl.

"""Kinematic fixture analysis in the sense of Asada and By (1985).

Model: a rigid part, frictionless point contacts, small motions. A contact
is a pair (p, n): the contact point p and the normal n that points from the
locator into the part. n need not have unit length; every answer here is
unchanged when a normal is scaled by a positive number.

A twist is xi = (dx, dy, dz, wx, wy, wz). The first-order change of the gap
at contact i is J_i . xi with J_i = (n_i, p_i x n_i).

All arithmetic is exact (Fraction), so a rank or a sign is never wrong
because of rounding.
"""

from collections import namedtuple
from fractions import Fraction
from itertools import combinations
from math import gcd

FixtureReport = namedtuple(
    "FixtureReport", ["rank", "deterministic", "null_twists", "detach_twist", "form_closure"]
)


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def jacobian(contacts):
    """The locator Jacobian: one row (n, p x n) per contact, as Fractions."""
    rows = []
    for p, n in contacts:
        m = cross(p, n)
        rows.append([Fraction(v) for v in (n[0], n[1], n[2], m[0], m[1], m[2])])  # @line L1
    return rows


def _echelon(rows, ncols):
    """Reduced row echelon form. Returns (matrix, pivot columns)."""
    a = [[Fraction(v) for v in r] for r in rows]
    pivots = []
    r = 0
    for c in range(ncols):
        if r == len(a):
            break
        piv = None
        for i in range(r, len(a)):
            if a[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        inv = 1 / a[r][c]
        a[r] = [v * inv for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
    return a, pivots


def rank(rows, ncols=6):
    return len(_echelon(rows, ncols)[1])


def null_space(rows, ncols=6):
    """A basis of {x : rows x = 0}, each vector with integer entries."""
    a, pivots = _echelon(rows, ncols)
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for f in free:
        x = [Fraction(0)] * ncols
        x[f] = Fraction(1)
        for i, c in enumerate(pivots):
            x[c] = -a[i][f]
        basis.append(_integer(x))
    return basis


def _integer(x):
    """Scale a rational vector by a positive number to coprime integers."""
    den = 1
    for v in x:
        den = den * v.denominator // gcd(den, v.denominator)
    ints = [int(v * den) for v in x]
    g = 0
    for v in ints:
        g = gcd(g, abs(v))
    if g > 1:
        ints = [v // g for v in ints]
    return [Fraction(v) for v in ints]


def solve_square(rows, b):
    """Solve rows x = b for a square invertible matrix; None if singular."""
    n = len(rows)
    aug = [list(r) + [Fraction(v)] for r, v in zip(rows, b)]
    a, pivots = _echelon(aug, n)
    if len(pivots) < n:
        return None
    return [a[i][n] for i in range(n)]


def apply(rows, xi):
    return [dot(r, xi) for r in rows]


def detach_twist(rows):
    """A twist xi with J xi >= 0 and J xi != 0, or None if there is none.

    If the cone spanned by the rows is not their whole span, it has a facet,
    and a facet contains rank - 1 independent rows. The twists that are
    orthogonal to those rows give, modulo the null space of J, a single
    line of gap vectors J xi, and one of its two directions is >= 0.
    So trying every independent set of rank - 1 rows finds a detaching
    twist whenever one exists.
    """
    r = rank(rows)
    if r == 0:
        return None
    for subset in combinations(range(len(rows)), r - 1):  # @line L4
        sub = [rows[i] for i in subset]
        if rank(sub) != r - 1:
            continue
        for b in null_space(sub):  # @line L5
            g = apply(rows, b)
            if all(v == 0 for v in g):
                continue
            if all(v >= 0 for v in g):  # @line L6
                return b
            if all(v <= 0 for v in g):  # @line L7
                return [-v for v in b]
            break
    return None  # @line L8


def analyze(contacts):
    """Rank, first-order determinism, and loading or unloading of a fixture.

    deterministic: rank J = 6, so J xi = 0 only for xi = 0.
    null_twists: a basis of the twists that change no gap to first order.
    detach_twist: a twist that opens some gap and closes none, or None.
    form_closure: deterministic and no detaching twist, so the contacts
    alone stop every small motion.
    """
    rows = jacobian(contacts)
    r = rank(rows)  # @line L2
    nulls = null_space(rows) if r < 6 else []  # @line L3
    d = detach_twist(rows)
    return FixtureReport(r, r == 6, nulls, d, r == 6 and d is None)


def error_twist(contacts, errors):
    """For six locators with rank 6: the twist that a set of small locator
    errors causes, the solution of J xi = errors. None if J is singular."""
    rows = jacobian(contacts)
    if len(rows) != 6:
        raise ValueError("error_twist needs exactly six locators")
    return solve_square(rows, errors)
