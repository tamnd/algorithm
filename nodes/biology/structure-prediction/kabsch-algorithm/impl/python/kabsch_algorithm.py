# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kabsch-algorithm/. The authors are listed in prov/P934Z2.jsonl.

"""Kabsch algorithm: the rotation R and translation t that minimize
sum |R x_i + t - y_i|^2 over proper rotations (det R = +1).

The singular vectors of the 3 x 3 covariance H = sum a_i b_i^T come from a
Jacobi eigen decomposition of H^T H, as in Kabsch (1976). The reflection fix of
Kabsch (1978) is built in: V and U are both made proper, so R = V U^T is a
rotation and equals V diag(1, 1, d) U_svd^T with d = sign(det(V U_svd^T)).
Standard library only. Cost: O(N) time for N point pairs, O(1) extra space.
"""

import math

Vec = tuple[float, float, float]
Mat = list[list[float]]


def jacobi_eigen_sym3(a: Mat, sweeps: int = 60) -> tuple[list[float], Mat]:
    """Eigenvalues (descending) and eigenvectors (as columns) of a symmetric 3 x 3 matrix."""
    a = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    for _ in range(sweeps):
        off = a[0][1] ** 2 + a[0][2] ** 2 + a[1][2] ** 2
        scale = sum(a[i][j] ** 2 for i in range(3) for j in range(3))
        if off <= 1e-32 * scale or off == 0.0:
            break
        for p, q in ((0, 1), (0, 2), (1, 2)):
            if a[p][q] == 0.0:
                continue
            theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
            t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
            c = 1.0 / math.sqrt(t * t + 1.0)
            s = t * c
            for k in range(3):  # A <- A J
                akp, akq = a[k][p], a[k][q]
                a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
            for k in range(3):  # A <- J^T A
                apk, aqk = a[p][k], a[q][k]
                a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
            for k in range(3):  # V <- V J
                vkp, vkq = v[k][p], v[k][q]
                v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    order = sorted(range(3), key=lambda i: -a[i][i])
    vals = [a[i][i] for i in order]
    vecs = [[v[r][i] for i in order] for r in range(3)]
    return vals, vecs


def _col(m: Mat, k: int) -> Vec:
    return (m[0][k], m[1][k], m[2][k])


def _matvec(m: Mat, x: Vec) -> Vec:
    return (m[0][0] * x[0] + m[0][1] * x[1] + m[0][2] * x[2],
            m[1][0] * x[0] + m[1][1] * x[1] + m[1][2] * x[2],
            m[2][0] * x[0] + m[2][1] * x[1] + m[2][2] * x[2])


def _cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _unit(a: Vec) -> Vec:
    n = math.sqrt(_dot(a, a))
    return (a[0] / n, a[1] / n, a[2] / n)


def _perpendicular(a: Vec) -> Vec:
    """A unit vector orthogonal to the unit vector a."""
    k = min(range(3), key=lambda i: abs(a[i]))
    e = tuple(1.0 if i == k else 0.0 for i in range(3))
    return _unit(_cross(a, e))


def det3(m: Mat) -> float:
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def kabsch_algorithm(xs: list[Vec], ys: list[Vec]) -> tuple[Mat, Vec, float]:
    """Return (R, t, rmsd) with R a proper rotation that minimizes the RMSD
    between R x_i + t and y_i. Precondition: len(xs) == len(ys) >= 1.
    When the points lie on a line or coincide, R is one of several optimal rotations."""
    n = len(xs)
    if n == 0 or n != len(ys):
        raise ValueError("need two non-empty lists of the same length")
    xbar = tuple(sum(p[k] for p in xs) / n for k in range(3))  # @line L1
    ybar = tuple(sum(p[k] for p in ys) / n for k in range(3))
    a = [(p[0] - xbar[0], p[1] - xbar[1], p[2] - xbar[2]) for p in xs]  # @line L2
    b = [(p[0] - ybar[0], p[1] - ybar[1], p[2] - ybar[2]) for p in ys]
    h = [[sum(ai[r] * bi[c] for ai, bi in zip(a, b)) for c in range(3)] for r in range(3)]  # @line L3
    hth = [[sum(h[k][r] * h[k][c] for k in range(3)) for c in range(3)] for r in range(3)]
    mu, v = jacobi_eigen_sym3(hth)  # @line L4
    if det3(v) < 0:  # @line L5
        for r in range(3):
            v[r][2] = -v[r][2]
    s = [math.sqrt(max(m, 0.0)) for m in mu]
    tiny = 1e-12 * max(s[0], 1e-300)
    if s[0] <= 1e-300:  # all points at the centroid: any rotation is optimal
        u1, u2 = (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)
        v = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    else:
        u1 = _unit(_matvec(h, _col(v, 0)))  # @line L6
        w = _matvec(h, _col(v, 1))
        w = tuple(w[k] - _dot(w, u1) * u1[k] for k in range(3))  # re-orthogonalize
        if s[1] > tiny and math.sqrt(_dot(w, w)) > 1e-9 * s[0]:
            u2 = _unit(w)
        else:  # points on a line: u2 is free
            u2 = _perpendicular(u1)
    u3 = _cross(u1, u2)  # @line L7
    us = (u1, u2, u3)
    rot = [[sum(v[r][k] * us[k][c] for k in range(3)) for c in range(3)] for r in range(3)]  # @line L8
    rx = _matvec(rot, xbar)
    t = (ybar[0] - rx[0], ybar[1] - rx[1], ybar[2] - rx[2])  # @line L9
    ga = sum(_dot(p, p) for p in a)
    gb = sum(_dot(p, p) for p in b)
    trace_rh = sum(rot[r][c] * h[c][r] for r in range(3) for c in range(3))
    e = ga + gb - 2.0 * trace_rh  # @line L10
    return rot, t, math.sqrt(max(e, 0.0) / n)  # @line L11


def apply(rot: Mat, t: Vec, p: Vec) -> Vec:
    q = _matvec(rot, p)
    return (q[0] + t[0], q[1] + t[1], q[2] + t[2])


def rmsd_after(rot: Mat, t: Vec, xs: list[Vec], ys: list[Vec]) -> float:
    """RMSD between R x_i + t and y_i, computed directly from the coordinates."""
    tot = 0.0
    for x, y in zip(xs, ys):
        q = apply(rot, t, x)
        tot += (q[0] - y[0]) ** 2 + (q[1] - y[1]) ** 2 + (q[2] - y[2]) ** 2
    return math.sqrt(tot / len(xs))
