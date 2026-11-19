# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marker-and-cell-method/. The authors are listed in prov/B1FT13.jsonl.

"""The marker-and-cell (MAC) method in a closed 2D box [0, Lx] x [0, Ly].

Staggered grid with nx by ny cells:
  p[i + nx * j]        at the cell center ((i + 1/2) dx, (j + 1/2) dy)
  u[i + (nx + 1) * j]  at the vertical face (i dx, (j + 1/2) dy), i = 0..nx
  v[i + nx * j]        at the horizontal face ((i + 1/2) dx, j dy), j = 0..ny
p is the pressure divided by the density. The wall faces (i = 0, nx for u and
j = 0, ny for v) carry zero normal velocity. The tangential velocity at a wall
enters through ghost values: free slip mirrors the first interior value, no
slip sets ghost = 2 u_wall - interior. The pressure equation gets the
homogeneous Neumann condition, and -D G is exactly the matrix of
scisparse.poisson2d(..., bc="neumann").

Marker particles are moved with the interpolated velocity; the cells that
hold a marker are the fluid cells. This file handles confined flow (every
cell is fluid); the free surface conditions of Harlow and Welch are described
on the page but not implemented here.
"""

import scisparse


class Box:
    def __init__(self, nx, ny, lx, ly, slip="free", lid=0.0):
        self.nx, self.ny, self.lx, self.ly = nx, ny, lx, ly
        self.dx, self.dy = lx / nx, ly / ny
        self.slip, self.lid = slip, lid  # lid: tangential wall speed of the top wall
        self.A = scisparse.poisson2d(nx, ny, self.dx, self.dy, bc="neumann")

    def iu(self, i, j):
        return i + (self.nx + 1) * j

    def iv(self, i, j):
        return i + self.nx * j

    def zeros(self):
        return [0.0] * ((self.nx + 1) * self.ny), [0.0] * (self.nx * (self.ny + 1)), [0.0] * (self.nx * self.ny)

    def sample(self, fu, fv):
        """Face values of a velocity field given by two functions of (x, y)."""
        u = [fu(i * self.dx, (j + 0.5) * self.dy) for j in range(self.ny) for i in range(self.nx + 1)]
        v = [fv((i + 0.5) * self.dx, j * self.dy) for j in range(self.ny + 1) for i in range(self.nx)]
        return u, v

    def sample_p(self, fp):
        return [fp((i + 0.5) * self.dx, (j + 0.5) * self.dy) for j in range(self.ny) for i in range(self.nx)]


def u_at(b, u, i, j):
    """u at face (i, j), with ghost rows j = -1 and j = ny from the wall condition."""
    if 0 <= j < b.ny:
        return u[b.iu(i, j)]
    inner = u[b.iu(i, 0 if j < 0 else b.ny - 1)]
    if b.slip == "free":
        return inner
    wall = b.lid if j >= b.ny else 0.0
    return 2 * wall - inner


def v_at(b, v, i, j):
    """v at face (i, j), with ghost columns i = -1 and i = nx from the wall condition."""
    if 0 <= i < b.nx:
        return v[b.iv(i, j)]
    inner = v[b.iv(0 if i < 0 else b.nx - 1, j)]
    return inner if b.slip == "free" else -inner


def divergence(b, u, v):
    nx, dx, dy = b.nx, b.dx, b.dy
    return [(u[b.iu(i + 1, j)] - u[b.iu(i, j)]) / dx + (v[b.iv(i, j + 1)] - v[b.iv(i, j)]) / dy
            for j in range(b.ny) for i in range(nx)]


def gradient(b, p):
    """G p on the interior faces; zero on the wall faces, which the projection does not change."""
    nx, ny = b.nx, b.ny
    gx = [0.0] * ((nx + 1) * ny)
    gy = [0.0] * (nx * (ny + 1))
    for j in range(ny):
        for i in range(1, nx):
            gx[b.iu(i, j)] = (p[i + nx * j] - p[i - 1 + nx * j]) / b.dx
    for j in range(1, ny):
        for i in range(nx):
            gy[b.iv(i, j)] = (p[i + nx * j] - p[i + nx * (j - 1)]) / b.dy
    return gx, gy


