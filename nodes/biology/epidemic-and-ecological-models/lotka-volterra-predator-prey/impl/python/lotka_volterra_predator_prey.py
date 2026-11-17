# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lotka-volterra-predator-prey/. The authors are listed in prov/JXS149.jsonl.
"""The Lotka-Volterra predator-prey model.

    dx/dt = a x - b x y      (prey)
    dy/dt = c x y - d y      (predator)

All four parameters are positive. The equilibrium with both species is
(d / c, a / b), and V = c x - d ln x + b y - a ln y is constant on every
solution. The module integrates the model with fixed step RK4, measures
the period of an orbit and the time averages over one period, and has
the variant with logistic prey growth, which loses the closed orbits.
"""

import math


def field(x: float, y: float, a: float, b: float, c: float, d: float, k: float = math.inf):
    """The vector field; k is the prey carrying capacity (infinite in the classical model)."""
    return a * x * (1.0 - x / k) - b * x * y, c * x * y - d * y


def first_integral(x: float, y: float, a: float, b: float, c: float, d: float) -> float:
    """V(x, y) = c x - d ln x + b y - a ln y."""
    return c * x - d * math.log(x) + b * y - a * math.log(y)


def rk4_step(x: float, y: float, dt: float, p):
    """One classical Runge-Kutta step for the field with parameters p = (a, b, c, d) or (a, b, c, d, k)."""
    k1 = field(x, y, *p)  # @line L3
    k2 = field(x + dt * k1[0] / 2, y + dt * k1[1] / 2, *p)  # @line L4
    k3 = field(x + dt * k2[0] / 2, y + dt * k2[1] / 2, *p)  # @line L5
    k4 = field(x + dt * k3[0], y + dt * k3[1], *p)  # @line L6
    x = x + dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6  # @line L7
    y = y + dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6  # @line L7
    return x, y


def simulate(x0: float, y0: float, dt: float, steps: int, p):
    """The list of states at times 0, dt, ..., steps dt."""
    x, y = x0, y0  # @line L1
    out = [(x, y)]
    for _ in range(steps):  # @line L2
        x, y = rk4_step(x, y, dt, p)
        out.append((x, y))
    return out  # @line L8


def crossings(traj, level: float, dt: float):
    """Times at which y crosses `level` upward, by linear interpolation between steps."""
    times = []
    for i in range(len(traj) - 1):
        y0, y1 = traj[i][1], traj[i + 1][1]
        if y0 < level <= y1:
            times.append((i + (level - y0) / (y1 - y0)) * dt)
    return times


def period_and_means(x0: float, y0: float, dt: float, t_max: float, p):
    """The period of the orbit from (x0, y0), and the time averages of x and y over one period."""
    a, b, c, d = p[:4]
    traj = simulate(x0, y0, dt, int(round(t_max / dt)), p)
    ts = crossings(traj, a / b, dt)
    i0, i1 = int(math.ceil(ts[0] / dt)), int(math.floor(ts[1] / dt))
    # trapezoid rule on the grid points inside one period, plus the two end pieces
    seg = traj[i0:i1 + 1]
    sx = sum((seg[j][0] + seg[j + 1][0]) / 2 for j in range(len(seg) - 1)) * dt
    sy = sum((seg[j][1] + seg[j + 1][1]) / 2 for j in range(len(seg) - 1)) * dt
    span = (len(seg) - 1) * dt
    return ts[1] - ts[0], sx / span, sy / span


def small_orbit_period(a: float, d: float) -> float:
    """The period 2 pi / sqrt(a d) of the linearization at the equilibrium."""
    return 2 * math.pi / math.sqrt(a * d)
