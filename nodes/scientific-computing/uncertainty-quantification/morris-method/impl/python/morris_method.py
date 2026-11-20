# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morris-method/. The authors are listed in prov/2Q63VY.jsonl.
"""The Morris method of elementary effects (Morris 1991), with mu* of Campolongo, Cariboni and Saltelli 2007.

The inputs are scaled to the unit cube [0, 1]^d and take values on a grid of
p levels {0, 1/(p-1), ..., 1}, with p even. The step is Delta = p / (2 (p - 1)).
One trajectory has d + 1 points. It starts at a random grid point, and each
next point moves one coordinate by +Delta or -Delta, each coordinate once, in
a random order. The elementary effect of input i on the trajectory is

    EE_i = (f(x after the move of i) - f(x before)) / (signed step of i).

With r trajectories, the method returns for each input the mean mu, the mean
of the absolute values mu*, and the standard deviation sigma of its r
elementary effects, at r (d + 1) model runs. These are screening measures,
not estimates with an error bound.
"""

import math
import random
from typing import Callable, Sequence

Model = Callable[[Sequence[float]], float]


def trajectory(d: int, p: int, rng: random.Random) -> tuple[list[list[float]], list[int]]:
    """One Morris trajectory: the d + 1 points and the order in which the coordinates move."""
    if p % 2 or p < 2:
        raise ValueError("p must be even and at least 2")
    delta = p / (2 * (p - 1))
    # base values x*_i in {0, 1/(p-1), ..., 1 - Delta}, so that x*_i + Delta is on the grid
    base = [rng.randrange(p // 2) / (p - 1) for _ in range(d)]  # @line L2
    up = [rng.random() < 0.5 for _ in range(d)]  # @line L3
    x = [base[i] if up[i] else base[i] + delta for i in range(d)]
    order = list(range(d))
    rng.shuffle(order)  # @line L4
    points = [list(x)]
    for i in order:  # @line L5
        x[i] = x[i] + delta if up[i] else x[i] - delta
        points.append(list(x))
    return points, order


def morris(f: Model, d: int, r: int, p: int, rng: random.Random) -> dict:
    """mu, mu* and sigma of the elementary effects of each input from r trajectories."""
    effects: list[list[float]] = [[] for _ in range(d)]
    runs = 0
    for _ in range(r):  # @line L1
        points, order = trajectory(d, p, rng)
        y = [f(pt) for pt in points]  # @line L6
        runs += len(points)
        for k, i in enumerate(order):  # @line L7
            step = points[k + 1][i] - points[k][i]
            effects[i].append((y[k + 1] - y[k]) / step)
    mu = [sum(e) / r for e in effects]  # @line L8
    mu_star = [sum(abs(v) for v in e) / r for e in effects]
    sigma = [math.sqrt(sum((v - m) ** 2 for v in e) / (r - 1)) if r > 1 else 0.0 for e, m in zip(effects, mu)]
    return {"mu": mu, "mu_star": mu_star, "sigma": sigma, "effects": effects, "runs": runs}  # @line L9


def grid_effects(f: Model, d: int, p: int, i: int) -> list[float]:
    """All elementary effects of input i over the full grid: pairs x, x + Delta e_i with both on the grid.

    For p even, each elementary effect of a random trajectory is a uniform draw from this list.
    """
    delta = p / (2 * (p - 1))
    levels = [k / (p - 1) for k in range(p)]
    low = [v for v in levels if v + delta <= 1 + 1e-12]
    out = []
    idx = [0] * d
    sizes = [len(low) if k == i else p for k in range(d)]
    while True:
        x = [low[idx[k]] if k == i else levels[idx[k]] for k in range(d)]
        xp = list(x)
        xp[i] += delta
        out.append((f(xp) - f(x)) / delta)
        k = 0
        while k < d:
            idx[k] += 1
            if idx[k] < sizes[k]:
                break
            idx[k] = 0
            k += 1
        if k == d:
            return out
