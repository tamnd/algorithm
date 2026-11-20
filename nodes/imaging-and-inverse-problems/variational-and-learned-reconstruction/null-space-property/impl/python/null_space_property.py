# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/null-space-property/. The authors are listed in prov/PPTQNH.jsonl.
"""Exact brute force check of the null space property of a small rational matrix.

A matrix is a list of m rows of length n with integer or Fraction entries.
The null space constant of order s is

    theta_s(A) = max over nonzero v with A v = 0 of (sum of the s largest |v_i|) / ||v||_1.

A has the null space property of order s if and only if theta_s(A) < 1/2.
The function in the maximum is convex and the set {v : A v = 0, ||v||_1 <= 1}
is a polytope, so the maximum is reached at a vertex. Each vertex spans the
one dimensional null space of A restricted to its support, and its support
has at most rank(A) + 1 entries. The check enumerates those supports with
exact Fraction arithmetic. It takes time exponential in n: use it on tiny
matrices only.
"""

from fractions import Fraction
from itertools import combinations


def _rref(rows):
    """Reduced row echelon form (in place on a copy). Returns (matrix, pivot columns)."""
    a = [[Fraction(v) for v in row] for row in rows]
    m = len(a)
    t = len(a[0]) if a else 0
    pivots = []
    r = 0
    for c in range(t):
        p = next((i for i in range(r, m) if a[i][c] != 0), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        piv = a[r][c]
        a[r] = [v / piv for v in a[r]]
        for i in range(m):
            if i != r and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == m:
            break
    return a, pivots


def rank(a):
    return len(_rref(a)[1])


def null_vector(a, cols):
    """The null vector of A restricted to the columns cols, if that null space has dimension 1.

    Returns a list of Fractions indexed like cols, or None.
    """
    sub = [[row[j] for j in cols] for row in a]
    red, pivots = _rref(sub)
    t = len(cols)
    free = [c for c in range(t) if c not in pivots]
    if len(free) != 1:
        return None
    f = free[0]
    v = [Fraction(0)] * t
    v[f] = Fraction(1)
    for i, c in enumerate(pivots):
        v[c] = -red[i][f]
    return v


def top_mass(v, s):
    """The sum of the s largest absolute values of v."""
    return sum(sorted((abs(x) for x in v), reverse=True)[:s])


def nsp_constant(a, s):
    """Return (theta_s, v): the exact null space constant and a null vector that attains it.

    If A is injective, there is no nonzero null vector; then theta is 0 and v is None.
    """
    n = len(a[0])
    r = rank(a)  # @line L1
    theta, best = Fraction(0), None
    for t in range(1, min(n, r + 1) + 1):
        for cols in combinations(range(n), t):  # @line L2
            w = null_vector(a, cols)  # @line L3
            if w is None or any(x == 0 for x in w):
                continue
            v = [Fraction(0)] * n
            for j, x in zip(cols, w):
                v[j] = x
            ratio = top_mass(v, s) / sum(abs(x) for x in v)  # @line L4
            if ratio > theta:
                theta, best = ratio, v
    return theta, best  # @line L5


def has_nsp(a, s):
    """True if A has the null space property of order s."""
    return nsp_constant(a, s)[0] < Fraction(1, 2)


def failure_certificate(a, s):
    """If the property fails, return (x, z): x is s-sparse, A x = A z, z != x and ||z||_1 <= ||x||_1.

    Then l1 minimization cannot return x as its unique solution. Returns None if the property holds.
    """
    theta, v = nsp_constant(a, s)
    if theta < Fraction(1, 2):
        return None
    order = sorted(range(len(v)), key=lambda i: -abs(v[i]))[:s]
    x = [v[i] if i in order else Fraction(0) for i in range(len(v))]
    z = [Fraction(0) if i in order else -v[i] for i in range(len(v))]
    return x, z
