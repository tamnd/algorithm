# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quaternion-superposition/. The authors are listed in prov/AMR9P8.jsonl.

"""Quaternion superposition (Horn 1987): the optimal rotation is the unit
quaternion q that maximizes q^T N q, so it is the eigenvector of the largest
eigenvalue of a symmetric 4 x 4 matrix N built from the covariance S.
The least RMSD is sqrt((G_A + G_B - 2 lambda_max) / N).

Also qcp_rmsd, the QCP method of Theobald (2005): Newton's method on the
characteristic polynomial of N gives lambda_max without the eigenvector.
Standard library only. Cost: O(N) time for N point pairs, O(1) extra space.
"""

import math

Vec = tuple[float, float, float]
Mat = list[list[float]]


def jacobi_eigen_sym(a: Mat, sweeps: int = 60) -> tuple[list[float], Mat]:
    """Eigenvalues (descending) and eigenvectors (columns) of a small symmetric matrix."""
    n = len(a)
    a = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
        scale = sum(a[i][j] ** 2 for i in range(n) for j in range(n))
        if off == 0.0 or off <= 1e-32 * scale:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    order = sorted(range(n), key=lambda i: -a[i][i])
    return [a[i][i] for i in order], [[v[r][i] for i in order] for r in range(n)]


def _center(pts: list[Vec]) -> tuple[Vec, list[Vec]]:
    n = len(pts)
    c = (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n, sum(p[2] for p in pts) / n)
    return c, [(p[0] - c[0], p[1] - c[1], p[2] - c[2]) for p in pts]


def covariance(a: list[Vec], b: list[Vec]) -> Mat:
    """S[r][c] = sum_i a_i[r] * b_i[c]."""
    return [[sum(ai[r] * bi[c] for ai, bi in zip(a, b)) for c in range(3)] for r in range(3)]


def horn_matrix(s: Mat) -> Mat:
    """The symmetric 4 x 4 matrix N with q^T N q = trace(R(q) S) for each unit quaternion q."""
    (sxx, sxy, sxz), (syx, syy, syz), (szx, szy, szz) = s
    return [[sxx + syy + szz, syz - szy, szx - sxz, sxy - syx],
            [syz - szy, sxx - syy - szz, sxy + syx, szx + sxz],
            [szx - sxz, sxy + syx, -sxx + syy - szz, syz + szy],
            [sxy - syx, szx + sxz, syz + szy, -sxx - syy + szz]]


def rotation_from_quaternion(q: list[float]) -> Mat:
    w, x, y, z = q
    return [[w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z]]


def quaternion_superposition(xs: list[Vec], ys: list[Vec]) -> tuple[Mat, Vec, float, list[float]]:
    """Return (R, t, rmsd, q): R x_i + t is the least-RMSD fit of x_i onto y_i,
    and q = (w, x, y, z) is the unit quaternion of R. Precondition: len(xs) == len(ys) >= 1."""
    n = len(xs)
    if n == 0 or n != len(ys):
        raise ValueError("need two non-empty lists of the same length")
    xbar, a = _center(xs)  # @line L1
    ybar, b = _center(ys)
    ga = sum(p[0] ** 2 + p[1] ** 2 + p[2] ** 2 for p in a)
    gb = sum(p[0] ** 2 + p[1] ** 2 + p[2] ** 2 for p in b)
    s = covariance(a, b)  # @line L2
    nmat = horn_matrix(s)  # @line L3
    vals, vecs = jacobi_eigen_sym(nmat)  # @line L4
    lam = vals[0]
    q = [vecs[r][0] for r in range(4)]
    norm = math.sqrt(sum(c * c for c in q))
    q = [c / norm for c in q]
    if q[0] < 0:  # q and -q give the same rotation; keep w >= 0
        q = [-c for c in q]
    rot = rotation_from_quaternion(q)  # @line L5
    t = tuple(ybar[r] - sum(rot[r][c] * xbar[c] for c in range(3)) for r in range(3))  # @line L6
    rmsd = math.sqrt(max(ga + gb - 2.0 * lam, 0.0) / n)  # @line L7
    return rot, t, rmsd, q


def _det3(m: Mat) -> float:
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def _det4(m: Mat) -> float:
    tot = 0.0
    for j in range(4):
        minor = [[m[r][c] for c in range(4) if c != j] for r in range(1, 4)]
        tot += (-1) ** j * m[0][j] * _det3(minor)
    return tot


def qcp_rmsd(xs: list[Vec], ys: list[Vec], tol: float = 1e-11) -> float:
    """Least RMSD by the QCP method: Newton's method on P(l) = l^4 + c2 l^2 + c1 l + c0,
    the characteristic polynomial of N, started at (G_A + G_B) / 2."""
    n = len(xs)
    _, a = _center(xs)
    _, b = _center(ys)
    ga = sum(p[0] ** 2 + p[1] ** 2 + p[2] ** 2 for p in a)
    gb = sum(p[0] ** 2 + p[1] ** 2 + p[2] ** 2 for p in b)
    s = covariance(a, b)
    c2 = -2.0 * sum(s[r][c] ** 2 for r in range(3) for c in range(3))
    c1 = -8.0 * _det3(s)
    c0 = _det4(horn_matrix(s))
    lam = (ga + gb) / 2.0
    for _ in range(100):
        p = ((lam * lam + c2) * lam + c1) * lam + c0
        dp = (4.0 * lam * lam + 2.0 * c2) * lam + c1
        if dp == 0.0:
            break
        step = p / dp
        lam -= step
        if abs(step) <= tol * max(abs(lam), 1.0):
            break
    return math.sqrt(max(ga + gb - 2.0 * lam, 0.0) / n)
