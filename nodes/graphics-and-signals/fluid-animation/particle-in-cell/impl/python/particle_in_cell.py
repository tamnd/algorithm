# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-in-cell/. The authors are listed in prov/N6Z3N3.jsonl.
"""The particle-in-cell method (PIC) for a liquid on a 2D MAC grid.

The particles carry the positions and the velocities. One step labels the
cells, transfers the particle velocities to the faces of the MAC grid (P2G),
adds gravity, makes the grid velocity divergence free with macgrid.project,
interpolates the grid velocity back to the particles (G2P) and moves the
particles through the grid velocity.

The weights are bilinear, with the same clamping as macgrid.sample, so G2P
gives the same values as macgrid.u_at and macgrid.v_at. The grid must have
nx >= 2 and ny >= 2. Gravity is (0, -9.81) m/s^2 by default.
"""

import math

import macgrid as mg

U_OFFSET = (0.0, 0.5)
V_OFFSET = (0.5, 0.0)


def weights(x, y, dx, ox, oy, na, nb):
    """The bilinear weights of the point (x, y) on a field of na by nb samples at ((a + ox) dx, (b + oy) dx).

    Returns four tuples (a, b, w, dw/dx, dw/dy). The weights are at least 0 and
    add up to 1. A point outside the samples is clamped as in macgrid.sample;
    the gradients are correct only for a point that is not clamped.
    """
    fx = min(max(x / dx - ox, 0.0), float(na - 1))
    fy = min(max(y / dx - oy, 0.0), float(nb - 1))
    a0 = min(int(math.floor(fx)), na - 2)
    b0 = min(int(math.floor(fy)), nb - 2)
    s = fx - a0
    t = fy - b0
    return ((a0, b0, (1.0 - s) * (1.0 - t), -(1.0 - t) / dx, -(1.0 - s) / dx),
            (a0, b0 + 1, (1.0 - s) * t, -t / dx, (1.0 - s) / dx),
            (a0 + 1, b0, s * (1.0 - t), (1.0 - t) / dx, -s / dx),
            (a0 + 1, b0 + 1, s * t, t / dx, s / dx))


def u_weights(g, x, y):
    return weights(x, y, g.dx, U_OFFSET[0], U_OFFSET[1], g.nx + 1, g.ny)


def v_weights(g, x, y):
    return weights(x, y, g.dx, V_OFFSET[0], V_OFFSET[1], g.nx, g.ny + 1)


def label_cells(g, xs, ys):
    """Mark each cell that holds a particle FLUID and each other cell that is not SOLID AIR."""
    for i in range(g.nx):
        for j in range(g.ny):
            if g.label[i][j] != mg.SOLID:
                g.label[i][j] = mg.AIR
    for x, y in zip(xs, ys):
        i = min(max(int(x / g.dx), 0), g.nx - 1)
        j = min(max(int(y / g.dx), 0), g.ny - 1)
        if g.label[i][j] != mg.SOLID:
            g.label[i][j] = mg.FLUID


def p2g(g, xs, ys, us, vs, ms):
    """Set each face velocity to the mass-weighted mean of the particle velocities.

    u_f = sum_p w_fp m_p u_p / sum_p w_fp m_p, and the same for v. A face with no
    mass gets 0. Returns the face masses (mu, mv).
    """
    mu = mg.zeros(g.nx + 1, g.ny)
    mv = mg.zeros(g.nx, g.ny + 1)
    pu = mg.zeros(g.nx + 1, g.ny)
    pv = mg.zeros(g.nx, g.ny + 1)
    for x, y, u, v, m in zip(xs, ys, us, vs, ms):
        for a, b, w, _, _ in u_weights(g, x, y):
            mu[a][b] += w * m
            pu[a][b] += w * m * u
        for a, b, w, _, _ in v_weights(g, x, y):
            mv[a][b] += w * m
            pv[a][b] += w * m * v
    g.u = [[pu[a][b] / mu[a][b] if mu[a][b] > 0.0 else 0.0 for b in range(g.ny)] for a in range(g.nx + 1)]
    g.v = [[pv[a][b] / mv[a][b] if mv[a][b] > 0.0 else 0.0 for b in range(g.ny + 1)] for a in range(g.nx)]
    return mu, mv


def add_gravity(g, mv, dt, gravity):
    """Add dt * gravity to each v face that has mass."""
    for a in range(g.nx):
        for b in range(g.ny + 1):
            if mv[a][b] > 0.0:
                g.v[a][b] += dt * gravity


def g2p(g, xs, ys):
    """The grid velocity at each particle, with the weights of p2g."""
    us, vs = [], []
    for x, y in zip(xs, ys):
        us.append(sum(w * g.u[a][b] for a, b, w, _, _ in u_weights(g, x, y)))
        vs.append(sum(w * g.v[a][b] for a, b, w, _, _ in v_weights(g, x, y)))
    return us, vs


def advect_particles(g, xs, ys, dt):
    """Move each particle for time dt through the grid velocity (RK2), and keep it half a cell from the walls."""
    lo = 0.5 * g.dx
    hx = g.nx * g.dx - lo
    hy = g.ny * g.dx - lo
    nxs, nys = [], []
    for x, y in zip(xs, ys):
        x1, y1 = mg.backtrace(g, x, y, -dt)
        nxs.append(min(max(x1, lo), hx))
        nys.append(min(max(y1, lo), hy))
    return nxs, nys


def step(g, xs, ys, us, vs, ms, dt, rho=1000.0, gravity=-9.81):
    """One PIC step. Changes the grid g and returns the new (xs, ys, us, vs)."""
    label_cells(g, xs, ys)  # @line L1
    mu, mv = p2g(g, xs, ys, us, vs, ms)  # @line L2
    add_gravity(g, mv, dt, gravity)  # @line L3
    mg.project(g, dt, rho)  # @line L4
    us, vs = g2p(g, xs, ys)  # @line L5
    xs, ys = advect_particles(g, xs, ys, dt)  # @line L6
    return xs, ys, us, vs


def seed_block(rng, i_cells, j_cells, dx, jitter=0.2):
    """Four particles per cell in the cells [0, i_cells) x [0, j_cells), each moved at random by up to jitter * dx / 2."""
    xs, ys = [], []
    for i in range(i_cells):
        for j in range(j_cells):
            for a in (0.25, 0.75):
                for b in (0.25, 0.75):
                    xs.append((i + a + rng.uniform(-0.5, 0.5) * jitter) * dx)
                    ys.append((j + b + rng.uniform(-0.5, 0.5) * jitter) * dx)
    return xs, ys


def particle_kinetic_energy(us, vs, ms):
    return 0.5 * sum(m * (u * u + v * v) for u, v, m in zip(us, vs, ms))


def grid_kinetic_energy(g, mu, mv):
    """(1/2) sum of m_f u_f^2 over the faces, with the face masses of p2g."""
    s = sum(mu[a][b] * g.u[a][b] ** 2 for a in range(g.nx + 1) for b in range(g.ny))
    s += sum(mv[a][b] * g.v[a][b] ** 2 for a in range(g.nx) for b in range(g.ny + 1))
    return 0.5 * s


def particle_momentum(us, vs, ms):
    return (sum(m * u for u, m in zip(us, ms)), sum(m * v for v, m in zip(vs, ms)))


def grid_momentum(g, mu, mv):
    return (sum(mu[a][b] * g.u[a][b] for a in range(g.nx + 1) for b in range(g.ny)),
            sum(mv[a][b] * g.v[a][b] for a in range(g.nx) for b in range(g.ny + 1)))
