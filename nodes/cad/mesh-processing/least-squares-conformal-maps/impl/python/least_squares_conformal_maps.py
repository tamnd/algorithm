# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-conformal-maps/. The authors are listed in prov/67C616.jsonl.

"""Least squares conformal maps (Levy, Petitjean, Ray and Maillot 2002).

Each triangle gets a 2D frame. For the corner positions q_0, q_1, q_2 of the
frame, as complex numbers, and the unknown images U_j = u_j + i v_j, the
Cauchy-Riemann residual of the triangle is

    s_T = sum_j eps_j U_j,   eps_j = q_(j+2) - q_(j+1),

and the energy is E = sum_T |s_T|^2 / (4 A_T). Two pinned vertices make the
minimizer unique in the usual case. The normal equations are solved by
Gaussian elimination. For a planar input with int or Fraction coordinates
the frames are the coordinates themselves, and the solve is exact.
"""

import math
from fractions import Fraction

from mp3geom import orient2d, solve


def triangle_frame(p0, p1, p2):
    """The corners of a triangle in a 2D frame with the same orientation, and its area.

    A 2D triangle is kept as it is (exact for int or Fraction). A 3D
    triangle is put in its plane with p0 at the origin and p1 on the x-axis,
    in floating point.
    """
    if len(p0) == 2:
        return (tuple(p0), tuple(p1), tuple(p2)), Fraction(orient2d(p0, p1, p2), 2)
    e1 = [float(p1[k]) - float(p0[k]) for k in range(3)]
    e2 = [float(p2[k]) - float(p0[k]) for k in range(3)]
    l1 = math.sqrt(sum(x * x for x in e1))
    x2 = sum(a * b for a, b in zip(e1, e2)) / l1
    c = (e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0])
    y2 = math.sqrt(sum(x * x for x in c)) / l1
    return ((0.0, 0.0), (l1, 0.0), (x2, y2)), l1 * y2 / 2


def residual_rows(q):
    """The real and imaginary rows of s_T: coefficients of (u_j, v_j), j = 0, 1, 2."""
    re, im = [], []
    for j in range(3):
        a, b = q[(j + 2) % 3], q[(j + 1) % 3]
        er, ei = a[0] - b[0], a[1] - b[1]        # eps_j = er + i ei
        re += [er, -ei]                          # Re(eps_j U_j) = er u_j - ei v_j
        im += [ei, er]                           # Im(eps_j U_j) = ei u_j + er v_j
    return re, im


def lscm(points, faces, pins):
    """Minimize the LSCM energy with pins = {vertex: (u, v)}. Returns {vertex: (u, v)}.

    Raises ValueError if the normal matrix is singular, which happens when
    the pins do not fix the map (see the page for when that is).
    """
    verts = sorted({v for f in faces for v in f})
    free = [v for v in verts if v not in pins]
    col = {v: k for k, v in enumerate(free)}
    exact = all(len(points[v]) == 2 and not isinstance(points[v][0], float) for v in verts)
    zero = Fraction(0) if exact else 0.0
    n = 2 * len(free)
    a = [[zero] * n for _ in range(n)]
    b = [[zero] for _ in range(n)]
    for f in faces:
        q, area = triangle_frame(*(points[v] for v in f))  # @line L1
        if area <= 0:
            raise ValueError("a triangle has no positive area")
        w = 1 / (4 * area)  # @line L2
        for row in residual_rows(q):  # @line L3
            idx, known = [], zero  # @line L4
            for j, v in enumerate(f):
                for c in range(2):
                    coef = row[2 * j + c]
                    if v in pins:
                        known += coef * pins[v][c]
                    else:
                        idx.append((2 * col[v] + c, coef))
            for r, cr in idx:  # @line L5: add w * row^T row to the normal matrix
                b[r][0] -= w * cr * known
                for s, cs in idx:
                    a[r][s] += w * cr * cs
    x = solve(a, b) if n else []  # @line L6
    out = {v: tuple(pins[v]) for v in pins}
    for v in free:
        out[v] = (x[2 * col[v]][0], x[2 * col[v] + 1][0])
    return out  # @line L7


def lscm_energy(points, faces, uv):
    """E = sum_T |s_T|^2 / (4 A_T)."""
    e = 0
    for f in faces:
        q, area = triangle_frame(*(points[v] for v in f))
        re, im = residual_rows(q)
        x = [uv[v][c] for v in f for c in range(2)]
        sr = sum(r * y for r, y in zip(re, x))
        si = sum(r * y for r, y in zip(im, x))
        e += (sr * sr + si * si) / (4 * area)
    return e


def dirichlet_energy(points, faces, uv):
    """E_D = (1/2) sum_T A_T (|grad u|^2 + |grad v|^2) of the piecewise linear map."""
    e = 0
    for f in faces:
        q, area = triangle_frame(*(points[v] for v in f))
        for c in range(2):
            gx = gy = 0
            for j, v in enumerate(f):
                a, b = q[(j + 2) % 3], q[(j + 1) % 3]
                # grad phi_j = rot90(eps_j) / (2A) = (-(a_y - b_y), a_x - b_x) / (2A)
                gx += uv[v][c] * (b[1] - a[1])
                gy += uv[v][c] * (a[0] - b[0])
            e += (gx * gx + gy * gy) / (8 * area)
    return e


def image_area(faces, uv):
    """Signed area of the image, sum over triangles of ORIENT2D / 2."""
    return sum(orient2d(uv[a], uv[b], uv[c]) for a, b, c in faces) / 2
