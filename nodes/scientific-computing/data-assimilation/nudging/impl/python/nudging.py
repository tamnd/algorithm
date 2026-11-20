# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nudging/. The authors are listed in prov/A44WD4.jsonl.

"""Nudging (Newtonian relaxation) of a model toward observations.

The model dx/dt = f(x) gets a relaxation term:

    dx/dt = f(x) + G (y^o(t) - H x),

where H (p by n) maps the state to the observed quantities, y^o(t) gives the
observations at any time t (usually by interpolation in time between
observation times), and G (n by p) is the nudging gain. The common choice
G = g H^T relaxes each observed component with the time scale 1/g.

The nudged equation is integrated with the classical Runge-Kutta method.
The module also holds the Lorenz-96 tendency for the tests and the page.
"""


def lorenz96(F):
    """Return the Lorenz-96 tendency f(x)_j = (x_{j+1} - x_{j-2}) x_{j-1} - x_j + F."""

    def f(x):
        n = len(x)
        return [(x[(j + 1) % n] - x[j - 2]) * x[j - 1] - x[j] + F for j in range(n)]

    return f


def rk4_step(q, t, x, dt):
    """Return one classical Runge-Kutta step of dx/dt = q(t, x)."""
    k1 = q(t, x)
    k2 = q(t + dt / 2, [a + dt / 2 * b for a, b in zip(x, k1)])
    k3 = q(t + dt / 2, [a + dt / 2 * b for a, b in zip(x, k2)])
    k4 = q(t + dt, [a + dt * b for a, b in zip(x, k3)])
    return [a + dt / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(x, k1, k2, k3, k4)]


def nudge(f, x0, H, G, yobs, dt, m, t0=0.0):
    """Return the nudged trajectory [x_0, x_1, ..., x_m] at t_k = t0 + k dt.

    f(x) is the model tendency, H a p by n matrix, G an n by p matrix and
    yobs(t) the list of p observed values at time t. With G = 0 this is
    the free model run.
    """
    n, p = len(x0), len(H)
    # Keep only the nonzero entries: H and G are usually very sparse.
    Hs = [[(j, H[k][j]) for j in range(n) if H[k][j] != 0] for k in range(p)]
    Gs = [[(k, G[i][k]) for k in range(p) if G[i][k] != 0] for i in range(n)]
    x = [float(v) for v in x0]  # @line L1
    path = [list(x)]

    def q(t, z):  # @line L3
        y = yobs(t)
        r = [y[k] - sum(h * z[j] for j, h in Hs[k]) for k in range(p)]
        fz = f(z)
        return [fz[i] + sum(gik * r[k] for k, gik in Gs[i]) for i in range(n)]

    for k in range(m):  # @line L2
        x = rk4_step(q, t0 + k * dt, x, dt)  # @line L4
        path.append(x)
    return path  # @line L5


def gain(H, g):
    """Return G = g H^T, which relaxes each observed quantity with the rate g."""
    return [[g * H[k][i] for k in range(len(H))] for i in range(len(H[0]))]


def time_interpolant(times, values):
    """Return y(t), linear in t between the given times and constant outside them.

    times must be equally spaced and increasing.
    """
    t0, step, last = times[0], times[1] - times[0], len(times) - 1

    def y(t):
        s = (t - t0) / step
        if s <= 0:
            return list(values[0])
        if s >= last:
            return list(values[last])
        k = int(s)
        a = s - k
        return [(1 - a) * u + a * v for u, v in zip(values[k], values[k + 1])]

    return y
