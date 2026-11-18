# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/continuum-crowds/. The authors are listed in prov/RXA6V1.jsonl.
"""Continuum crowds (Treuille, Cooper and Popovic 2006) on a small 2D grid.

The grid has nx by ny square cells of size dx. Scalar fields are lists of
rows indexed [i][j], with i the x index and j the y index; cell (i, j) has
its center at ((i + 1/2) dx, (j + 1/2) dx). Anisotropic fields (speed f and
unit cost C) have one value per cell and direction, in the order
E, N, W, S (theta = 0, 90, 180 and 270 degrees).

One time step for one group:
  1. splat the people into the density rho and the mean velocity vbar;
  2. compute the speed f and the unit cost C = (alpha f + beta + gamma g) / f
     for every cell and direction, evaluated at the cell one moves into;
  3. solve the discrete eikonal equation |grad phi| = C with phi = 0 in the
     goal by fast marching;
  4. move every person with x' = -f grad(phi) / |grad(phi)|;
  5. push apart pairs closer than a minimum distance.

The local update of step 3 is the upwind form: for each axis the active
neighbor is the one with the largest (phi_M - phi_i) / (dx C_M->i), and
phi_M solves sum over the active axes of ((phi_M - phi_i) / (dx C_M->i))^2
= 1. When the two faces of an axis have the same cost this is the rule of
the paper (the neighbor with the smaller phi_i + C_M->i). solve_brute
iterates the same update over all cells until no value changes; it is the
reference that the fast marching result must equal.
"""

import heapq
import math

INF = float("inf")
DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))  # E, N, W, S
OPP = (2, 3, 0, 1)


def grid(nx, ny, value=0.0):
    return [[value] * ny for _ in range(nx)]


def _candidates(xs, ys):
    """xs, ys: lists of (phi_i, h_i) for the two neighbors of each axis, with
    h_i = dx C_M->i. Return the upwind solution phi_M (INF if none)."""
    best = INF
    for a in xs + [None]:
        for b in ys + [None]:
            terms = [t for t in (a, b) if t is not None and t[0] < INF and t[1] < INF]
            if len(terms) == 1:
                p, h = terms[0]
                best = min(best, p + h)
            elif len(terms) == 2:
                (p1, h1), (p2, h2) = terms
                w1, w2 = 1.0 / (h1 * h1), 1.0 / (h2 * h2)
                qa = w1 + w2
                qb = -2.0 * (p1 * w1 + p2 * w2)
                qc = p1 * p1 * w1 + p2 * p2 * w2 - 1.0
                disc = qb * qb - 4.0 * qa * qc
                if disc >= 0.0:
                    r = (-qb + math.sqrt(disc)) / (2.0 * qa)
                    if r >= max(p1, p2):
                        best = min(best, r)
    return best


def local_update(phi, cost, i, j, dx, known=None):
    """The upwind update of cell (i, j) from its four neighbors.

    cost[i][j][d] is C_M->neighbor d. Neighbors outside the grid, with an
    infinite cost, or not in `known` (when given) are left out.
    """
    nx, ny = len(phi), len(phi[0])
    axis = ([], [])
    for d, (di, dj) in enumerate(DIRS):
        a, b = i + di, j + dj
        if 0 <= a < nx and 0 <= b < ny and (known is None or known[a][b]):
            h = dx * cost[i][j][d]
            axis[d % 2].append((phi[a][b], h))
    return _candidates(axis[0], axis[1])  # @line L6


def fast_march(cost, goal, dx):
    """Return (phi, order): the potential and the order of acceptance.

    cost[i][j][d] = C_M->d (INF for an obstacle face), goal: list of cells.
    """
    nx, ny = len(cost), len(cost[0])
    phi = grid(nx, ny, INF)
    known = grid(nx, ny, False)
    heap = []
    for (i, j) in goal:
        phi[i][j] = 0.0  # @line L1
        heapq.heappush(heap, (0.0, i, j))
    order = []
    while heap:  # @line L2
        p, i, j = heapq.heappop(heap)  # @line L3
        if known[i][j] or p > phi[i][j]:
            continue
        known[i][j] = True  # @line L4
        order.append((i, j))
        for di, dj in DIRS:  # @line L5
            a, b = i + di, j + dj
            if 0 <= a < nx and 0 <= b < ny and not known[a][b]:
                v = local_update(phi, cost, a, b, dx, known)
                if v < phi[a][b]:
                    phi[a][b] = v  # @line L7
                    heapq.heappush(heap, (v, a, b))
    return phi, order  # @line L8


def solve_brute(cost, goal, dx, max_sweeps=100000):
    """Iterate the local update over all cells (Jacobi) until no change."""
    nx, ny = len(cost), len(cost[0])
    goals = set(goal)
    phi = grid(nx, ny, INF)
    for (i, j) in goal:
        phi[i][j] = 0.0
    for _ in range(max_sweeps):
        new = [row[:] for row in phi]
        changed = False
        for i in range(nx):
            for j in range(ny):
                if (i, j) in goals:
                    continue
                v = local_update(phi, cost, i, j, dx)
                if v != phi[i][j]:
                    new[i][j] = v
                    changed = True
        phi = new
        if not changed:
            return phi
    raise RuntimeError("no convergence")


