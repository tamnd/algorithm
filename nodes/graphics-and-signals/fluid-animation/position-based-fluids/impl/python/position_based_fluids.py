# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/position-based-fluids/. The authors are listed in prov/XH6YNA.jsonl.
"""Position based fluids (PBF) in 2D, after Macklin and Mueller (2013).

The density constraint of particle i is C_i = rho_i / rho0 - 1 with
rho_i = sum_j m W_poly6(x_i - x_j). Each solver pass computes

    lambda_i = -C_i / (sum_k |grad_k C_i|^2 + eps),
    dx_i = (m / rho0) sum_j (lambda_i + lambda_j + s_corr_ij) grad W_spiky(x_i - x_j),
    s_corr_ij = -k (W_poly6(x_i - x_j) / W_poly6(dq))^n,

and moves the predicted positions by dx. Both kernels have support h. All
particles have the same mass m. The 2D kernels are

    W_poly6(r) = 4 / (pi h^8) (h^2 - r^2)^3,  W_spiky(r) = 10 / (pi h^5) (h - r)^3.

The values of eps, k and the XSPH weight c are tuning constants; the defaults
here are scaled by the denominator D0 of a particle in a full lattice.
"""

import math

from sph import neighbor_pairs

GRAVITY = (0.0, -9.81)
POLY6_2D = 4.0 / math.pi  # times 1 / h^8
SPIKY_2D = 10.0 / math.pi  # times 1 / h^5


def w_poly6(r2, h):
    """W_poly6 as a function of r^2, support h."""
    if r2 >= h * h:
        return 0.0
    return POLY6_2D / h ** 8 * (h * h - r2) ** 3


def w_spiky(r, h):
    if r >= h:
        return 0.0
    return SPIKY_2D / h ** 5 * (h - r) ** 3


def grad_spiky(dx, dy, h):
    """Gradient of W_spiky(|x|) at x = (dx, dy); (0, 0) at x = 0."""
    r = math.hypot(dx, dy)
    if r == 0.0 or r >= h:
        return (0.0, 0.0)
    s = -3.0 * SPIKY_2D / h ** 5 * (h - r) ** 2 / r
    return (s * dx, s * dy)


def densities(pos, pairs, m, h):
    rho = [m * w_poly6(0.0, h)] * len(pos)
    for i, j in pairs:
        w = m * w_poly6((pos[i][0] - pos[j][0]) ** 2 + (pos[i][1] - pos[j][1]) ** 2, h)
        rho[i] += w
        rho[j] += w
    return rho


def full_lattice_denominator(dx, h, m, rho0):
    """D0 = sum_k |grad_k C_i|^2 for a particle in a full square lattice of spacing dx."""
    s = 0.0
    n = int(h / dx) + 1
    for a in range(-n, n + 1):
        for b in range(-n, n + 1):
            g = grad_spiky(a * dx, b * dx, h)
            s += g[0] * g[0] + g[1] * g[1]
    return (m / rho0) ** 2 * s


def lambdas(pos, pairs, m, h, rho0, eps, one_sided=False):
    """lambda_i = -C_i / (sum_k |grad_k C_i|^2 + eps). Returns (lambda, C)."""
    n = len(pos)
    rho = densities(pos, pairs, m, h)
    c = [r / rho0 - 1.0 for r in rho]  # @line L4
    if one_sided:
        c = [max(t, 0.0) for t in c]
    gx = [0.0] * n
    gy = [0.0] * n
    sq = [0.0] * n
    f = m / rho0
    for i, j in pairs:
        g = grad_spiky(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1], h)
        gx[i] += f * g[0]
        gy[i] += f * g[1]
        gx[j] -= f * g[0]
        gy[j] -= f * g[1]
        g2 = f * f * (g[0] * g[0] + g[1] * g[1])
        sq[i] += g2
        sq[j] += g2
    lam = [-c[i] / (gx[i] ** 2 + gy[i] ** 2 + sq[i] + eps) for i in range(n)]  # @line L5
    return lam, c


def corrections(pos, pairs, lam, m, h, rho0, k=0.0, dq=0.2, power=4):
    """dx_i = (m / rho0) sum_j (lambda_i + lambda_j + s_corr_ij) grad W_spiky(x_i - x_j)."""
    n = len(pos)
    out_x = [0.0] * n
    out_y = [0.0] * n
    f = m / rho0
    w_dq = w_poly6((dq * h) ** 2, h)
    for i, j in pairs:
        ddx = pos[i][0] - pos[j][0]
        ddy = pos[i][1] - pos[j][1]
        s = lam[i] + lam[j]
        if k != 0.0:
            s -= k * (w_poly6(ddx * ddx + ddy * ddy, h) / w_dq) ** power
        g = grad_spiky(ddx, ddy, h)
        out_x[i] += f * s * g[0]
        out_y[i] += f * s * g[1]
        out_x[j] -= f * s * g[0]
        out_y[j] -= f * s * g[1]
    return list(zip(out_x, out_y))


def clamp_box(pos, box):
    x0, y0, x1, y1 = box
    return [(min(max(x, x0), x1), min(max(y, y0), y1)) for x, y in pos]


def xsph(pos, vel, pairs, m, h, rho0, c):
    """v_i <- v_i + c sum_j (m / rho0) (v_j - v_i) W_poly6(x_i - x_j)."""
    vx = [v[0] for v in vel]
    vy = [v[1] for v in vel]
    f = c * m / rho0
    for i, j in pairs:
        w = f * w_poly6((pos[i][0] - pos[j][0]) ** 2 + (pos[i][1] - pos[j][1]) ** 2, h)
        du = vel[j][0] - vel[i][0]
        dv = vel[j][1] - vel[i][1]
        vx[i] += w * du
        vy[i] += w * dv
        vx[j] -= w * du
        vy[j] -= w * dv
    return list(zip(vx, vy))


def step(pos, vel, m, dt, h, rho0, eps, iterations=4, k=0.0, dq=0.2, power=4, c_xsph=0.01,
         gravity=GRAVITY, box=None, one_sided=False):
    """One PBF step. Returns (pos, vel, constraint errors C of each pass before its correction)."""
    n = len(pos)
    vel = [(v[0] + dt * gravity[0], v[1] + dt * gravity[1]) for v in vel]  # @line L1
    pred = [(pos[i][0] + dt * vel[i][0], pos[i][1] + dt * vel[i][1]) for i in range(n)]
    if box is not None:
        pred = clamp_box(pred, box)
    pairs = neighbor_pairs(pred, h)  # @line L2
    history = []
    for _ in range(iterations):  # @line L3
        lam, c = lambdas(pred, pairs, m, h, rho0, eps, one_sided)
        history.append(c)
        dp = corrections(pred, pairs, lam, m, h, rho0, k, dq, power)  # @line L6
        pred = [(pred[i][0] + dp[i][0], pred[i][1] + dp[i][1]) for i in range(n)]  # @line L7
        if box is not None:
            pred = clamp_box(pred, box)
    vel = [((pred[i][0] - pos[i][0]) / dt, (pred[i][1] - pos[i][1]) / dt) for i in range(n)]  # @line L8
    if c_xsph != 0.0:
        vel = xsph(pred, vel, pairs, m, h, rho0, c_xsph)  # @line L9
    return pred, vel, history  # @line L10


def momentum(vel, m):
    return (m * sum(v[0] for v in vel), m * sum(v[1] for v in vel))


def mean_abs(c):
    return sum(abs(t) for t in c) / len(c)


def mean_positive(c):
    return sum(max(t, 0.0) for t in c) / len(c)
