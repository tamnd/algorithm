# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tutte-embedding/. The authors are listed in prov/BD4HAH.jsonl.

"""Tutte embedding of a triangulated disk.

The boundary loop is pinned to the corners of a convex polygon, and each
inner vertex is put at a convex combination of its neighbours. The
positions solve one linear system. With Fraction weights and Fraction
corners the solve is exact, so the signs of the triangle orientations of
the result are exact too.
"""

import math
from fractions import Fraction

from mp3geom import boundary_loop, neighbours, orient2d, solve


def circle_polygon(k, denominator=10**6):
    """k rational points in strictly convex position on the unit circle, counterclockwise.

    The point of parameter t is ((1 - t^2) / (1 + t^2), 2 t / (1 + t^2)). It is
    on the circle exactly, and an increasing t goes counterclockwise.
    """
    pts = []
    for i in range(k):
        theta = -math.pi + 2 * math.pi * (i + 0.5) / k
        t = Fraction(math.tan(theta / 2)).limit_denominator(denominator)
        d = 1 + t * t
        pts.append(((1 - t * t) / d, 2 * t / d))
    return pts


def uniform_weights(faces):
    """lambda_ij = 1 / deg(i): Tutte's barycentric weights."""
    nb = neighbours(faces)
    return {i: {j: Fraction(1, len(nb[i])) for j in nb[i]} for i in nb}


def mean_value_weights(points, faces):
    """Floater's mean value weights of each vertex with respect to its 1-ring, in floating point.

    lambda_ij is proportional to (tan(a_(j-1)/2) + tan(a_j/2)) / |x_j - x_i|,
    where a_(j-1) and a_j are the angles at x_i of the two triangles at the
    edge ij. tan(a/2) = |d x e| / (|d| |e| + d . e), which has no cancellation
    for small angles.
    """
    w = {}
    for tri in faces:
        for k in range(3):
            i, j, l = tri[k], tri[(k + 1) % 3], tri[(k + 2) % 3]
            d = [float(points[j][c]) - float(points[i][c]) for c in range(len(points[i]))]
            e = [float(points[l][c]) - float(points[i][c]) for c in range(len(points[i]))]
            dd, ee = math.sqrt(sum(x * x for x in d)), math.sqrt(sum(x * x for x in e))
            de = sum(x * y for x, y in zip(d, e))
            if len(d) == 2:
                cr = abs(d[0] * e[1] - d[1] * e[0])
            else:
                cr = math.sqrt(sum(x * x for x in (d[1] * e[2] - d[2] * e[1], d[2] * e[0] - d[0] * e[2], d[0] * e[1] - d[1] * e[0])))
            half = cr / (dd * ee + de)
            wi = w.setdefault(i, {})
            wi[j] = wi.get(j, 0.0) + half / dd
            wi[l] = wi.get(l, 0.0) + half / ee
    for i in w:
        s = sum(w[i].values())
        for j in w[i]:
            w[i][j] /= s
    return w


def tutte_embedding(faces, corners, weights=None):
    """Positions of all vertices of the disk `faces`.

    corners[t] is the position of the t-th vertex of boundary_loop(faces).
    weights[i][j] > 0 with sum over j equal to 1, for each inner vertex i;
    the default is uniform_weights. Returns a dict vertex -> (x, y).
    """
    loop = boundary_loop(faces)  # @line L1
    if len(corners) != len(loop):
        raise ValueError("need one corner per boundary vertex")
    if weights is None:
        weights = uniform_weights(faces)
    pos = {v: tuple(c) for v, c in zip(loop, corners)}  # @line L2
    inner = sorted(v for v in neighbours(faces) if v not in pos)
    index = {v: r for r, v in enumerate(inner)}  # @line L3
    n = len(inner)
    zero = 0.0 if any(isinstance(x, float) for i in inner for x in weights[i].values()) else Fraction(0)
    a = [[zero + (r == c) for c in range(n)] for r in range(n)]  # @line L4
    b = [[zero, zero] for _ in range(n)]
    for i in inner:  # @line L5: row i is x_i - sum_j lambda_ij x_j = 0
        r = index[i]
        for j, lam in weights[i].items():
            if j in index:
                a[r][index[j]] -= lam  # @line L6
            else:
                b[r][0] += lam * pos[j][0]  # @line L7
                b[r][1] += lam * pos[j][1]
    if n:
        x = solve(a, b)  # @line L8
        for i in inner:
            pos[i] = (x[index[i]][0], x[index[i]][1])  # @line L9
    return pos  # @line L10


def is_valid_embedding(faces, pos):
    """True if every triangle has positive orientation. Exact for int or Fraction positions."""
    for a, b, c in faces:  # @line L11
        if orient2d(pos[a], pos[b], pos[c]) <= 0:
            return False  # @line L12
    return True  # @line L13
