# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-slicing/. The authors are listed in prov/YQA8PY.jsonl.

"""Direct slicing of a CSG solid built from quadric half-spaces.

A leaf of the tree is a symmetric 4 x 4 matrix Q. A point p = (x, y, z) is
inside the leaf when X^T Q X <= 0 with X = (x, y, z, 1). Spheres, cylinders,
cones and planes are leaves of this form. Inner nodes are ("union", A, B),
("inter", A, B) and ("diff", A, B).

The plane z = Z cuts each leaf in a conic, given by the symmetric 3 x 3 matrix
M with [x y 1] M [x y 1]^T = X^T Q X. With rational input every entry of M is
rational, so the section is exact. The only approximation is the optional
polyline that is made for the printer, and its error is bounded by tol.
"""

import math
from fractions import Fraction as F

# ---------------------------------------------------------------- leaves


def sphere(center, r2):
    """Ball |p - c|^2 - r2 <= 0. r2 is the squared radius."""
    cx, cy, cz = (F(v) for v in center)
    q = [[F(0)] * 4 for _ in range(4)]
    for i in range(3):
        q[i][i] = F(1)
    q[0][3] = q[3][0] = -cx
    q[1][3] = q[3][1] = -cy
    q[2][3] = q[3][2] = -cz
    q[3][3] = cx * cx + cy * cy + cz * cz - F(r2)
    return q


def cylinder(point, axis, r2):
    """Infinite solid cylinder |p - a|^2 - ((p - a).u)^2 / |u|^2 - r2 <= 0."""
    p = [F(v) for v in point]
    a = [F(v) for v in axis]
    n2 = sum(v * v for v in a)
    if n2 == 0:
        raise ValueError("zero axis")
    # quadratic part I - a a^T / |a|^2
    m = [[(F(1) if i == j else F(0)) - a[i] * a[j] / n2 for j in range(3)] for i in range(3)]
    mp = [sum(m[i][j] * p[j] for j in range(3)) for i in range(3)]
    q = [[F(0)] * 4 for _ in range(4)]
    for i in range(3):
        for j in range(3):
            q[i][j] = m[i][j]
        q[i][3] = q[3][i] = -mp[i]
    q[3][3] = sum(p[i] * mp[i] for i in range(3)) - F(r2)
    return q


def half_space(normal, offset):
    """Half-space n.p - offset <= 0, a quadric with no quadratic part."""
    n = [F(v) for v in normal]
    q = [[F(0)] * 4 for _ in range(4)]
    for i in range(3):
        q[i][3] = q[3][i] = n[i] / 2
    q[3][3] = -F(offset)
    return q


def quadric_value(q, p):
    x = [F(p[0]), F(p[1]), F(p[2]), F(1)]
    return sum(x[i] * q[i][j] * x[j] for i in range(4) for j in range(4))


def inside_3d(tree, p):
    """Exact membership of a 3D point, used as the reference."""
    if tree[0] == "leaf":
        return quadric_value(tree[1], p) <= 0
    a, b = inside_3d(tree[1], p), inside_3d(tree[2], p)
    return combine(tree[0], a, b)


def combine(op, a, b):
    if op == "union":
        return a or b
    if op == "inter":
        return a and b
    if op == "diff":
        return a and not b
    raise ValueError(op)


# ---------------------------------------------------------------- section


def section(q, z):
    """The conic matrix M of the leaf q on the plane z = Z. Exact."""
    z = F(z)
    m = [[F(0)] * 3 for _ in range(3)]
    for i in range(2):
        for j in range(2):
            m[i][j] = q[i][j]
        m[i][2] = m[2][i] = q[i][2] * z + q[i][3]
    m[2][2] = q[2][2] * z * z + 2 * q[2][3] * z + q[3][3]
    return m


def slice_tree(tree, z):
    """Lines L1 and L2: replace every quadric leaf by its conic."""
    if tree[0] == "leaf":
        return ("leaf", section(tree[1], z))  # @line L1
    return (tree[0], slice_tree(tree[1], z), slice_tree(tree[2], z))


def conic_value(m, p):
    x = [F(p[0]), F(p[1]), F(1)]
    return sum(x[i] * m[i][j] * x[j] for i in range(3) for j in range(3))


def inside_2d(tree2, p):
    """Exact membership of a point of the layer."""
    if tree2[0] == "leaf":
        return conic_value(tree2[1], p) <= 0
    return combine(tree2[0], inside_2d(tree2[1], p), inside_2d(tree2[2], p))


def classify(m):
    """Line L5. Return (kind, center, fc, det) for a conic matrix.

    det is the determinant of the 2 x 2 block, center solves the 2 x 2 system
    when det != 0, and fc is the value of the conic at the center. Kinds:
    "ellipse", "point", "empty" (positive definite block), "hyperbola",
    "line pair", "parabolic" (det = 0), "complement" (negative definite block:
    the region f <= 0 lies outside an ellipse, or is the whole plane).
    """
    a, b, c = m[0][0], m[0][1], m[1][1]
    d, e, f = m[0][2], m[1][2], m[2][2]
    det = a * c - b * b
    if det == 0:  # @line L9
        return ("parabolic", None, None, det)
    cx = (b * e - c * d) / det
    cy = (b * d - a * e) / det
    fc = f + d * cx + e * cy  # @line L10
    if det > 0 and a > 0:  # @line L11
        kind = "ellipse" if fc < 0 else ("point" if fc == 0 else "empty")
    elif det > 0:  # @line L12
        kind = "complement"
    else:
        kind = "line pair" if fc == 0 else "hyperbola"
    return (kind, (cx, cy), fc, det)


