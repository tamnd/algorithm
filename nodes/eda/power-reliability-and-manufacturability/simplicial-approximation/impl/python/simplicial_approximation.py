# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simplicial-approximation/. The authors are listed in prov/TB95X2.jsonl.
"""Simplicial approximation for design centering in the plane (after Director and Hachtel 1977).

The feasible region R is known only through a line search oracle:
exit_point(x, d) returns the point where the ray x + t d, t >= 0, first
leaves R, for a point x of R. The method keeps a set of boundary points,
takes their convex hull, puts the largest inscribed disc in the hull by a
linear program, and adds a new boundary point found from the middle of the
longest edge that touches the disc, along the outward normal of that edge.

simplicial_approximation returns one record per iteration with the hull,
the centre and the radius. The method assumes that R is convex; on a
nonconvex region the hull can leave R.
"""

import math


def convex_hull(points):
    """Andrew's monotone chain; vertices in counterclockwise order, no collinear ones."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 1e-12:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 1e-12:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def edges(hull):
    """Edges (a, b, unit outward normal, offset): the hull is n . x <= offset."""
    out = []
    for i, a in enumerate(hull):
        b = hull[(i + 1) % len(hull)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy)
        nrm = (dy / length, -dx / length)
        out.append((a, b, nrm, nrm[0] * a[0] + nrm[1] * a[1]))
    return out


def inscribed_disc(faces, inner):
    """The LP max r subject to n_f . c + r <= b_f, by the simplex method.

    inner is a point strictly inside the polygon. The variables are
    c - inner split into positive and negative parts, and r, so the origin
    is a feasible basis. Bland's rule prevents cycling.
    """
    m = len(faces)
    rows = []
    for i, (_, _, (nx, ny), off) in enumerate(faces):
        slack = [1.0 if j == i else 0.0 for j in range(m)]
        rows.append([nx, -nx, ny, -ny, 1.0] + slack + [off - nx * inner[0] - ny * inner[1]])
    cost = [0.0, 0.0, 0.0, 0.0, -1.0] + [0.0] * m + [0.0]
    basis = [5 + i for i in range(m)]
    while True:
        enter = next((j for j in range(5 + m) if cost[j] < -1e-12), None)
        if enter is None:
            break
        best = None
        for i in range(m):
            if rows[i][enter] > 1e-12:
                ratio = rows[i][-1] / rows[i][enter]
                if best is None or ratio < best[0] - 1e-15 or (abs(ratio - best[0]) <= 1e-15 and basis[i] < basis[best[1]]):
                    best = (ratio, i)
        i = best[1]
        piv = rows[i][enter]
        rows[i] = [x / piv for x in rows[i]]
        for k in range(m):
            if k != i and rows[k][enter] != 0.0:
                f = rows[k][enter]
                rows[k] = [x - f * y for x, y in zip(rows[k], rows[i])]
        f = cost[enter]
        cost = [x - f * y for x, y in zip(cost, rows[i])]
        basis[i] = enter
    x = [0.0] * 5
    for i, j in enumerate(basis):
        if j < 5:
            x[j] = rows[i][-1]
    return (inner[0] + x[0] - x[1], inner[1] + x[2] - x[3]), x[4]


def simplicial_approximation(exit_point, x0, iterations, rule="tangent", tol=1e-9):
    points = [exit_point(x0, d) for d in ((1, 0), (0, 1), (-1, 0), (0, -1))]  # @line L1
    on_boundary = set()
    history = []
    for _ in range(iterations):  # @line L2
        hull = convex_hull(points)  # @line L3
        faces = edges(hull)
        inner = (sum(p[0] for p in hull) / len(hull), sum(p[1] for p in hull) / len(hull))
        centre, radius = inscribed_disc(faces, inner)  # @line L4
        history.append({"hull": hull, "centre": centre, "radius": radius})
        scale = max(1.0, radius)
        if rule == "tangent":  # @line L5
            cand = [f for f in faces if f[3] - f[2][0] * centre[0] - f[2][1] * centre[1] - radius <= 1e-7 * scale]
        else:
            cand = list(faces)
        cand.sort(key=lambda f: -math.dist(f[0], f[1]))  # @line L6
        added = False
        for a, b, nrm, _ in cand:
            if (a, b) in on_boundary:
                continue
            mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)  # @line L7
            y = exit_point(mid, nrm)  # @line L8
            if math.dist(y, mid) > tol * scale:
                points.append(y)  # @line L9
                added = True
                break
            on_boundary.add((a, b))  # @line L10
        if not added:  # @line L11
            break
    return history  # @line L12
