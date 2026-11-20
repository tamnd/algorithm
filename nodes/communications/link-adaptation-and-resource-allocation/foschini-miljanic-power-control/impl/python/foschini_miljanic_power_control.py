# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/foschini-miljanic-power-control/. The authors are listed in prov/K8XR5H.jsonl.

"""Foschini-Miljanic distributed power control.

There are K links. G[i][j] >= 0 is the power gain from transmitter j to
receiver i, so G[i][i] > 0 is the gain of link i. Receiver i has the noise
power noise[i] > 0, and link i wants the SINR target gamma[i] > 0. With the
powers p, receiver i measures

    SINR_i = G[i][i] p[i] / (sum over j != i of G[i][j] p[j] + noise[i]).

Each link sets p_i <- (1 - beta) p_i + beta (gamma_i / SINR_i) p_i, which is
p_i <- (1 - beta) p_i + beta gamma_i I_i / G[i][i] with I_i the interference
plus noise that receiver i measures. In matrix form this is
p <- (1 - beta) p + beta (F p + u) with F[i][j] = gamma_i G[i][j] / G[i][i]
for j != i, F[i][i] = 0, and u[i] = gamma_i noise[i] / G[i][i]. The iteration
converges from every start, for every beta in (0, 1], exactly when the
spectral radius of F is below 1, and then its limit is the smallest power
vector that meets all the targets.
"""

import random


def normalized_gain(g: list[list[float]], gamma: list[float], noise: list[float]) -> tuple[list[list[float]], list[float]]:
    """F[i][j] = gamma_i G[i][j] / G[i][i] (j != i, F[i][i] = 0) and u[i] = gamma_i noise_i / G[i][i]."""
    k = len(g)
    f = [[0.0 if i == j else gamma[i] * g[i][j] / g[i][i] for j in range(k)] for i in range(k)]
    u = [gamma[i] * noise[i] / g[i][i] for i in range(k)]
    return f, u


def interference(g: list[list[float]], noise: list[float], p: list[float], i: int) -> float:
    """The interference plus noise at receiver i: sum over j != i of G[i][j] p[j], plus noise[i]."""
    return sum(g[i][j] * p[j] for j in range(len(p)) if j != i) + noise[i]


def sinr(g: list[list[float]], noise: list[float], p: list[float]) -> list[float]:
    """The SINR of each link for the powers p."""
    return [g[i][i] * p[i] / interference(g, noise, p, i) for i in range(len(p))]


def foschini_miljanic(
    g: list[list[float]],
    gamma: list[float],
    noise: list[float],
    p0: list[float],
    beta: float = 1.0,
    iters: int = 1000,
    tol: float = 1e-12,
) -> tuple[list[float], int]:
    """Run the synchronous iteration from p0. Return the powers and the number of steps done."""
    if not 0.0 < beta <= 1.0:
        raise ValueError("beta must be in (0, 1]")
    p = list(p0)
    k = len(p)
    for t in range(iters):  # @line L1
        q = [0.0] * k
        for i in range(k):  # @line L2
            meas = interference(g, noise, p, i)  # @line L3
            q[i] = (1.0 - beta) * p[i] + beta * gamma[i] * meas / g[i][i]  # @line L4
        change = max(abs(a - b) for a, b in zip(q, p))
        p = q
        if change <= tol * max(p):  # @line L5
            return p, t + 1
    return p, iters  # @line L6


def foschini_miljanic_async(
    g: list[list[float]],
    gamma: list[float],
    noise: list[float],
    p0: list[float],
    rng: random.Random,
    updates: int,
) -> list[float]:
    """Asynchronous form: at each step one link, chosen at random, applies line L4 with beta = 1."""
    p = list(p0)
    k = len(p)
    for _ in range(updates):
        i = rng.randrange(k)
        p[i] = gamma[i] * interference(g, noise, p, i) / g[i][i]
    return p


def solve_linear(a: list[list[float]], b: list[float]) -> list[float] | None:
    """Solve a x = b by Gaussian elimination with partial pivoting; None if a is singular."""
    n = len(a)
    m = [list(map(float, row)) + [float(b[i])] for i, row in enumerate(a)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[piv][c]) < 1e-300:
            return None
        m[c], m[piv] = m[piv], m[c]
        for r in range(c + 1, n):
            fac = m[r][c] / m[c][c]
            if fac:
                for k in range(c, n + 1):
                    m[r][k] -= fac * m[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))) / m[r][r]
    return x


def target_powers(g: list[list[float]], gamma: list[float], noise: list[float]) -> list[float] | None:
    """The fixed point p* = (I - F)^(-1) u if the targets are feasible, else None.

    For u > 0, a positive solution of (I - F) p = u exists exactly when the
    spectral radius of F is below 1, so this is also the feasibility test.
    """
    f, u = normalized_gain(g, gamma, noise)
    k = len(u)
    a = [[(1.0 if i == j else 0.0) - f[i][j] for j in range(k)] for i in range(k)]
    p = solve_linear(a, u)
    if p is None or min(p) <= 0.0:
        return None
    return p


def spectral_radius(f: list[list[float]], iters: int = 5000) -> float:
    """The spectral radius of a nonnegative irreducible matrix F, by power iteration on I + F.

    I + F is primitive when F is irreducible, and rho(I + F) = 1 + rho(F).
    """
    k = len(f)
    x = [1.0] * k
    lam = 0.0
    for _ in range(iters):
        y = [x[i] + sum(f[i][j] * x[j] for j in range(k)) for i in range(k)]
        s = max(y)
        y = [v / s for v in y]
        if max(abs(a - b) for a, b in zip(x, y)) < 1e-15:
            x, lam = y, s
            break
        x, lam = y, s
    return lam - 1.0
