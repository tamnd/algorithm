# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/angle-based-flattening/. The authors are listed in prov/1YT62Y.jsonl.

"""Angle-based flattening (Sheffer and de Sturler 2001).

The unknowns are the planar angles alpha of all triangle corners. The
objective is F(alpha) = sum (alpha - beta)^2 / beta^2, where beta are the 3D
angles, scaled at each inner vertex so that they add up to 2 pi. The
constraints are

    triangle:  the three angles of each triangle add up to pi,
    vertex:    the angles at each inner vertex add up to 2 pi,
    wheel:     at each inner vertex, sum log sin(next) - sum log sin(prev) = 0,

where next and prev are the corners after and before the vertex in each
triangle around it. The wheel condition makes the edge lengths given by the
law of sines agree around the vertex. The solver is a Lagrange-Newton
(sequential quadratic programming) iteration in which the Hessian is the
Hessian diag(2 / beta^2) of the objective only. The layout places the
triangles one by one across shared edges.

All of this is floating point. Faces are oriented so that the outward normal
follows the right-hand rule.
"""

import math
from collections import deque

from mp3geom import boundary_loop, directed_edges, solve


def corner_angles_3d(points, faces):
    """The angle of each corner, as a list indexed by 3 * face + corner."""
    out = []
    for f in faces:
        for k in range(3):
            p, a, b = (points[f[(k + j) % 3]] for j in range(3))
            u = [float(a[i]) - float(p[i]) for i in range(len(p))]
            v = [float(b[i]) - float(p[i]) for i in range(len(p))]
            uv = sum(x * y for x, y in zip(u, v))
            if len(p) == 2:
                cr = abs(u[0] * v[1] - u[1] * v[0])
            else:
                cr = math.sqrt((u[1] * v[2] - u[2] * v[1]) ** 2 + (u[2] * v[0] - u[0] * v[2]) ** 2 + (u[0] * v[1] - u[1] * v[0]) ** 2)
            out.append(math.atan2(cr, uv))
    return out


def inner_vertices(faces):
    bnd = set(boundary_loop(faces))
    return sorted({v for f in faces for v in f} - bnd)


def corners_at(faces):
    """Map each vertex to the list of (face, corner) where it appears."""
    at = {}
    for i, f in enumerate(faces):
        for k in range(3):
            at.setdefault(f[k], []).append((i, k))
    return at


def constraints(faces, alpha, inner, at, wheel=True):
    """The constraint values C and the rows of the Jacobian J, as sparse dicts."""
    c, rows = [], []
    for i in range(len(faces)):
        c.append(alpha[3 * i] + alpha[3 * i + 1] + alpha[3 * i + 2] - math.pi)
        rows.append({3 * i: 1.0, 3 * i + 1: 1.0, 3 * i + 2: 1.0})
    for v in inner:
        c.append(sum(alpha[3 * i + k] for i, k in at[v]) - 2 * math.pi)
        rows.append({3 * i + k: 1.0 for i, k in at[v]})
    if wheel:
        for v in inner:
            s, row = 0.0, {}
            for i, k in at[v]:
                nx, pv = 3 * i + (k + 1) % 3, 3 * i + (k + 2) % 3
                s += math.log(math.sin(alpha[nx])) - math.log(math.sin(alpha[pv]))
                row[nx] = row.get(nx, 0.0) + 1 / math.tan(alpha[nx])
                row[pv] = row.get(pv, 0.0) - 1 / math.tan(alpha[pv])
            c.append(s)
            rows.append(row)
    return c, rows


def target_angles(points, faces):
    beta = corner_angles_3d(points, faces)
    at = corners_at(faces)
    for v in inner_vertices(faces):
        total = sum(beta[3 * i + k] for i, k in at[v])
        for i, k in at[v]:
            beta[3 * i + k] *= 2 * math.pi / total
    return beta


def objective(alpha, beta):
    return sum((a - b) ** 2 / (b * b) for a, b in zip(alpha, beta))


