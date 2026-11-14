# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicitization/. The authors are listed in prov/FF7D9Q.jsonl.

"""Implicitization of a rational plane curve by the Sylvester resultant.

The curve is x = X(t) / W(t), y = Y(t) / W(t), with X, Y, W polynomials given
as coefficient lists from the constant term up, with integer or Fraction
entries. The implicit polynomial is

    F(x, y) = Res_t(X(t) - x W(t), Y(t) - y W(t)),

the determinant of the 2d x 2d Sylvester matrix of the two polynomials, both
taken with the formal degree d = max(deg X, deg Y, deg W). Its entries are
linear in x or in y, so F has degree at most d in x and at most d in y. The
code evaluates the determinant exactly at the (d + 1)^2 points of a grid and
interpolates. F is returned as a dictionary (a, b) -> coefficient of x^a y^b,
scaled to integer coefficients with no common factor and a positive leading
coefficient.
"""

from fractions import Fraction
from math import gcd
from typing import Sequence

from si1geom import det, solve


def sylvester(A: Sequence, B: Sequence, d: int) -> list:
    """The 2d x 2d Sylvester matrix of A and B, both of formal degree d.

    Row i < d holds the coefficients of t^(d-1-i) A, row d + i those of
    t^(d-1-i) B, highest power first."""
    a = [A[k] if k < len(A) else 0 for k in range(d, -1, -1)]
    b = [B[k] if k < len(B) else 0 for k in range(d, -1, -1)]
    rows = []
    for c in (a, b):
        for i in range(d):
            rows.append([0] * i + c + [0] * (d - 1 - i))
    return rows


def _interpolate(nodes: list, values: list) -> list:
    """Coefficients (constant first) of the polynomial through (nodes[k], values[k])."""
    V = [[Fraction(x) ** j for j in range(len(nodes))] for x in nodes]
    return solve(V, [Fraction(v) for v in values])


def implicitize(X: Sequence, Y: Sequence, W: Sequence) -> dict:
    d = max(len(X), len(Y), len(W)) - 1  # @line L1
    nodes = list(range(d + 1))
    R = [[None] * (d + 1) for _ in range(d + 1)]
    for i, x0 in enumerate(nodes):  # @line L2
        for j, y0 in enumerate(nodes):
            A = [Fraction(X[k] if k < len(X) else 0) - x0 * Fraction(W[k] if k < len(W) else 0) for k in range(d + 1)]  # @line L3
            B = [Fraction(Y[k] if k < len(Y) else 0) - y0 * Fraction(W[k] if k < len(W) else 0) for k in range(d + 1)]
            R[i][j] = det(sylvester(A, B, d))  # @line L4
    rows = [_interpolate(nodes, R[i]) for i in range(d + 1)]  # @line L5
    F = {}
    for b in range(d + 1):
        col = _interpolate(nodes, [rows[i][b] for i in range(d + 1)])
        for a in range(d + 1):
            if col[a] != 0:
                F[(a, b)] = col[a]
    return normalize(F)  # @line L6


def normalize(F: dict) -> dict:
    """Scale F to coprime integer coefficients, with the coefficient of the
    largest monomial (by total degree, then by the power of x) positive."""
    if not F:
        return {}
    den = 1
    for c in F.values():
        den = den * Fraction(c).denominator // gcd(den, Fraction(c).denominator)
    ints = {k: int(Fraction(c) * den) for k, c in F.items()}
    g = 0
    for c in ints.values():
        g = gcd(g, c)
    lead = max(ints, key=lambda e: (e[0] + e[1], e[0]))
    s = 1 if ints[lead] > 0 else -1
    return {k: s * c // g for k, c in ints.items()}


def eval_implicit(F: dict, x, y):
    return sum(c * x ** a * y ** b for (a, b), c in F.items())
