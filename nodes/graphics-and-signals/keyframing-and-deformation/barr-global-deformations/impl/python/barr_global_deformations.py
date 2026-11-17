# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barr-global-deformations/. The authors are listed in prov/702PFN.jsonl.
"""Global deformations of Barr (1984): taper, twist and bend.

Each operation is a map F from R^3 to R^3 with a closed-form Jacobian J.
Points move by F. Normal vectors move by the cofactor matrix of J,
n' = cof(J) n = det(J) J^-T n, and are then normalized. A chain of
operations is applied left to right; the Jacobians multiply as
J <- J_op(p) J, with J_op taken at the current point p.

Each operation below is a function op(p) that returns (F(p), J(p)).
"""

import math


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def mat_vec(a, v):
    return tuple(sum(a[i][k] * v[k] for k in range(3)) for i in range(3))


def identity():
    return [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]


def det3(a):
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def cofactor(a):
    """Return the cofactor matrix of a, which equals det(a) a^-T when a is invertible."""
    c = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            r = [x for x in range(3) if x != i]
            s = [x for x in range(3) if x != j]
            minor = a[r[0]][s[0]] * a[r[1]][s[1]] - a[r[0]][s[1]] * a[r[1]][s[0]]
            c[i][j] = minor if (i + j) % 2 == 0 else -minor
    return c


def taper(r, dr):
    """Taper along z: (x, y, z) -> (r(z) x, r(z) y, z). dr is the derivative r'."""

    def op(p):
        x, y, z = p
        f, fp = r(z), dr(z)
        return (f * x, f * y, z), [[f, 0.0, fp * x], [0.0, f, fp * y], [0.0, 0.0, 1.0]]

    return op


def twist(theta, dtheta):
    """Twist about z: rotate the xy plane by the angle theta(z)."""

    def op(p):
        x, y, z = p
        t, tp = theta(z), dtheta(z)
        c, s = math.cos(t), math.sin(t)
        out = (x * c - y * s, x * s + y * c, z)
        jac = [[c, -s, (-x * s - y * c) * tp], [s, c, (x * c - y * s) * tp], [0.0, 0.0, 1.0]]
        return out, jac

    return op


def bend(k, y0, ymin, ymax):
    """Bend along y in the yz plane with rate k, center y0 and region [ymin, ymax].

    Inside the region, the line z = 0 maps onto a circle of radius 1 / k.
    Outside it, the object continues along the tangent at the region end.
    """
    if k == 0:
        raise ValueError("use the identity for k = 0")
    if not ymin <= y0 <= ymax:
        raise ValueError("the center must lie in the bend region")

    def op(p):
        x, y, z = p
        yh = min(max(y, ymin), ymax)
        th = k * (yh - y0)
        c, s = math.cos(th), math.sin(th)
        yy = -s * (z - 1.0 / k) + y0
        zz = c * (z - 1.0 / k) + 1.0 / k
        if ymin <= y <= ymax:
            jac = [[1.0, 0.0, 0.0], [0.0, c * (1 - k * z), -s], [0.0, s * (1 - k * z), c]]
            return (x, yy, zz), jac
        d = y - yh
        jac = [[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]]
        return (x, yy + c * d, zz + s * d), jac

    return op


def deform(p, n, ops):
    """Apply the chain ops to the point p and the normal n. Return (p', n')."""
    jac = identity()  # @line L1
    p = tuple(p)
    for op in ops:  # @line L2
        q, j_op = op(p)
        jac = mat_mul(j_op, jac)  # @line L3
        p = q  # @line L4
    m = mat_vec(cofactor(jac), n)  # @line L5
    length = math.sqrt(sum(v * v for v in m))
    if length == 0:
        raise ValueError("the deformation is singular at this point")
    return p, tuple(v / length for v in m)  # @line L6


def deform_point(p, ops):
    """Apply the chain ops to a point only."""
    for op in ops:
        p, _ = op(p)
    return p


def jacobian(p, ops):
    """Return the Jacobian of the whole chain at p."""
    jac = identity()
    for op in ops:
        p, j_op = op(p)
        jac = mat_mul(j_op, jac)
    return jac