def abf_angles(points, faces, tol=1e-13, max_iter=60, wheel=True):
    """Solve for the planar angles. Returns (alpha, number of iterations)."""
    inner = inner_vertices(faces)
    at = corners_at(faces)
    beta = target_angles(points, faces)  # @line L1
    hinv = [b * b / 2 for b in beta]
    alpha = list(beta)  # @line L2
    for it in range(1, max_iter + 1):  # @line L3
        c, rows = constraints(faces, alpha, inner, at, wheel)  # @line L4
        g = [2 * (a - b) / (b * b) for a, b in zip(alpha, beta)]
        m = len(rows)
        # Schur complement: (J H^-1 J^T) lam = C - J H^-1 g
        s = [[0.0] * m for _ in range(m)]
        rhs = [[c[r] - sum(val * hinv[j] * g[j] for j, val in rows[r].items())] for r in range(m)]
        for r in range(m):
            for q in range(r, m):
                common = rows[r].keys() & rows[q].keys()
                val = sum(rows[r][j] * hinv[j] * rows[q][j] for j in common)
                s[r][q] = s[q][r] = val
        lam = [x[0] for x in solve(s, rhs, tol=1e-300)]  # @line L5
        step = [-hinv[j] * g[j] for j in range(len(alpha))]
        for r in range(m):
            for j, val in rows[r].items():
                step[j] -= hinv[j] * val * lam[r]
        alpha = [a + d for a, d in zip(alpha, step)]  # @line L6
        if max(abs(x) for x in c) <= tol and max(abs(d) for d in step) <= tol:  # @line L7
            break
    else:
        raise ValueError("no convergence")
    if not all(0 < a < math.pi for a in alpha):
        raise ValueError("an angle is outside (0, pi)")
    return alpha, it


def layout(points, faces, alpha):
    """Place the triangles across shared edges in breadth-first order. Returns {vertex: (x, y)}."""
    de = directed_edges(faces)
    f0 = faces[0]
    p0, p1 = points[f0[0]], points[f0[1]]
    length = math.sqrt(sum((float(a) - float(b)) ** 2 for a, b in zip(p0, p1)))
    x = {f0[0]: (0.0, 0.0), f0[1]: (length, 0.0)}  # @line L8

    def third(face, k):
        """Position of the corner k+2 of the face from the corners k and k+1."""
        a, b, c = (faces[face][(k + j) % 3] for j in range(3))
        aa, ab, ac = (alpha[3 * face + (k + j) % 3] for j in range(3))
        r = math.sin(ab) / math.sin(ac)
        dx, dy = x[b][0] - x[a][0], x[b][1] - x[a][1]
        co, si = math.cos(aa), math.sin(aa)
        return c, (x[a][0] + r * (co * dx - si * dy), x[a][1] + r * (si * dx + co * dy))

    c, pos = third(0, 0)
    x[c] = pos
    seen, queue = {0}, deque([0])
    while queue:  # @line L9
        f = queue.popleft()
        for k in range(3):
            i, j = faces[f][k], faces[f][(k + 1) % 3]
            if (j, i) in de:
                g, kg = de[(j, i)]
                if g not in seen:
                    seen.add(g)
                    c, pos = third(g, kg)
                    if c not in x:
                        x[c] = pos
                    queue.append(g)
    return x  # @line L10


def layout_residual(faces, alpha, x):
    """The largest distance between a placed vertex and where its triangle puts it."""
    worst = 0.0
    for f, tri in enumerate(faces):
        for k in range(3):
            a, b, c = (tri[(k + j) % 3] for j in range(3))
            aa, ab, ac = (alpha[3 * f + (k + j) % 3] for j in range(3))
            r = math.sin(ab) / math.sin(ac)
            dx, dy = x[b][0] - x[a][0], x[b][1] - x[a][1]
            co, si = math.cos(aa), math.sin(aa)
            px, py = x[a][0] + r * (co * dx - si * dy), x[a][1] + r * (si * dx + co * dy)
            worst = max(worst, math.hypot(px - x[c][0], py - x[c][1]))
    return worst


def angle_based_flattening(points, faces):
    alpha, _ = abf_angles(points, faces)
    return layout(points, faces, alpha)
