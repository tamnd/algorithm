# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barvinok-algorithm/. The authors are listed in prov/EFNZQ1.jsonl.

"""Barvinok's algorithm in dimension 2.

The input is a convex polygon with rational vertices. The algorithm writes the
generating function of its lattice points as a signed sum of rational functions
of unimodular cones (Brion's theorem plus Barvinok's signed decomposition of
the dual cones), then evaluates the sum at z = (1, 1) through a limit.
"""

from fractions import Fraction
from math import gcd


def _det(p, q):
    return p[0] * q[1] - p[1] * q[0]


def _rot(p):
    """Rotate by 90 degrees counterclockwise."""
    return (-p[1], p[0])


def _neg(p):
    return (-p[0], -p[1])


def _primitive(p):
    """The primitive integer vector in the direction of the nonzero rational vector p."""
    x, y = Fraction(p[0]), Fraction(p[1])
    den = x.denominator * y.denominator
    a, b = int(x * den), int(y * den)
    g = gcd(a, b)
    return (a // g, b // g)


def _sign(x):
    return (x > 0) - (x < 0)


def shortest_vector(u, v):
    """Lagrange-Gauss reduction: a shortest nonzero vector of the integer lattice with basis u, v."""

    def n2(x):
        return x[0] * x[0] + x[1] * x[1]

    if n2(u) > n2(v):
        u, v = v, u
    while True:
        nu = n2(u)
        dot = u[0] * v[0] + u[1] * v[1]
        m = (2 * dot + nu) // (2 * nu)  # the integer nearest to dot / nu
        v = (v[0] - m * u[0], v[1] - m * u[1])
        if n2(v) >= nu:
            return u
        u, v = v, u


def decompose(p, q):
    """Signed unimodular decomposition of cone(p, q), modulo lower-dimensional cones.

    Returns a list of (sign, p_i, q_i) with |det(p_i, q_i)| = 1.
    """
    out = []
    stack = [(1, p, q)]
    while stack:  # @line L4
        eps, p, q = stack.pop()
        d = _det(p, q)
        if abs(d) == 1:
            out.append((eps, p, q))
            continue
        # @line L5: a short w = l1 p + l2 q in Z^2; the coefficient lattice is G^-1 Z^2, scaled by d
        mu = shortest_vector((q[1], -p[1]), (-q[0], p[0]))
        l1, l2 = Fraction(mu[0], d), Fraction(mu[1], d)
        if l1 < 0 and l2 < 0:
            l1, l2 = -l1, -l2
        w = (int(l1 * p[0] + l2 * q[0]), int(l1 * p[1] + l2 * q[1]))
        if l1 != 0:  # @line L6
            stack.append((eps * _sign(l1), w, q))
        if l2 != 0:
            stack.append((eps * _sign(l2), p, w))
    return out


def _dual_basis(p, q):
    """The generators of the dual of the unimodular cone cone(p, q)."""
    delta = _det(p, q)
    r = _rot(p)
    s = _rot(q)
    return (delta * r[0], delta * r[1]), (-delta * s[0], -delta * s[1])


def _constant_term(a, b, c):
    """Constant term at t = 0 of exp(a t) / ((1 - exp(b t)) (1 - exp(c t))), b, c != 0."""
    a, b, c = Fraction(a), Fraction(b), Fraction(c)
    return (a * a / 2 - a * (b + c) / 2 + (b * b + c * c) / 12 + b * c / 4) / (b * c)


def signed_cones(vertices):
    """Brion's theorem plus the signed decomposition: a list of (sign, u, r, s).

    Each entry stands for the rational function sign * z^u / ((1 - z^r)(1 - z^s)),
    where r, s is a basis of Z^2 and u is the first lattice point of the
    affine cone v + cone(r, s).
    """
    verts = [(Fraction(x), Fraction(y)) for x, y in vertices]
    m = len(verts)
    if m < 3:
        raise ValueError("a polygon needs at least 3 vertices")
    for i in range(m):
        a = (verts[(i + 1) % m][0] - verts[i][0], verts[(i + 1) % m][1] - verts[i][1])
        b = (verts[(i + 2) % m][0] - verts[(i + 1) % m][0], verts[(i + 2) % m][1] - verts[(i + 1) % m][1])
        if _det(a, b) <= 0:
            raise ValueError("the vertices must form a strictly convex polygon in counterclockwise order")
    out = []  # @line L1
    for i in range(m):  # @line L2
        v = verts[i]
        a = _primitive((verts[(i + 1) % m][0] - v[0], verts[(i + 1) % m][1] - v[1]))
        b = _primitive((verts[i - 1][0] - v[0], verts[i - 1][1] - v[1]))
        p, q = _rot(a), _neg(_rot(b))  # @line L3: the dual of the tangent cone cone(a, b)
        for eps, pi, qi in decompose(p, q):
            r, s = _dual_basis(pi, qi)  # @line L7
            d = _det(r, s)
            alpha = (v[0] * s[1] - v[1] * s[0]) / d  # v = alpha r + beta s
            beta = (r[0] * v[1] - r[1] * v[0]) / d
            ka, kb = -((-alpha.numerator) // alpha.denominator), -((-beta.numerator) // beta.denominator)
            u = (ka * r[0] + kb * s[0], ka * r[1] + kb * s[1])  # @line L8
            out.append((eps, u, r, s))
    return out


def barvinok_count(vertices):
    """The number of integer points in the closed convex polygon with the given vertices.

    vertices is a list of points (x, y) with int or Fraction coordinates, in
    counterclockwise order, with every turn strictly to the left.
    """
    cones = signed_cones(vertices)
    gens = [g for _, _, r, s in cones for g in (r, s)]
    lam = None
    k = 0
    while lam is None:  # @line L9: a direction that is not orthogonal to any generator
        cand = (1, k)
        if all(cand[0] * g[0] + cand[1] * g[1] != 0 for g in gens):
            lam = cand
        k += 1
    total = Fraction(0)
    for eps, u, r, s in cones:  # @line L10
        dot = lambda g: lam[0] * g[0] + lam[1] * g[1]
        total += eps * _constant_term(dot(u), dot(r), dot(s))
    if total.denominator != 1:
        raise ArithmeticError("the sum is not an integer")
    return int(total)
