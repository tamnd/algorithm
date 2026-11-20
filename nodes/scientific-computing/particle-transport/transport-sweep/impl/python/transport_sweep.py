# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transport-sweep/. The authors are listed in prov/WZRH6P.jsonl.
"""Transport sweeps for one direction of flight.

A sweep solves the discrete equation

    Omega . grad psi + sigma_t psi = q

for one fixed direction Omega, cell by cell, in an order in which every cell
comes after the cells that send particles into it (its upstream cells).

Unstructured meshes: a mesh is a number of cells and a list of faces
(a, b, nx, ny, area). The normal (nx, ny) is a unit vector that points out of
cell a. b is the cell on the other side, or -1 for a face on the boundary.
The cell equation is the upwind (step) finite volume balance

    sigma_t V psi_c + sum_out (Omega . n) A psi_c - sum_in |Omega . n| A psi_up = q V,

which is first order and never negative. The order is found by Kahn's
topological sort of the graph upstream cell -> downstream cell; a cycle is
reported with the cells that could not be ordered.

Cartesian meshes: sweep_dd_2d is the diamond difference sweep of one
direction on a rectangle grid, which is second order and can give negative
values in thick cells.
"""

import math
from collections import deque


def _cell_faces(n_cells, faces):
    lists = [[] for _ in range(n_cells)]
    for f, (a, b, _, _, _) in enumerate(faces):
        lists[a].append(f)
        if b >= 0:
            lists[b].append(f)
    return lists


def _flow(face, omega):
    """Omega . n times the area, positive when particles cross from a to b."""
    _, _, nx, ny, area = face
    return (omega[0] * nx + omega[1] * ny) * area


def sweep_order(n_cells, faces, omega):
    """Kahn order of the cells for direction omega. Returns (order, blocked).

    blocked is the list of cells that lie on or after a cycle; it is empty for an acyclic mesh."""
    down = [[] for _ in range(n_cells)]
    indeg = [0] * n_cells
    for face in faces:
        a, b = face[0], face[1]
        if b < 0:
            continue
        g = _flow(face, omega)
        if g > 0:
            down[a].append(b)
            indeg[b] += 1
        elif g < 0:
            down[b].append(a)
            indeg[a] += 1
    queue = deque(c for c in range(n_cells) if indeg[c] == 0)
    order = []
    while queue:
        c = queue.popleft()
        order.append(c)
        for d in down[c]:
            indeg[d] -= 1
            if indeg[d] == 0:
                queue.append(d)
    blocked = [c for c in range(n_cells) if indeg[c] > 0]
    return order, blocked


def wavefronts(n_cells, faces, omega):
    """Level of each cell: 1 for cells without upstream cells, else 1 + the largest level upstream.

    Cells of the same level can be solved at the same time. Returns (levels, number of levels)."""
    order, blocked = sweep_order(n_cells, faces, omega)
    if blocked:
        raise ValueError("the mesh has a cycle for this direction")
    level = [1] * n_cells
    cf = _cell_faces(n_cells, faces)
    for c in order:
        for f in cf[c]:
            a, b = faces[f][0], faces[f][1]
            if b < 0:
                continue
            g = _flow(faces[f], omega)
            up = a if g > 0 else b if g < 0 else -1
            if up >= 0 and up != c:
                level[c] = max(level[c], level[up] + 1)
    return level, max(level)


def sweep_step(n_cells, faces, volume, sigma_t, q, omega, psi_in=0.0):
    """Upwind sweep of one direction on an unstructured mesh.

    psi_in is the incoming angular flux on the boundary (a number, or a function of the face index).
    Returns (psi per cell, outflow through the boundary, inflow through the boundary)."""
    cf = _cell_faces(n_cells, faces)
    down = [[] for _ in range(n_cells)]
    indeg = [0] * n_cells
    for face in faces:  # @line L1
        a, b = face[0], face[1]
        if b < 0:
            continue
        g = _flow(face, omega)
        if g > 0:
            down[a].append(b)
            indeg[b] += 1  # @line L2
        elif g < 0:
            down[b].append(a)
            indeg[a] += 1
    queue = deque(c for c in range(n_cells) if indeg[c] == 0)  # @line L3
    psi = [0.0] * n_cells
    done = [False] * n_cells
    outflow = inflow = 0.0
    while queue:  # @line L4
        c = queue.popleft()
        num = q[c] * volume[c]
        den = sigma_t[c] * volume[c]
        for f in cf[c]:
            a, b = faces[f][0], faces[f][1]
            g = _flow(faces[f], omega)
            if c == b:
                g = -g  # the flow out of c through this face
            other = b if c == a else a
            if g > 0:
                den += g
            elif g < 0:
                if other < 0:
                    v = psi_in(f) if callable(psi_in) else psi_in
                    inflow += -g * v
                else:
                    v = psi[other]
                num += -g * v
        psi[c] = num / den  # @line L5
        done[c] = True
        for d in down[c]:  # @line L6
            indeg[d] -= 1
            if indeg[d] == 0:
                queue.append(d)
    if not all(done):  # @line L7
        raise ValueError("the mesh has a cycle for this direction: cells %s" % [c for c in range(n_cells) if not done[c]])
    for f, (a, b, _, _, _) in enumerate(faces):
        if b < 0:
            g = _flow(faces[f], omega)
            if g > 0:
                outflow += g * psi[a]
    return psi, outflow, inflow


