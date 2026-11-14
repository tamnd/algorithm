# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bezier-extraction/. The authors are listed in prov/5HN7GF.jsonl.

"""Bezier extraction of a clamped B-spline basis, after Borden, Scott, Evans and Hughes.

extract(U, p) returns one (p+1) x (p+1) matrix C^e per element. Row a of C^e
gives the local B-spline N_{k-p+a} (k the span of the element) as a
combination of the p + 1 Bernstein polynomials of the element:
N^e(u) = C^e B(s), s = (u - u_left) / (u_right - u_left).
The loop follows Algorithm 1 of the paper, with 1-based indices inside.
"""

from fractions import Fraction
from math import comb


def identity(n):
    return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def extract(U, p):
    """Element extraction operators of a clamped knot vector U of degree p."""
    m = len(U)
    u = [None] + [Fraction(x) for x in U]  # u[1..m]
    one = lambda: [[None] * (p + 2)] + [[None] + row for row in identity(p + 1)]
    a, b, nb = p + 1, p + 2, 1  # @line L1
    C = {1: one()}
    alphas = [None] * (p + 2)
    while b < m:  # @line L2
        C[nb + 1] = one()  # @line L3
        i = b
        while b < m and u[b + 1] == u[b]:  # @line L4
            b += 1
        mult = b - i + 1  # @line L5
        if mult < p:  # @line L6
            numer = u[b] - u[a]
            for j in range(p, mult, -1):  # @line L7
                alphas[j - mult] = numer / (u[a + j] - u[a])
            r = p - mult  # @line L8
            for j in range(1, r + 1):  # @line L9
                save = r - j + 1
                s = mult + j  # @line L10
                for k in range(p + 1, s, -1):  # @line L11
                    al = alphas[k - s]
                    for row in range(1, p + 2):
                        C[nb][row][k] = al * C[nb][row][k] + (1 - al) * C[nb][row][k - 1]
                if b < m:  # @line L12
                    for t in range(j + 1):
                        C[nb + 1][save + t][save] = C[nb][p - j + 1 + t][p + 1]
        nb += 1  # @line L13
        if b < m:  # @line L14
            a, b = b, b + 1
    return [[row[1:] for row in C[e][1:]] for e in range(1, nb)]  # @line L15


def elements(U):
    """The nonempty knot spans [u_k, u_{k+1}) with their span index k."""
    return [(k, U[k], U[k + 1]) for k in range(len(U) - 1) if U[k] < U[k + 1]]


def bernstein(p, s):
    return [comb(p, j) * s**j * (1 - s) ** (p - j) for j in range(p + 1)]


def local_basis(Ce, p, s):
    """N^e = C^e B(s) for the local parameter s in [0, 1]."""
    B = bernstein(p, s)
    return [sum(c * x for c, x in zip(row, B)) for row in Ce]


def rational_local_basis(Ce, w, p, s):
    """NURBS: R^e = W^e C^e B / W with the weight function W = (C^e^T w) . B."""
    N = local_basis(Ce, p, s)
    W = sum(wa * na for wa, na in zip(w, N))
    return [wa * na / W for wa, na in zip(w, N)]


def bezier_points(Ce, P):
    """Bezier control points of an element: (C^e)^T applied to the local points."""
    n = len(Ce)
    return [tuple(sum(Ce[a][j] * P[a][c] for a in range(n)) for c in range(len(P[0]))) for j in range(n)]
