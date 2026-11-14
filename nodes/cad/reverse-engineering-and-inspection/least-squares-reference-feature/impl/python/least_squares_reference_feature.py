# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-reference-feature/. The authors are listed in prov/5ETC50.jsonl.

"""Least-squares (Gaussian) reference features: line, plane and circle.

Each fit minimizes the sum of the squared orthogonal deviations of the points
from the ideal feature. The deviations from the fitted feature give the
least-squares zone, whose width max(e) - min(e) is an upper bound of the
minimum zone form error.
"""

import math


def _centroid(points):
    n = len(points)
    d = len(points[0])
    return tuple(sum(p[k] for p in points) / n for k in range(d))


def _covariance(points, c):
    d = len(c)
    m = [[0.0] * d for _ in range(d)]
    for p in points:
        q = [p[k] - c[k] for k in range(d)]
        for i in range(d):
            for j in range(d):
                m[i][j] += q[i] * q[j]
    return m


def jacobi_eigen(a, sweeps=60):
    """Eigenvalues and unit eigenvectors (columns) of a small symmetric matrix."""
    n = len(a)
    a = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        scale = sum(a[i][i] ** 2 for i in range(n)) + 1e-300
        if off <= 1e-30 * scale:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - s * vkq
                    v[k][q] = s * vkp + c * vkq
    vals = [a[i][i] for i in range(n)]
    vecs = [tuple(v[k][i] for k in range(n)) for i in range(n)]
    order = sorted(range(n), key=lambda i: vals[i])
    return [vals[i] for i in order], [vecs[i] for i in order]


def zone_width(deviations):
    """Width of the zone between the extreme deviations."""
    return max(deviations) - min(deviations)


def ls_plane(points):
    """Least-squares plane of 3D points.

    Returns (centroid, unit normal, deviations, sum of squares). The normal is
    the eigenvector of the smallest eigenvalue of the scatter matrix, and the
    sum of squares equals that eigenvalue.
    """
    c = _centroid(points)
    vals, vecs = jacobi_eigen(_covariance(points, c))
    n = vecs[0]
    dev = [sum(n[k] * (p[k] - c[k]) for k in range(3)) for p in points]
    return c, n, dev, sum(e * e for e in dev)


def ls_line(points):
    """Least-squares line of 2D or 3D points.

    Returns (centroid, unit direction, distances). The direction is the
    eigenvector of the largest eigenvalue of the scatter matrix. In 2D the
    deviations are signed; in 3D they are distances to the line.
    """
    c = _centroid(points)
    d = len(c)
    vals, vecs = jacobi_eigen(_covariance(points, c))
    u = vecs[-1]
    if d == 2:
        nrm = (-u[1], u[0])
        dev = [nrm[0] * (p[0] - c[0]) + nrm[1] * (p[1] - c[1]) for p in points]
        return c, u, dev
    dev = []
    for p in points:
        q = [p[k] - c[k] for k in range(d)]
        h = sum(q[k] * u[k] for k in range(d))
        dev.append(math.sqrt(sum((q[k] - h * u[k]) ** 2 for k in range(d))))
    return c, u, dev


def _solve3(m, b):
    m = [row[:] + [b[i]] for i, row in enumerate(m)]
    for col in range(3):
        piv = max(range(col, 3), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-300:
            raise ValueError("singular system")
        m[col], m[piv] = m[piv], m[col]
        for r in range(3):
            if r != col:
                f = m[r][col] / m[col][col]
                for k in range(col, 4):
                    m[r][k] -= f * m[col][k]
    return [m[i][3] / m[i][i] for i in range(3)]


def kasa_start(points):
    """Linear algebraic circle used as the start: x^2 + y^2 + D x + E y + G = 0."""
    ata = [[0.0] * 3 for _ in range(3)]
    atb = [0.0] * 3
    for x, y in points:
        row = (x, y, 1.0)
        rhs = -(x * x + y * y)
        for i in range(3):
            atb[i] += row[i] * rhs
            for j in range(3):
                ata[i][j] += row[i] * row[j]
    d, e, g = _solve3(ata, atb)
    a, b = -d / 2.0, -e / 2.0
    return (a, b), math.sqrt(max(0.0, a * a + b * b - g))


def _circle_cost(points, a, b, r):
    return sum((math.hypot(x - a, y - b) - r) ** 2 for x, y in points)


def ls_circle(points, max_iter=200, tol=1e-15):
    """Least-squares (geometric) circle of 2D points.

    Starts from the Kasa circle and takes Levenberg-Marquardt steps on the
    orthogonal residuals |x_i - c| - r. Returns (center, radius, deviations,
    sum of squares). The cost never increases from one accepted step to the
    next.
    """
    (a, b), r = kasa_start(points)
    cost = _circle_cost(points, a, b, r)
    mu = 1e-3
    for _ in range(max_iter):
        jtj = [[0.0] * 3 for _ in range(3)]
        jtr = [0.0] * 3
        for x, y in points:
            dist = math.hypot(x - a, y - b)
            if dist == 0.0:
                continue
            row = (-(x - a) / dist, -(y - b) / dist, -1.0)
            res = dist - r
            for i in range(3):
                jtr[i] += row[i] * res
                for j in range(3):
                    jtj[i][j] += row[i] * row[j]
        improved = False
        for _ in range(30):
            m = [[jtj[i][j] + (mu * (1.0 + jtj[i][i]) if i == j else 0.0) for j in range(3)] for i in range(3)]
            step = _solve3(m, [-v for v in jtr])
            na, nb, nr = a + step[0], b + step[1], r + step[2]
            ncost = _circle_cost(points, na, nb, nr)
            if ncost < cost:
                gain = cost - ncost
                a, b, r, cost = na, nb, nr, ncost
                mu = max(mu / 10.0, 1e-12)
                improved = True
                break
            mu *= 10.0
        if not improved or gain <= tol * max(cost, 1e-300):
            break
    dev = [math.hypot(x - a, y - b) - r for x, y in points]
    return (a, b), r, dev, cost


if __name__ == "__main__":
    pts = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 1)]
    c, u, dev = ls_line(pts)
    print("line", c, u, zone_width(dev))
    arc = [(math.cos(t), math.sin(t)) for t in (0.0, 0.2, 0.4, 0.6)]
    print("circle", ls_circle(arc)[:2])