def cartesian_mesh(nx, ny, lx, ly):
    """Rectangle cells numbered i + nx j. Returns (number of cells, faces, volumes, centroids)."""
    hx, hy = lx / nx, ly / ny
    faces = []
    for j in range(ny):
        for i in range(nx):
            c = i + nx * j
            faces.append((c, c + 1 if i < nx - 1 else -1, 1.0, 0.0, hy))
            faces.append((c, c + nx if j < ny - 1 else -1, 0.0, 1.0, hx))
            if i == 0:
                faces.append((c, -1, -1.0, 0.0, hy))
            if j == 0:
                faces.append((c, -1, 0.0, -1.0, hx))
    cent = [((i + 0.5) * hx, (j + 0.5) * hy) for j in range(ny) for i in range(nx)]
    return nx * ny, faces, [hx * hy] * (nx * ny), cent


def triangle_mesh(nx, ny, lx, ly):
    """Each rectangle cut along its rising diagonal into a lower triangle 2k and an upper triangle 2k + 1."""
    hx, hy = lx / nx, ly / ny
    d = math.hypot(hx, hy)
    dn = (-hy / d, hx / d)  # normal of the diagonal, out of the lower triangle
    faces = []
    for j in range(ny):
        for i in range(nx):
            k = i + nx * j
            lo, up = 2 * k, 2 * k + 1
            faces.append((lo, up, dn[0], dn[1], d))
            # the lower triangle has the bottom and right sides, the upper one the top and left sides
            faces.append((lo, 2 * (k - nx) + 1 if j > 0 else -1, 0.0, -1.0, hx))
            faces.append((lo, 2 * (k + 1) + 1 if i < nx - 1 else -1, 1.0, 0.0, hy))
            if j == ny - 1:
                faces.append((up, -1, 0.0, 1.0, hx))
            if i == 0:
                faces.append((up, -1, -1.0, 0.0, hy))
    cent = []
    for j in range(ny):
        for i in range(nx):
            x0, y0 = i * hx, j * hy
            cent.append((x0 + 2 * hx / 3, y0 + hy / 3))
            cent.append((x0 + hx / 3, y0 + 2 * hy / 3))
    return 2 * nx * ny, faces, [hx * hy / 2] * (2 * nx * ny), cent


def sweep_dd_2d(mu, eta, sigma_t, q, dx, dy, inc_x, inc_y):
    """Diamond difference sweep of the direction (mu, eta) on a rectangle grid.

    sigma_t[i][j] and q[i][j] are the cell data, inc_x[j] the incoming values on the x face where the
    direction enters, inc_y[i] those on the y face. Returns (cell values, outgoing x face values,
    outgoing y face values)."""
    nx, ny = len(dx), len(dy)
    ii = list(range(nx)) if mu > 0 else list(range(nx - 1, -1, -1))
    jj = list(range(ny)) if eta > 0 else list(range(ny - 1, -1, -1))
    face_y = list(inc_y)
    out_x = [0.0] * ny
    cells = [[0.0] * ny for _ in range(nx)]
    for j in jj:
        face_x = inc_x[j]
        for i in ii:
            a = 2.0 * abs(mu) / dx[i]
            b = 2.0 * abs(eta) / dy[j]
            c = (q[i][j] + a * face_x + b * face_y[i]) / (sigma_t[i][j] + a + b)
            cells[i][j] = c
            face_x = 2.0 * c - face_x
            face_y[i] = 2.0 * c - face_y[i]
        out_x[j] = face_x
    return cells, out_x, face_y
