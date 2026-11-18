# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deformation-gradient/. The authors are listed in prov/1C1F35.jsonl.
"""The deformation gradient of a linear triangle (2D) or tetrahedron (3D).

For rest vertices X_0, ..., X_d and current vertices x_0, ..., x_d, the edge
matrices are D_m = [X_1 - X_0, ..., X_d - X_0] and D_s = [x_1 - x_0, ...],
and F = D_s D_m^(-1). The quantities derived from F are J = det F, the right
Cauchy-Green tensor C = F^T F, the Green strain E = (C - I) / 2 and the
polar decomposition F = R S, which comes from anim.polar.

Matrices are lists of rows, and vectors are tuples or lists.
"""

import math

from anim import det, inv, mul, polar, transpose


def edge_matrix(points):
    """D = [p_1 - p_0, ..., p_d - p_0] as a d by d matrix (the edges are columns)."""
    d = len(points) - 1
    return [[points[k + 1][i] - points[0][i] for k in range(d)] for i in range(d)]


def deformation_gradient(rest, cur):
    """F = D_s D_m^(-1) for one simplex with rest vertices rest and current vertices cur."""
    dm = edge_matrix(rest)
    if det(dm) == 0.0:
        raise ValueError("the rest simplex is degenerate")
    return mul(edge_matrix(cur), inv(dm))


def right_cauchy_green(f):
    """C = F^T F."""
    return mul(transpose(f), f)


def green_strain(f):
    """E = (F^T F - I) / 2."""
    c = right_cauchy_green(f)
    return [[0.5 * (c[i][j] - (1.0 if i == j else 0.0)) for j in range(len(f))] for i in range(len(f))]


def simplex_measure(points):
    """The signed area (2D) or volume (3D) of a simplex: det D / d!."""
    d = len(points) - 1
    return det(edge_matrix(points)) / math.factorial(d)


def polar_decomposition(f):
    """F = R S with det R = +1 and S symmetric; S is positive definite when det F > 0."""
    return polar(f)
