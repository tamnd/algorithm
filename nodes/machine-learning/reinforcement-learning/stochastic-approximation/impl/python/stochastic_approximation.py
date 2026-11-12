# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-approximation/. The authors are listed in prov/TVB7PM.jsonl.

import math
import random
from typing import Callable, Sequence

Vector = list[float]


def stochastic_approximation(
    sample: Callable[[Vector, random.Random], Vector],
    x0: Sequence[float],
    step: Callable[[int], float],
    n_iter: int,
    rng: random.Random,
    project: Callable[[Vector], Vector] | None = None,
) -> list[Vector]:
    """Run x_(n+1) = P(x_n + a_n y_n), where y_n = sample(x_n) = h(x_n) + M_(n+1).

    sample returns one noisy observation of the mean field h at x. step(n) is a_n > 0.
    project is an optional map back into a bounded set (the identity when None).
    Returns the n_iter + 1 iterates x_0, ..., x_N. Cost: n_iter samples and O(n_iter d) arithmetic.
    """
    x = [float(v) for v in x0]  # @line L1
    out = [list(x)]
    for n in range(n_iter):  # @line L2
        y = sample(x, rng)  # @line L3
        x = [xi + step(n) * yi for xi, yi in zip(x, y)]  # @line L4
        if project is not None:
            x = project(x)
        out.append(list(x))
    return out  # @line L5


def ode_times(step: Callable[[int], float], n_iter: int) -> list[float]:
    """The ODE clock t_n = a_0 + ... + a_(n-1), with t_0 = 0."""
    t, out = 0.0, [0.0]
    for n in range(n_iter):
        t += step(n)
        out.append(t)
    return out


def linear_field(a: Sequence[Sequence[float]], b: Sequence[float]) -> Callable[[Vector], Vector]:
    """The mean field h(x) = b - A x."""
    return lambda x: [b[i] - sum(a[i][j] * x[j] for j in range(len(x))) for i in range(len(b))]


def gaussian_noise_sampler(h: Callable[[Vector], Vector], sigma: float) -> Callable[[Vector, random.Random], Vector]:
    """Observations h(x) + M with M a vector of independent N(0, sigma^2) entries (a martingale difference)."""
    return lambda x, rng: [v + rng.gauss(0.0, sigma) for v in h(x)]


def rotation_ode_solution(x_star: Sequence[float], x0: Sequence[float], t: float) -> Vector:
    """Exact solution of dx/dt = b - A x with A = [[1, 1], [-1, 1]] and root x_star.

    Since A = I + J with J^2 = -I, x(t) - x* = exp(-t) [[cos t, -sin t], [sin t, cos t]] (x0 - x*).
    """
    d0, d1 = x0[0] - x_star[0], x0[1] - x_star[1]
    e, c, s = math.exp(-t), math.cos(t), math.sin(t)
    return [x_star[0] + e * (c * d0 - s * d1), x_star[1] + e * (s * d0 + c * d1)]
