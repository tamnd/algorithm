# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weakly-compressible-sph/. The authors are listed in prov/XB7CYE.jsonl.
"""Weakly compressible SPH (WCSPH) in 2D with the Tait equation of state.

One step (Monaghan 1994; Becker and Teschner 2007):
1. find the neighbor pairs at a distance below 2h,
2. rho_i = sum_j m_j W_ij (j = i included),
3. p_i = B ((rho_i / rho0)^gamma - 1) with B = rho0 c^2 / gamma,
4. a_i = g - sum_j m_j (p_i / rho_i^2 + p_j / rho_j^2 + Pi_ij) grad W_ij,
   with the artificial viscosity Pi_ij of Monaghan,
5. symplectic Euler: v += dt a, then x += dt v.

The kernel, the neighbor search and the density come from the shared helper
sph.py. Each pair force is applied with opposite signs to i and j, so the
internal forces conserve linear and angular momentum.
"""

import math

from sph import density, grad_w, neighbor_pairs

GRAVITY = (0.0, -9.81)


def tait_b(rho0, c, gamma=7.0):
    """The stiffness B = rho0 c^2 / gamma of the Tait equation (Pa)."""
    return rho0 * c * c / gamma


def tait_pressure(rho, rho0, c, gamma=7.0, clamp=False):
    """p = B ((rho / rho0)^gamma - 1). With clamp, a negative p is set to 0."""
    p = tait_b(rho0, c, gamma) * ((rho / rho0) ** gamma - 1.0)
    if clamp and p < 0.0:
        return 0.0
    return p


def time_step_limit(h, c, v_max, lam=0.4):
    """The CFL type limit dt <= lam h / (c + v_max) (a heuristic, lam about 0.4)."""
    return lam * h / (c + v_max)


def accelerations(pos, vel, masses, h, rho0, c, gravity=GRAVITY, alpha=0.0,
                  gamma=7.0, clamp=False):
    """Return (acc, rho, p) for the particles. Cost O(n + q) for q pairs."""
    n = len(pos)
    pairs = neighbor_pairs(pos, 2.0 * h)  # @line L1
    rho = density(pos, masses, h)  # @line L2
    p = [tait_pressure(r, rho0, c, gamma, clamp) for r in rho]  # @line L3
    ax = [gravity[0]] * n  # @line L4
    ay = [gravity[1]] * n
    eps = 0.01 * h * h
    for i, j in pairs:  # @line L5
        dx = pos[i][0] - pos[j][0]
        dy = pos[i][1] - pos[j][1]
        gx, gy = grad_w((dx, dy), h)
        s = p[i] / (rho[i] * rho[i]) + p[j] / (rho[j] * rho[j])  # @line L6
        if alpha > 0.0:
            vx = vel[i][0] - vel[j][0]
            vy = vel[i][1] - vel[j][1]
            vr = vx * dx + vy * dy
            if vr < 0.0:  # @line L7
                mu = h * vr / (dx * dx + dy * dy + eps)
                s += -alpha * c * mu / (0.5 * (rho[i] + rho[j]))
        ax[i] -= masses[j] * s * gx  # @line L8
        ay[i] -= masses[j] * s * gy
        ax[j] += masses[i] * s * gx
        ay[j] += masses[i] * s * gy
    return list(zip(ax, ay)), rho, p


def apply_box(pos, vel, box, restitution=0.0):
    """Clamp the particles into box = (x0, y0, x1, y1) and reflect the normal velocity.

    This is a simple wall model (a heuristic), not part of WCSPH itself.
    """
    x0, y0, x1, y1 = box
    out_p, out_v = [], []
    for (x, y), (u, v) in zip(pos, vel):
        if x < x0:
            x, u = x0, -restitution * u if u < 0.0 else u
        elif x > x1:
            x, u = x1, -restitution * u if u > 0.0 else u
        if y < y0:
            y, v = y0, -restitution * v if v < 0.0 else v
        elif y > y1:
            y, v = y1, -restitution * v if v > 0.0 else v
        out_p.append((x, y))
        out_v.append((u, v))
    return out_p, out_v


def step(pos, vel, masses, dt, h, rho0, c, gravity=GRAVITY, alpha=0.0,
         gamma=7.0, clamp=False, box=None):
    """Advance one step of WCSPH. Returns (pos, vel, rho) with rho at the start."""
    acc, rho, _ = accelerations(pos, vel, masses, h, rho0, c, gravity, alpha,
                                gamma, clamp)
    vel = [(v[0] + dt * a[0], v[1] + dt * a[1]) for v, a in zip(vel, acc)]  # @line L9
    pos = [(x[0] + dt * v[0], x[1] + dt * v[1]) for x, v in zip(pos, vel)]  # @line L10
    if box is not None:  # @line L11
        pos, vel = apply_box(pos, vel, box)
    return pos, vel, rho


def momentum(vel, masses):
    """The total linear momentum sum_i m_i v_i."""
    return (sum(m * v[0] for m, v in zip(masses, vel)),
            sum(m * v[1] for m, v in zip(masses, vel)))


def angular_momentum(pos, vel, masses):
    """The total angular momentum sum_i m_i (x_i v_i,y - y_i v_i,x) about the origin."""
    return sum(m * (x[0] * v[1] - x[1] * v[0]) for m, x, v in zip(masses, pos, vel))


def max_speed(vel):
    """The largest particle speed."""
    return max((math.hypot(v[0], v[1]) for v in vel), default=0.0)
