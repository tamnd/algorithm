# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affine-particle-in-cell/. The authors are listed in prov/AJQ8H2.jsonl.
"""The affine particle-in-cell method (APIC) for a liquid on a 2D MAC grid.

Each particle carries its velocity (u_p, v_p) and the gradients c^u_p and c^v_p
of the two velocity components, so it carries an affine velocity field. The
transfers are

    P2G: u_f = sum_p w_fp m_p (u_p + c^u_p . (x_f - x_p)) / sum_p w_fp m_p,
    G2P: u_p = sum_f w_fp u_f,  c^u_p = sum_f grad w_fp u_f,

and the same for v. For bilinear weights, the gradient form of G2P equals
B_p D_p^-1 of Jiang et al. (2015), with D_p diagonal and the entries
s (1 - s) dx^2 and t (1 - t) dx^2, where (s, t) are the fractional positions of
the particle in the stencil of the component.

The weights are bilinear, with the same clamping as macgrid.sample; the
gradients and the angular momentum claim need a particle that is not clamped,
which advect_particles ensures. The grid must have nx >= 2 and ny >= 2.
Gravity is (0, -9.81) m/s^2 by default.
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


def u_face(g, a, b):
    """The position of the u face (a, b)."""
    return (a * g.dx, (b + 0.5) * g.dx)


def v_face(g, a, b):
    """The position of the v face (a, b)."""
    return ((a + 0.5) * g.dx, b * g.dx)


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


def p2g(g, xs, ys, us, vs, cus, cvs, ms):
    """The APIC particle to grid transfer. Returns the face masses (mu, mv).

    cus[p] and cvs[p] are the gradients (d/dx, d/dy) of u and v on particle p.
    With all gradients 0 this is the PIC transfer.
    """
    mu = mg.zeros(g.nx + 1, g.ny)
    mv = mg.zeros(g.nx, g.ny + 1)
    pu = mg.zeros(g.nx + 1, g.ny)
    pv = mg.zeros(g.nx, g.ny + 1)
    for x, y, u, v, cu, cv, m in zip(xs, ys, us, vs, cus, cvs, ms):
        for a, b, w, _, _ in u_weights(g, x, y):
            fx, fy = u_face(g, a, b)
            mu[a][b] += w * m
            pu[a][b] += w * m * (u + cu[0] * (fx - x) + cu[1] * (fy - y))
        for a, b, w, _, _ in v_weights(g, x, y):
            fx, fy = v_face(g, a, b)
            mv[a][b] += w * m
            pv[a][b] += w * m * (v + cv[0] * (fx - x) + cv[1] * (fy - y))
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
    """The APIC grid to particle transfer. Returns (us, vs, cus, cvs)."""
    us, vs, cus, cvs = [], [], [], []
    for x, y in zip(xs, ys):
        u = cux = cuy = 0.0
        for a, b, w, wx, wy in u_weights(g, x, y):
            q = g.u[a][b]
            u += w * q
            cux += wx * q
            cuy += wy * q
        v = cvx = cvy = 0.0
        for a, b, w, wx, wy in v_weights(g, x, y):
            q = g.v[a][b]
            v += w * q
            cvx += wx * q
            cvy += wy * q
        us.append(u)
        vs.append(v)
        cus.append((cux, cuy))
        cvs.append((cvx, cvy))
    return us, vs, cus, cvs


def inertia_diagonals(g, x, y):
    """(D^u_yy, D^v_xx) of particle (x, y): sum_f w_fp (y_f - y)^2 on the u faces and sum_f w_fp (x_f - x)^2 on the v faces."""
    duy = sum(w * (u_face(g, a, b)[1] - y) ** 2 for a, b, w, _, _ in u_weights(g, x, y))
    dvx = sum(w * (v_face(g, a, b)[0] - x) ** 2 for a, b, w, _, _ in v_weights(g, x, y))
    return duy, dvx


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


def step(g, xs, ys, us, vs, cus, cvs, ms, dt, rho=1000.0, gravity=-9.81):
    """One APIC step. Changes the grid g and returns the new (xs, ys, us, vs, cus, cvs)."""
    label_cells(g, xs, ys)  # @line L1
    mu, mv = p2g(g, xs, ys, us, vs, cus, cvs, ms)  # @line L2
    add_gravity(g, mv, dt, gravity)  # @line L3
    mg.project(g, dt, rho)  # @line L4
    us, vs, cus, cvs = g2p(g, xs, ys)  # @line L5
    xs, ys = advect_particles(g, xs, ys, dt)  # @line L6
    return xs, ys, us, vs, cus, cvs


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


def particle_momentum(us, vs, ms):
    return (sum(m * u for u, m in zip(us, ms)), sum(m * v for v, m in zip(vs, ms)))


def grid_momentum(g, mu, mv):
    return (sum(mu[a][b] * g.u[a][b] for a in range(g.nx + 1) for b in range(g.ny)),
            sum(mv[a][b] * g.v[a][b] for a in range(g.nx) for b in range(g.ny + 1)))


def particle_angular_momentum(g, xs, ys, us, vs, cus, cvs, ms):
    """sum_p m_p (x_p v_p - y_p u_p + c^v_x D^v_xx - c^u_y D^u_yy), about the origin."""
    total = 0.0
    for x, y, u, v, cu, cv, m in zip(xs, ys, us, vs, cus, cvs, ms):
        duy, dvx = inertia_diagonals(g, x, y)
        total += m * (x * v - y * u + cv[0] * dvx - cu[1] * duy)
    return total


def grid_angular_momentum(g, mu, mv):
    """sum over the v faces of m_f x_f v_f minus the sum over the u faces of m_f y_f u_f."""
    total = 0.0
    for a in range(g.nx):
        for b in range(g.ny + 1):
            total += mv[a][b] * v_face(g, a, b)[0] * g.v[a][b]
    for a in range(g.nx + 1):
        for b in range(g.ny):
            total -= mu[a][b] * u_face(g, a, b)[1] * g.u[a][b]
    return total
