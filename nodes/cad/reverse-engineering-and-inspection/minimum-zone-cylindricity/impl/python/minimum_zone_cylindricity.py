# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-zone-cylindricity/. The authors are listed in prov/HBSSZY.jsonl.

"""Minimum zone cylindricity by sequential linear programming.

The cylindricity of measured points is the least difference R_out - R_in of
two coaxial cylinders that hold the points between them. For a fixed axis the
width is the range of the distances to the axis, so the problem is a
minimization over the four parameters of a line. It is not convex.

The method linearizes the distances about the current axis, solves the linear
program "minimize R_out - R_in" inside a box of trust (a small dense simplex
method below), and accepts the new axis only if the exact width goes down. So
the widths decrease monotonically to a local minimum. There is no guarantee of
reaching the global minimum.
"""

import math


# ---------------------------------------------------------------- vectors

def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _scale(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _unit(a):
    n = math.sqrt(_dot(a, a))
    return (a[0] / n, a[1] / n, a[2] / n)


def _frame(u):
    """Two unit vectors that make (e1, e2, u) orthonormal."""
    t = (1.0, 0.0, 0.0) if abs(u[0]) < 0.9 else (0.0, 1.0, 0.0)
    e1 = _unit(_cross(u, t))
    return e1, _cross(u, e1)


# ---------------------------------------------------------------- widths

def radial_distances(points, p, u):
    """Distances from the points to the line through p with unit direction u."""
    out = []
    for q in points:
        w = _sub(q, p)
        h = _dot(w, u)
        out.append(math.sqrt(_dot(_sub(w, _scale(u, h)), _sub(w, _scale(u, h)))))
    return out


def cylinder_width(points, p, u):
    """Width R_out - R_in of the thinnest coaxial zone with the given axis."""
    d = radial_distances(points, p, u)
    return max(d) - min(d)


# ---------------------------------------------------------------- simplex

def simplex_max(c, a, b, eps=1e-11, max_pivots=100000):
    """Maximize c.x subject to a x <= b, x >= 0, with b >= 0.

    Dense tableau simplex with Bland's rule, which never cycles. The origin is
    feasible because b >= 0, so no first phase is needed.
    """
    n, m = len(c), len(a)
    tab = [list(a[i]) + [1.0 if k == i else 0.0 for k in range(m)] + [float(b[i])] for i in range(m)]
    z = [-float(v) for v in c] + [0.0] * (m + 1)
    basis = [n + i for i in range(m)]
    for _ in range(max_pivots):
        col = next((j for j in range(n + m) if z[j] < -eps), None)
        if col is None:
            break
        row, best = None, None
        for i in range(m):
            if tab[i][col] > eps:
                ratio = tab[i][-1] / tab[i][col]
                if best is None or ratio < best - eps or (abs(ratio - best) <= eps and basis[i] < basis[row]):
                    row, best = i, ratio
        if row is None:
            raise ValueError("unbounded linear program")
        pr = tab[row]
        piv = pr[col]
        pr = [v / piv for v in pr]
        tab[row] = pr
        for i in range(m):
            if i != row:
                f = tab[i][col]
                if f != 0.0:
                    ti = tab[i]
                    tab[i] = [ti[k] - f * pr[k] for k in range(n + m + 1)]
        f = z[col]
        z = [z[k] - f * pr[k] for k in range(n + m + 1)]
        basis[row] = col
    x = [0.0] * n
    for i, j in enumerate(basis):
        if j < n:
            x[j] = tab[i][-1]
    return x


def linearized_step(points, p, u, box_shift, box_tilt):
    """Solve the linear program of one step about the axis (p, u).

    In the frame (e1, e2, u) at p, a point has coordinates (x, y, z) and
    radius rho. Moving the axis to pass through (dx, dy, 0) with direction
    (ta, tb, 1) changes its radius to first order to
        rho - (x dx + y dy) / rho - z (x ta + y tb) / rho.
    The program minimizes R_out - R_in over |dx|, |dy| <= box_shift and
    |ta|, |tb| <= box_tilt. Returns (dx, dy, ta, tb).
    """
    e1, e2 = _frame(u)
    rho, grad = [], []
    for q in points:
        w = _sub(q, p)
        x, y, zz = _dot(w, e1), _dot(w, e2), _dot(w, u)
        r = math.hypot(x, y)
        rho.append(r)
        if r == 0.0:
            grad.append((0.0, 0.0, 0.0, 0.0))
        else:
            grad.append((-x / r, -y / r, -zz * x / r, -zz * y / r))
    box = (box_shift, box_shift, box_tilt, box_tilt)
    # Variables v_k = delta_k + box_k in [0, 2 box_k], then P, Q >= 0 with
    # R_out = U - P and R_in = L + Q, so the origin is feasible.
    spread = [sum(abs(g[k]) * box[k] for k in range(4)) for g in grad]
    upper = max(r + s for r, s in zip(rho, spread))
    lower = min(r - s for r, s in zip(rho, spread))
    rows, rhs = [], []
    for r, g in zip(rho, grad):
        shift = sum(g[k] * box[k] for k in range(4))
        rows.append([g[0], g[1], g[2], g[3], 1.0, 0.0])
        rhs.append(max(0.0, upper - r + shift))
        rows.append([-g[0], -g[1], -g[2], -g[3], 0.0, 1.0])
        rhs.append(max(0.0, r - shift - lower))
    for k in range(4):
        row = [0.0] * 6
        row[k] = 1.0
        rows.append(row)
        rhs.append(2.0 * box[k])
    sol = simplex_max([0.0, 0.0, 0.0, 0.0, 1.0, 1.0], rows, rhs)
    return tuple(sol[k] - box[k] for k in range(4)), (e1, e2)


# ---------------------------------------------------------------- start

def _jacobi3(a):
    a = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    for _ in range(50):
        off = a[0][1] ** 2 + a[0][2] ** 2 + a[1][2] ** 2
        if off < 1e-30 * (a[0][0] ** 2 + a[1][1] ** 2 + a[2][2] ** 2 + 1e-300):
            break
        for p, q in ((0, 1), (0, 2), (1, 2)):
            if a[p][q] == 0.0:
                continue
            th = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
            t = math.copysign(1.0, th) / (abs(th) + math.sqrt(th * th + 1.0))
            c = 1.0 / math.sqrt(t * t + 1.0)
            s = t * c
            for k in range(3):
                akp, akq = a[k][p], a[k][q]
                a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
            for k in range(3):
                apk, aqk = a[p][k], a[q][k]
                a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
            for k in range(3):
                vkp, vkq = v[k][p], v[k][q]
                v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [tuple(v[k][i] for k in range(3)) for i in range(3)]


def _circle_center(pts2):
    """Center of the linear algebraic circle fit of planar points."""
    s = [[0.0] * 3 for _ in range(3)]
    t = [0.0] * 3
    for x, y in pts2:
        row = (x, y, 1.0)
        for i in range(3):
            t[i] -= row[i] * (x * x + y * y)
            for j in range(3):
                s[i][j] += row[i] * row[j]
    m = [s[i] + [t[i]] for i in range(3)]
    for col in range(3):
        piv = max(range(col, 3), key=lambda r: abs(m[r][col]))
        m[col], m[piv] = m[piv], m[col]
        if abs(m[col][col]) < 1e-300:
            return 0.0, 0.0
        for r in range(3):
            if r != col:
                f = m[r][col] / m[col][col]
                for k in range(col, 4):
                    m[r][k] -= f * m[col][k]
    d, e = m[0][3] / m[0][0], m[1][3] / m[1][1]
    return -d / 2.0, -e / 2.0


def default_start(points):
    """Try the three principal directions as axes, each with the center of a
    circle fit of the projected points, and keep the thinnest zone."""
    n = len(points)
    c = tuple(sum(q[k] for q in points) / n for k in range(3))
    cov = [[sum((q[i] - c[i]) * (q[j] - c[j]) for q in points) for j in range(3)] for i in range(3)]
    best = None
    for u in _jacobi3(cov):
        e1, e2 = _frame(u)
        pts2 = [(_dot(_sub(q, c), e1), _dot(_sub(q, c), e2)) for q in points]
        cx, cy = _circle_center(pts2)
        p = _add(c, _add(_scale(e1, cx), _scale(e2, cy)))
        w = cylinder_width(points, p, u)
        if best is None or w < best[0]:
            best = (w, p, u)
    return best[1], best[2]


# ---------------------------------------------------------------- method

def minimum_zone_cylindricity(points, start=None, max_iter=300, tol=1e-12):
    """Local minimum zone cylinder of 3D points.

    Returns a dict with the axis point p, the unit direction u, the radii
    r_in and r_out, the width r_out - r_in, and the history of accepted
    widths, which is strictly decreasing.
    """
    points = [tuple(float(v) for v in q) for q in points]
    p, u = start if start is not None else default_start(points)  # @line L1
    u = _unit(u)
    n = len(points)
    cen = tuple(sum(q[k] for q in points) / n for k in range(3))
    p = _add(p, _scale(u, _dot(_sub(cen, p), u)))
    width = cylinder_width(points, p, u)
    history = [width]
    zmax = max(abs(_dot(_sub(q, p), u)) for q in points) or 1.0
    scale = max(math.sqrt(_dot(_sub(q, cen), _sub(q, cen))) for q in points) or 1.0
    trust = max(width, 1e-6 * scale)
    for _ in range(max_iter):  # @line L2
        if trust < tol * scale:
            break
        (dx, dy, ta, tb), (e1, e2) = linearized_step(points, p, u, trust, trust / zmax)  # @line L3
        newp = _add(p, _add(_scale(e1, dx), _scale(e2, dy)))  # @line L4
        newu = _unit(_add(u, _add(_scale(e1, ta), _scale(e2, tb))))
        newp = _add(newp, _scale(newu, _dot(_sub(cen, newp), newu)))
        neww = cylinder_width(points, newp, newu)  # @line L5
        if neww < width - 1e-15 * scale:  # @line L6
            p, u, width = newp, newu, neww
            history.append(width)
            trust *= 2.0
        else:
            trust *= 0.25  # @line L7
    d = radial_distances(points, p, u)
    return {"p": p, "u": u, "r_in": min(d), "r_out": max(d), "width": width, "history": history}  # @line L8


if __name__ == "__main__":
    import random

    rng = random.Random(1)
    pts = []
    for i in range(40):
        t = 2 * math.pi * i / 40
        r = 5 + 0.01 * math.cos(3 * t) + rng.uniform(-0.002, 0.002)
        pts.append((r * math.cos(t), r * math.sin(t), rng.uniform(0, 10)))
    res = minimum_zone_cylindricity(pts)
    print(res["width"], res["u"], len(res["history"]))
