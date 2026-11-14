# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arap-parameterization/. The authors are listed in prov/7SBDXS.jsonl.

"""As-rigid-as-possible parameterization (Liu, Zhang, Xu, Gotsman and Gortler 2008).

Each triangle t gets a congruent 2D frame. For a map u of the vertices to
the plane, J_t is the 2 x 2 Jacobian of the linear map from the frame of t
to its image. The energy is

    E(u, R) = sum_t A_t || J_t - R_t ||_F^2,

with R_t a rotation. The local step sets each R_t to the rotation closest to
J_t. The global step fixes the R_t and solves a linear least squares problem
in u, with the cotangent Laplacian of the mesh as its matrix. One vertex is
pinned, because E does not change when u is translated.
"""

import math

from mx2geom import boundary_loop, cholesky, cholesky_solve, length, solve, triangle_frame, undirected_edges


def tutte_start(vertices, faces):
    """A uniform-weight Tutte map with the boundary on the unit circle by arc length (no flips)."""
    loop = boundary_loop(faces)
    nxt = {loop[k]: loop[(k + 1) % len(loop)] for k in range(len(loop))}
    total = sum(length(vertices[v], vertices[nxt[v]]) for v in loop)
    pos, s = {}, 0.0
    for v in loop:
        t = 2 * math.pi * s / total
        pos[v] = (math.cos(t), math.sin(t))
        s += length(vertices[v], vertices[nxt[v]])
    nb = {}
    for i, j in undirected_edges(faces):
        nb.setdefault(i, set()).add(j)
        nb.setdefault(j, set()).add(i)
    inner = [v for v in sorted(nb) if v not in pos]
    idx = {v: k for k, v in enumerate(inner)}
    a = [[0.0] * len(inner) for _ in inner]
    b = [[0.0, 0.0] for _ in inner]
    for v in inner:
        r = idx[v]
        a[r][r] = float(len(nb[v]))
        for w in nb[v]:
            if w in idx:
                a[r][idx[w]] -= 1.0
            else:
                b[r][0] += pos[w][0]
                b[r][1] += pos[w][1]
    x = solve(a, b) if inner else []
    for v in inner:
        pos[v] = (x[idx[v]][0], x[idx[v]][1])
    return [pos[v] for v in range(len(vertices))]


def frames(vertices, faces):
    """For each face: the 2D frame corners, the area, and the cotangent of the angle at each corner."""
    out = []
    for a, b, c in faces:
        q = triangle_frame(vertices[a], vertices[b], vertices[c])
        area = 0.5 * ((q[1][0] - q[0][0]) * (q[2][1] - q[0][1]) - (q[1][1] - q[0][1]) * (q[2][0] - q[0][0]))
        if area <= 0:
            raise ValueError("degenerate triangle")
        cots = []
        for k in range(3):
            p, r, s = q[k], q[(k + 1) % 3], q[(k + 2) % 3]
            ux, uy, vx, vy = r[0] - p[0], r[1] - p[1], s[0] - p[0], s[1] - p[1]
            cots.append((ux * vx + uy * vy) / (ux * vy - uy * vx))
        out.append((q, area, cots))
    return out


def jacobian(q, area, w):
    """The Jacobian of the linear map from the frame q to the image points w, as ((a, b), (c, d))."""
    # Gradients of the three corner functions, from the edge opposite each corner.
    j = [[0.0, 0.0], [0.0, 0.0]]
    for k in range(3):
        e = (q[(k + 2) % 3][0] - q[(k + 1) % 3][0], q[(k + 2) % 3][1] - q[(k + 1) % 3][1])
        g = (-e[1] / (2 * area), e[0] / (2 * area))
        for r in range(2):
            j[r][0] += w[k][r] * g[0]
            j[r][1] += w[k][r] * g[1]
    return j