def splat(people, nx, ny, dx, lam):
    """Density rho and mean velocity vbar (Section 4.1 of the paper).

    people: list of ((x, y), (vx, vy)). Each person adds
    min(1 - Dx, 1 - Dy)^lam, min(Dx, 1 - Dy)^lam, min(Dx, Dy)^lam and
    min(1 - Dx, Dy)^lam to the cells A, B, C and D around it, where
    (Dx, Dy) is its offset from the center of A in cell units.
    """
    rho = grid(nx, ny)
    mvx, mvy = grid(nx, ny), grid(nx, ny)
    for (px, py), (vx, vy) in people:
        u, v = px / dx - 0.5, py / dx - 0.5
        i, j = math.floor(u), math.floor(v)
        ddx, ddy = u - i, v - j
        for (a, b, w) in (
            (i, j, min(1 - ddx, 1 - ddy) ** lam),
            (i + 1, j, min(ddx, 1 - ddy) ** lam),
            (i + 1, j + 1, min(ddx, ddy) ** lam),
            (i, j + 1, min(1 - ddx, ddy) ** lam),
        ):
            if 0 <= a < nx and 0 <= b < ny:
                rho[a][b] += w
                mvx[a][b] += w * vx
                mvy[a][b] += w * vy
    vbar = [[(mvx[i][j] / rho[i][j], mvy[i][j] / rho[i][j]) if rho[i][j] > 0 else (0.0, 0.0)
             for j in range(ny)] for i in range(nx)]
    return rho, vbar


def speed_and_cost(rho, vbar, disc, params):
    """Speed f (Eq. 10, flat terrain so f_T = f_max) and unit cost C (Eq. 4),
    both evaluated at the neighbor cell in each direction."""
    fmax, fmin_flow = params["fmax"], params.get("fmin", 1e-3)
    rmin, rmax = params["rho_min"], params["rho_max"]
    al, be, ga = params["alpha"], params["beta"], params["gamma"]
    nx, ny = len(rho), len(rho[0])
    f = [[[0.0] * 4 for _ in range(ny)] for _ in range(nx)]
    C = [[[INF] * 4 for _ in range(ny)] for _ in range(nx)]
    for i in range(nx):
        for j in range(ny):
            for d, (di, dj) in enumerate(DIRS):
                a, b = i + di, j + dj
                if not (0 <= a < nx and 0 <= b < ny) or disc[a][b] == INF:
                    continue
                ft = fmax
                fv = max(0.0, vbar[a][b][0] * di + vbar[a][b][1] * dj)
                r = rho[a][b]
                if r <= rmin:
                    s = ft
                elif r >= rmax:
                    s = fv
                else:
                    s = ft + (r - rmin) / (rmax - rmin) * (fv - ft)
                s = max(s, fmin_flow)
                f[i][j][d] = s
                C[i][j][d] = (al * s + be + ga * disc[a][b]) / s
    return f, C


def velocity_field(phi, f, dx):
    """v = -f grad(phi) / |grad(phi)| with upwind one sided differences."""
    nx, ny = len(phi), len(phi[0])
    vel = grid(nx, ny, (0.0, 0.0))
    for i in range(nx):
        for j in range(ny):
            if phi[i][j] == INF:
                continue
            comp = []
            for axis in (0, 1):
                best, bd = 0.0, None
                for d in (axis, axis + 2):
                    di, dj = DIRS[d]
                    a, b = i + di, j + dj
                    if 0 <= a < nx and 0 <= b < ny and phi[a][b] < phi[i][j]:
                        drop = phi[i][j] - phi[a][b]
                        if drop > best:
                            best, bd = drop, d
                comp.append((best / dx, bd))
            g = math.hypot(comp[0][0], comp[1][0])
            if g == 0.0:
                continue
            v = [0.0, 0.0]
            for axis in (0, 1):
                mag, d = comp[axis]
                if d is not None:
                    di, dj = DIRS[d]
                    v[axis] = f[i][j][d] * mag / g * (di + dj)
            vel[i][j] = (v[0], v[1])
    return vel


def enforce_min_distance(pos, dmin):
    """Push apart every pair closer than dmin, half each (one pass)."""
    n = len(pos)
    pos = [list(p) for p in pos]
    for a in range(n):
        for b in range(a + 1, n):
            dx_, dy_ = pos[b][0] - pos[a][0], pos[b][1] - pos[a][1]
            d = math.hypot(dx_, dy_)
            if 0.0 < d < dmin:
                push = 0.5 * (dmin - d) / d
                pos[a][0] -= push * dx_
                pos[a][1] -= push * dy_
                pos[b][0] += push * dx_
                pos[b][1] += push * dy_
    return [tuple(p) for p in pos]


def step(people, goal, nx, ny, dx, dt, params, disc=None):
    """One time step for one group. Return (new people, phi)."""
    if disc is None:
        disc = grid(nx, ny)
    rho, vbar = splat(people, nx, ny, dx, params["lam"])
    f, C = speed_and_cost(rho, vbar, disc, params)
    phi, _ = fast_march(C, goal, dx)
    vel = velocity_field(phi, f, dx)
    pos = []
    vels = []
    for (px, py), _ in people:
        i = min(nx - 1, max(0, int(px / dx)))
        j = min(ny - 1, max(0, int(py / dx)))
        vx, vy = vel[i][j]
        pos.append((min(nx * dx - 1e-9, max(1e-9, px + dt * vx)),
                    min(ny * dx - 1e-9, max(1e-9, py + dt * vy))))
        vels.append((vx, vy))
    pos = enforce_min_distance(pos, params["dmin"])
    return list(zip(pos, vels)), phi


def sample(phi, p, dx):
    nx, ny = len(phi), len(phi[0])
    i = min(nx - 1, max(0, int(p[0] / dx)))
    j = min(ny - 1, max(0, int(p[1] / dx)))
    return phi[i][j]
