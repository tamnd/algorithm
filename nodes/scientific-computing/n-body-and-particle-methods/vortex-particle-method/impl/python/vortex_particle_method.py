# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vortex-particle-method/. The authors are listed in prov/4WPAHS.jsonl.
"""The 2D vortex blob method for the incompressible Euler equations.

Particle p sits at (x_p, y_p) and carries the circulation g_p. The vorticity
is the sum of Gaussian blobs of core size delta,

    omega(x) = sum_p g_p zeta(x - x_p),   zeta(x) = exp(-|x|^2 / delta^2) / (pi delta^2),

and the Biot-Savart law gives the velocity with the smoothed kernel

    K(x, y) = (-y, x) (1 - exp(-r^2 / delta^2)) / (2 pi r^2),   r^2 = x^2 + y^2.

The particles move with this velocity (explicit midpoint rule) and keep their
circulations, since vorticity is carried by an inviscid 2D flow.

Cost: Theta(N^2) time per velocity evaluation by direct summation.
"""

import math


def kernel(dx: float, dy: float, delta: float) -> tuple[float, float]:
    """The blob kernel K_delta(dx, dy); K(0, 0) = (0, 0)."""
    r2 = dx * dx + dy * dy
    if r2 == 0.0:
        return 0.0, 0.0
    s = -math.expm1(-r2 / (delta * delta)) / (2 * math.pi * r2)
    return -dy * s, dx * s


def velocity_at(x: float, y: float, xs: list[float], ys: list[float], gs: list[float], delta: float):
    """The velocity of the blob field at the point (x, y)."""
    u = v = 0.0
    for xq, yq, g in zip(xs, ys, gs):
        ku, kv = kernel(x - xq, y - yq, delta)
        u += g * ku
        v += g * kv
    return u, v


def velocities(xs: list[float], ys: list[float], gs: list[float], delta: float):
    """u_p = sum_q g_q K(x_p - x_q) for every particle, by direct summation over the pairs."""
    n = len(xs)
    us, vs = [0.0] * n, [0.0] * n
    for p in range(n):  # @line L1
        for q in range(p + 1, n):  # @line L2
            ku, kv = kernel(xs[p] - xs[q], ys[p] - ys[q], delta)  # @line L2
            us[p] += gs[q] * ku  # @line L2
            vs[p] += gs[q] * kv  # @line L2
            us[q] -= gs[p] * ku  # @line L2
            vs[q] -= gs[p] * kv  # @line L2
    return us, vs


def vortex_step(xs: list[float], ys: list[float], gs: list[float], delta: float, h: float):
    """One explicit midpoint step of dx_p/dt = u(x_p); the circulations do not change."""
    us, vs = velocities(xs, ys, gs, delta)
    xm = [x + 0.5 * h * u for x, u in zip(xs, us)]  # @line L3
    ym = [y + 0.5 * h * v for y, v in zip(ys, vs)]  # @line L3
    us, vs = velocities(xm, ym, gs, delta)  # @line L4
    xs = [x + h * u for x, u in zip(xs, us)]  # @line L5
    ys = [y + h * v for y, v in zip(ys, vs)]  # @line L5
    return xs, ys  # @line L6


def lamb_oseen_vorticity(r: float, gamma: float, nu: float, t: float) -> float:
    """omega = gamma / (4 pi nu t) exp(-r^2 / (4 nu t))."""
    return gamma / (4 * math.pi * nu * t) * math.exp(-r * r / (4 * nu * t))


def lamb_oseen_speed(r: float, gamma: float, nu: float, t: float) -> float:
    """The azimuthal velocity gamma / (2 pi r) (1 - exp(-r^2 / (4 nu t)))."""
    return -gamma * math.expm1(-r * r / (4 * nu * t)) / (2 * math.pi * r)


def lattice_particles(omega, spacing: float, radius: float):
    """Particles on a square lattice inside the disc of the given radius, with g_p = omega(r_p) spacing^2."""
    xs, ys, gs = [], [], []
    k = int(radius / spacing)
    for i in range(-k, k + 1):
        for j in range(-k, k + 1):
            x, y = i * spacing, j * spacing
            if x * x + y * y <= radius * radius:
                xs.append(x)
                ys.append(y)
                gs.append(omega(math.hypot(x, y)) * spacing * spacing)
    return xs, ys, gs