def closest_rotation(j):
    """The rotation R that maximizes trace(R^T J), the closest rotation to J in the Frobenius norm."""
    c, s = j[0][0] + j[1][1], j[1][0] - j[0][1]
    if c == 0 and s == 0:
        return ((1.0, 0.0), (0.0, 1.0))
    r = math.hypot(c, s)
    return ((c / r, -s / r), (s / r, c / r))


def energy(fr, faces, u, rots=None):
    """E(u, R); with rots None, each R_t is the closest rotation, which gives min over R of E(u, R)."""
    total = 0.0
    for t, (q, area, _) in enumerate(fr):
        j = jacobian(q, area, [u[v] for v in faces[t]])
        r = closest_rotation(j) if rots is None else rots[t]
        total += area * sum((j[a][b] - r[a][b]) ** 2 for a in range(2) for b in range(2))
    return total


def global_matrix(fr, faces, n, pin):
    """The cotangent Laplacian with the row and column of the pinned vertex removed, and the index map."""
    idx = {v: k for k, v in enumerate(v for v in range(n) if v != pin)}
    a = [[0.0] * (n - 1) for _ in range(n - 1)]
    for (q, area, cots), tri in zip(fr, faces):
        for k in range(3):
            # cots[k] is the angle at corner k, which is opposite the edge (k+1, k+2).
            w = 0.5 * cots[k]
            i, j = tri[(k + 1) % 3], tri[(k + 2) % 3]
            for x, y, val in ((i, i, w), (j, j, w), (i, j, -w), (j, i, -w)):
                if x != pin and y != pin:
                    a[idx[x]][idx[y]] += val
    return a, idx


def global_step(fr, faces, n, pin, pin_pos, rots, factor, idx):
    """The u that minimizes E(u, R) for the fixed rotations, with u[pin] = pin_pos."""
    b = [[0.0] * (n - 1), [0.0] * (n - 1)]
    for (q, area, cots), tri, r in zip(fr, faces, rots):  # @line L7
        for k in range(3):
            w = 0.5 * cots[k]
            ki, kj = (k + 1) % 3, (k + 2) % 3
            i, j = tri[ki], tri[kj]
            e = (q[ki][0] - q[kj][0], q[ki][1] - q[kj][1])
            d = (r[0][0] * e[0] + r[0][1] * e[1], r[1][0] * e[0] + r[1][1] * e[1])
            for c in range(2):
                # Terms of w * |(u_i - u_j) - d|^2 that are linear in u, and the pinned vertex.
                if i != pin:
                    b[c][idx[i]] += w * d[c] + (w * pin_pos[c] if j == pin else 0.0)
                if j != pin:
                    b[c][idx[j]] += -w * d[c] + (w * pin_pos[c] if i == pin else 0.0)
    xs = [cholesky_solve(factor, b[c]) for c in range(2)]  # @line L8
    u = [None] * n
    for v in range(n):
        u[v] = pin_pos if v == pin else (xs[0][idx[v]], xs[1][idx[v]])
    return u


def arap_parameterization(vertices, faces, iterations=20, start=None, pin=None):
    """Run the local and global steps from a start map (default: Tutte). Returns (u, energies).

    energies[k] is min over R of E(u_k, R) for the map after k global steps.
    """
    n = len(vertices)
    fr = frames(vertices, faces)  # @line L1
    u = list(start) if start is not None else tutte_start(vertices, faces)
    if pin is None:
        pin = faces[0][0]
    a, idx = global_matrix(fr, faces, n, pin)  # @line L2
    factor = cholesky(a)  # @line L3
    energies = [energy(fr, faces, u)]
    for _ in range(iterations):  # @line L4
        rots = []
        for (q, area, _), tri in zip(fr, faces):  # @line L5
            rots.append(closest_rotation(jacobian(q, area, [u[v] for v in tri])))  # @line L6
        u = global_step(fr, faces, n, pin, u[pin], rots, factor, idx)
        energies.append(energy(fr, faces, u))
    return u, energies  # @line L9