def momentum_rhs(b, u, v, nu):
    """-(u . grad) u + nu Laplacian u on the interior faces, central differences."""
    nx, ny, dx, dy = b.nx, b.ny, b.dx, b.dy
    ru = [0.0] * len(u)
    rv = [0.0] * len(v)
    for j in range(ny):
        for i in range(1, nx):
            c = u[b.iu(i, j)]
            e, w = u[b.iu(i + 1, j)], u[b.iu(i - 1, j)]
            n, s = u_at(b, u, i, j + 1), u_at(b, u, i, j - 1)
            vb = 0.25 * (v[b.iv(i - 1, j)] + v[b.iv(i, j)] + v[b.iv(i - 1, j + 1)] + v[b.iv(i, j + 1)])
            adv = c * (e - w) / (2 * dx) + vb * (n - s) / (2 * dy)
            lap = (e - 2 * c + w) / (dx * dx) + (n - 2 * c + s) / (dy * dy)
            ru[b.iu(i, j)] = nu * lap - adv
    for j in range(1, ny):
        for i in range(nx):
            c = v[b.iv(i, j)]
            e, w = v_at(b, v, i + 1, j), v_at(b, v, i - 1, j)
            n, s = v[b.iv(i, j + 1)], v[b.iv(i, j - 1)]
            ub = 0.25 * (u[b.iu(i, j - 1)] + u[b.iu(i + 1, j - 1)] + u[b.iu(i, j)] + u[b.iu(i + 1, j)])
            adv = ub * (e - w) / (2 * dx) + c * (n - s) / (2 * dy)
            lap = (e - 2 * c + w) / (dx * dx) + (n - 2 * c + s) / (dy * dy)
            rv[b.iv(i, j)] = nu * lap - adv
    return ru, rv


def project(b, us, vs, dt, p0=None, tol=1e-12):
    """Solve -D G p = -D u* / dt with the Neumann matrix, then u = u* - dt G p."""
    rhs = [-x / dt for x in divergence(b, us, vs)]
    mean = sum(rhs) / len(rhs)
    rhs = [x - mean for x in rhs]  # zero in exact arithmetic: the wall faces carry no flux
    p, its = scisparse.cg(b.A, rhs, tol=tol, x0=p0)
    gx, gy = gradient(b, p)
    return [us[k] - dt * gx[k] for k in range(len(us))], [vs[k] - dt * gy[k] for k in range(len(vs))], p, its


def interpolate(b, u, v, x, y):
    """Bilinear interpolation of (u, v) at (x, y); needs nx, ny >= 2. Points closer to a
    wall than half a cell use the nearest row (u) or column (v) of unknowns."""
    nx, ny, dx, dy = b.nx, b.ny, b.dx, b.dy

    def bilinear(field, idx, gx, gy, mi, mj):
        i = min(max(int(gx), 0), mi - 1)
        j = min(max(int(gy), 0), mj - 1)
        a, c = gx - i, gy - j
        return ((1 - a) * (1 - c) * field[idx(i, j)] + a * (1 - c) * field[idx(i + 1, j)]
                + (1 - a) * c * field[idx(i, j + 1)] + a * c * field[idx(i + 1, j + 1)])

    gy_u = min(max(y / dy - 0.5, 0.0), ny - 1.0)
    gx_v = min(max(x / dx - 0.5, 0.0), nx - 1.0)
    return bilinear(u, b.iu, x / dx, gy_u, nx, ny - 1), bilinear(v, b.iv, gx_v, y / dy, nx - 1, ny)


def move_markers(b, u, v, markers, dt):
    """One midpoint (RK2) step for every marker; markers are kept inside the box."""
    out = []
    for x, y in markers:
        u1, v1 = interpolate(b, u, v, x, y)
        u2, v2 = interpolate(b, u, v, x + 0.5 * dt * u1, y + 0.5 * dt * v1)
        out.append((min(max(x + dt * u2, 0.0), b.lx), min(max(y + dt * v2, 0.0), b.ly)))
    return out


def fluid_cells(b, markers):
    """The set of cells that hold at least one marker."""
    return {min(int(x / b.dx), b.nx - 1) + b.nx * min(int(y / b.dy), b.ny - 1) for x, y in markers}


def mac(b, u, v, dt, nu, steps, markers=(), gravity=(0.0, 0.0), p=None):
    """Run MAC-STEP a number of times. Returns (u, v, p, markers, fluid cells)."""
    markers = list(markers)
    cells = fluid_cells(b, markers)
    for n in range(steps):  # @line L1
        ru, rv = momentum_rhs(b, u, v, nu)  # @line L2
        us = [u[k] + dt * (ru[k] + gravity[0]) if 0 < k % (b.nx + 1) < b.nx else u[k] for k in range(len(u))]  # @line L3
        vs = [v[k] + dt * (rv[k] + gravity[1]) if 0 < k // b.nx < b.ny else v[k] for k in range(len(v))]  # @line L3
        u, v, p, _ = project(b, us, vs, dt, p0=p)  # @line L4 @line L5
        markers = move_markers(b, u, v, markers, dt)  # @line L6
        cells = fluid_cells(b, markers)  # @line L7
    return u, v, p, markers, cells  # @line L8