def ellipse_axes(m):
    """Squared semi-axes and unit axis directions of an ellipse (floats).

    The squared semi-axes are -fc / lambda_i, where lambda_i are the
    eigenvalues of the 2 x 2 block.
    """
    kind, center, fc, det = classify(m)
    if kind != "ellipse":
        raise ValueError("not an ellipse: " + kind)
    a, b, c = float(m[0][0]), float(m[0][1]), float(m[1][1])
    mean = (a + c) / 2
    rad = math.hypot((a - c) / 2, b)
    lam1, lam2 = mean - rad, mean + rad  # lam1 <= lam2, both > 0
    if b == 0 and a <= c:
        v1 = (1.0, 0.0)
    elif b == 0:
        v1 = (0.0, 1.0)
    else:
        v1 = (lam1 - c, b)
        n = math.hypot(*v1)
        v1 = (v1[0] / n, v1[1] / n)
    v2 = (-v1[1], v1[0])
    s1, s2 = -float(fc) / lam1, -float(fc) / lam2  # s1 >= s2
    return (float(center[0]), float(center[1])), s1, s2, v1, v2


def vertex_count(a, tol):
    """The least n >= 3 with a (1 - cos(pi / n)) <= tol."""
    if tol >= a:
        return 3
    n = math.ceil(math.pi / math.acos(1 - tol / a))
    n = max(3, n)
    while a * (1 - math.cos(math.pi / n)) > tol:  # guard against rounding
        n += 1
    return n


def ellipse_polyline(m, tol):
    """Line L6. A closed polygon with vertices on the ellipse and
    Hausdorff distance at most tol from it."""
    (cx, cy), s1, s2, v1, v2 = ellipse_axes(m)
    a1, a2 = math.sqrt(s1), math.sqrt(s2)
    n = vertex_count(a1, tol)  # @line L13
    pts = []
    for k in range(n):  # @line L14
        t = 2 * math.pi * k / n
        u, w = a1 * math.cos(t), a2 * math.sin(t)
        pts.append((cx + u * v1[0] + w * v2[0], cy + u * v1[1] + w * v2[1]))
    return pts


# ------------------------------------------------- boundary classification

IN, ON, OUT = -1, 0, 1


def _combine3(op, a, b):
    if op == "union":
        if IN in (a, b):
            return IN
        return OUT if a == b == OUT else ON
    if op == "inter":
        if OUT in (a, b):
            return OUT
        return IN if a == b == IN else ON
    if op == "diff":
        return _combine3("inter", a, -b)
    raise ValueError(op)


def classify_point(tree2, p, leaf, eps):
    """Three-valued membership, with the given leaf forced to ON.

    Other leaves are ON when |f| <= eps, so a point on two conics at once is
    ON. Two ON values in a union give ON, which is right for contours that
    cross but not for two solids that touch along a curve.
    """
    if tree2[0] == "leaf":
        if tree2 is leaf:
            return ON
        v = conic_value_float(tree2[1], p)
        return ON if abs(v) <= eps else (IN if v < 0 else OUT)
    return _combine3(tree2[0], classify_point(tree2[1], p, leaf, eps), classify_point(tree2[2], p, leaf, eps))


def conic_value_float(m, p):
    x = (p[0], p[1], 1.0)
    return sum(x[i] * float(m[i][j]) * x[j] for i in range(3) for j in range(3))


def leaves(tree2):
    if tree2[0] == "leaf":
        return [tree2]
    return leaves(tree2[1]) + leaves(tree2[2])


def direct_slice(tree, z, tol, eps=1e-12):
    """DIRECT-SLICE. Return the exact conic tree of the layer and the
    contour pieces as lists of points (open runs, or closed loops with the
    first point repeated at the end)."""
    tree2 = slice_tree(tree, z)  # @line L2
    contours = []  # @line L3
    for leaf in leaves(tree2):  # @line L4
        kind = classify(leaf[1])[0]  # @line L5
        if kind != "ellipse":
            continue  # points, empty sets and unbounded conics give no loop here
        poly = ellipse_polyline(leaf[1], tol)  # @line L6
        keep = [classify_point(tree2, p, leaf, eps) == ON for p in poly]  # @line L7
        if all(keep):
            contours.append(poly + [poly[0]])
            continue
        n = len(poly)
        start = keep.index(False)
        run = []
        for k in range(1, n + 1):
            i = (start + k) % n
            if keep[i]:
                run.append(poly[i])
            elif run:
                contours.append(run)
                run = []
        if run:
            contours.append(run)
    return tree2, contours  # @line L8


# --------------------------------------------- mesh slice, for comparison


def uv_sphere_section_radii(r, rings, segments, z):
    """Slice a UV-sphere mesh of radius r at height z (|z| < r, z not at a
    ring). Return (min, max) distance from the axis to the polygon of the
    section. The true section is a circle of radius sqrt(r^2 - z^2)."""
    lats = [math.pi * k / rings - math.pi / 2 for k in range(rings + 1)]
    zs = [r * math.sin(t) for t in lats]
    k = max(i for i in range(rings) if zs[i] < z)
    r0, r1 = r * math.cos(lats[k]), r * math.cos(lats[k + 1])
    t = (z - zs[k]) / (zs[k + 1] - zs[k])
    rho = r0 + t * (r1 - r0)  # the section is a regular polygon with this circumradius
    return rho * math.cos(math.pi / segments), rho
