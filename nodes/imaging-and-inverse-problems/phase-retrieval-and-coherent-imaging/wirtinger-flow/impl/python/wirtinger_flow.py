# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wirtinger-flow/. The authors are listed in prov/E17F69.jsonl.

"""Wirtinger flow for phase retrieval (Candes, Li and Soltanolkotabi 2015).

The data are y_r = |a_r^H x|^2 for known a_r in C^n (lists of numbers). The
loss is

    f(z) = (1 / (2 m)) sum_r (|a_r^H z|^2 - y_r)^2,

and its Wirtinger gradient (the derivative with respect to conj(z)) is

    g(z) = (1 / m) sum_r (|a_r^H z|^2 - y_r) a_r (a_r^H z).

For a real direction t and any d, d/dt f(z + t d) at t = 0 is 2 Re <g(z), d>.
The method starts from the spectral estimate z_0 and takes the steps
z <- z - (mu_tau / ||z_0||^2) g(z) with mu_tau = min(1 - exp(-tau / tau0), mu_max);
the values tau0 = 330 and mu_max = 0.4 are those the authors report for
their simulations. The convergence theorem is for a constant step mu <= c1 / n
and Gaussian a_r; the schedule is a tuned choice.
"""

import math
import random


def gaussian_design(rng, m, n):
    """m sampling vectors with entries N(0, 1/2) + i N(0, 1/2)."""
    s = math.sqrt(0.5)
    return [[complex(rng.gauss(0.0, s), rng.gauss(0.0, s)) for _ in range(n)] for _ in range(m)]


def inner(a, v):
    """<a, v> = a^H v = sum conj(a_i) v_i."""
    return sum(complex(u).conjugate() * w for u, w in zip(a, v))


def norm(v):
    """The Euclidean norm."""
    return math.sqrt(sum(abs(w) ** 2 for w in v))


def measure(a_rows, x):
    """The phaseless data y_r = |a_r^H x|^2."""
    return [abs(inner(a, x)) ** 2 for a in a_rows]


def loss(a_rows, y, z):
    """f(z) = (1 / (2 m)) sum_r (|a_r^H z|^2 - y_r)^2."""
    return sum((abs(inner(a, z)) ** 2 - yr) ** 2 for a, yr in zip(a_rows, y)) / (2.0 * len(y))


def wirtinger_gradient(a_rows, y, z):
    """g(z) = (1 / m) sum_r (|a_r^H z|^2 - y_r) a_r (a_r^H z)."""
    out = [0j] * len(z)
    for a, yr in zip(a_rows, y):
        p = inner(a, z)
        c = (abs(p) ** 2 - yr) * p
        for i, ai in enumerate(a):
            out[i] += c * ai
    m = len(y)
    return [w / m for w in out]


def spectral_start(a_rows, y, iters=100, seed=0):
    """The spectral estimate: lambda times the top eigenvector of (1/m) sum y_r a_r a_r^H."""
    n, m = len(a_rows[0]), len(y)
    lam = math.sqrt(n * sum(y) / sum(norm(a) ** 2 for a in a_rows))
    rng = random.Random(seed)
    v = [complex(rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)) for _ in range(n)]
    for _ in range(iters):
        w = [0j] * n
        for a, yr in zip(a_rows, y):
            c = yr * inner(a, v) / m
            for i, ai in enumerate(a):
                w[i] += c * ai
        s = norm(w)
        v = [u / s for u in w]
    return [lam * u for u in v]


def step_size(tau, tau0=330.0, mu_max=0.4):
    """mu_tau = min(1 - exp(-tau / tau0), mu_max)."""
    return min(1.0 - math.exp(-tau / tau0), mu_max)


def wirtinger_flow(a_rows, y, iters, z0=None, tau0=330.0, mu_max=0.4, record=None):
    """Run Wirtinger flow. Returns z. If record is a list, z_0 .. z_iters are appended to it."""
    z = list(spectral_start(a_rows, y) if z0 is None else z0)  # @line L1
    scale = norm(z) ** 2  # @line L2
    if record is not None:
        record.append(z)
    for tau in range(1, iters + 1):  # @line L3
        mu = step_size(tau, tau0, mu_max)  # @line L4
        g = wirtinger_gradient(a_rows, y, z)  # @line L5
        z = [u - (mu / scale) * v for u, v in zip(z, g)]  # @line L6
        if record is not None:
            record.append(z)
    return z  # @line L7


def dist(z, x):
    """min over phi of ||z - e^{i phi} x||, reached at the phase of x^H z."""
    c = inner(x, z)
    phase = c / abs(c) if abs(c) > 0.0 else 1.0
    return norm([u - phase * v for u, v in zip(z, x)])
