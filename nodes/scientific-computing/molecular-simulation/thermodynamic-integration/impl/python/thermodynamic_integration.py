# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thermodynamic-integration/. The authors are listed in prov/G0H3ZS.jsonl.
"""Thermodynamic integration (Kirkwood 1935).

A family of potentials U_lambda, lambda in [0, 1], joins state 0 to state 1.
The derivative of the free energy along the path is a canonical average,

    dA / dlambda = < dU_lambda / dlambda >_lambda,

so A_1 - A_0 is the integral of this average over [0, 1]. The method samples a
few values of lambda, takes the mean of dU/dlambda at each one, and applies a
quadrature rule. The result has two errors: the statistical error of the
means and the quadrature error of the rule.

The sampler is an input. A Metropolis sampler and the batch-means error for
its correlated samples are included for the tests.

Cost: (number of nodes) times (samples per node) evaluations of dU/dlambda,
plus the cost of the sampler.
"""

import math
from typing import Callable, Sequence


def trapezoid_rule(k: int) -> tuple[list[float], list[float]]:
    """Nodes and weights of the composite trapezoid rule with k intervals on [0, 1]."""
    if k < 1:
        raise ValueError("need k >= 1")
    nodes = [i / k for i in range(k + 1)]
    weights = [1.0 / k] * (k + 1)
    weights[0] = weights[-1] = 0.5 / k
    return nodes, weights


def simpson_rule(k: int) -> tuple[list[float], list[float]]:
    """Nodes and weights of the composite Simpson rule with k (even) intervals on [0, 1]."""
    if k < 2 or k % 2:
        raise ValueError("need an even k >= 2")
    nodes = [i / k for i in range(k + 1)]
    weights = [(4 if i % 2 else 2) / (3 * k) for i in range(k + 1)]
    weights[0] = weights[-1] = 1 / (3 * k)
    return nodes, weights


def _legendre(n: int, x: float) -> tuple[float, float]:
    """P_n(x) and its derivative, by the three-term recurrence."""
    p_prev, p = 1.0, x
    for j in range(2, n + 1):
        p_prev, p = p, ((2 * j - 1) * x * p - (j - 1) * p_prev) / j
    return p, n * (x * p - p_prev) / (x * x - 1)


def gauss_legendre_rule(n: int) -> tuple[list[float], list[float]]:
    """Nodes and weights of the n-point Gauss-Legendre rule, mapped to [0, 1]."""
    if n < 1:
        raise ValueError("need n >= 1")
    pts = []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p, dp = _legendre(n, x)
            dx = p / dp
            x -= dx
            if abs(dx) < 1e-15:
                break
        _, dp = _legendre(n, x)
        # weight 2 / ((1 - x^2) P_n'(x)^2) on [-1, 1], halved for [0, 1]
        pts.append((0.5 * (1 - x), 1.0 / ((1 - x * x) * dp * dp)))
    pts.sort()
    return [p[0] for p in pts], [p[1] for p in pts]


def mean_and_error(values: Sequence[float], batches: int = 1) -> tuple[float, float]:
    """Mean and standard error. With batches > 1, the error uses batch means
    (for correlated samples); with batches = 1, it assumes independent samples."""
    n = len(values)
    mean = sum(values) / n
    if batches <= 1:
        var = sum((v - mean) ** 2 for v in values) / (n - 1)
        return mean, math.sqrt(var / n)
    b = n // batches
    means = [sum(values[i * b:(i + 1) * b]) / b for i in range(batches)]
    m = sum(means) / batches
    var = sum((x - m) ** 2 for x in means) / (batches - 1)
    return mean, math.sqrt(var / batches)


def thermodynamic_integration(nodes: Sequence[float], weights: Sequence[float],
                              sample: Callable, dudl: Callable, n: int, rng,
                              batches: int = 1) -> tuple[float, float, list[float]]:
    """A_1 - A_0 by quadrature of the mean of dU/dlambda.

    sample(lam, n, rng) returns n configurations of the state lam (independent
    or a correlated chain), dudl(lam, x) is dU_lam / dlam at x. Returns the
    estimate, its statistical standard error and the means at the nodes.
    """
    total, var, means = 0.0, 0.0, []                     # @line L1
    for lam, w in zip(nodes, weights):                   # @line L2
        xs = sample(lam, n, rng)                         # @line L3
        g, s = mean_and_error([dudl(lam, x) for x in xs], batches)  # @line L4
        total += w * g                                   # @line L5
        var += (w * s) ** 2                              # @line L5
        means.append(g)
    return total, math.sqrt(var), means                  # @line L6


def metropolis(u: Callable, beta: float, x0: float, step: float, n: int,
               rng, burn: int = 1000) -> list[float]:
    """A random walk Metropolis chain in one dimension for the density exp(-beta u)."""
    x, ux = x0, u(x0)
    out = []
    for i in range(burn + n):
        y = x + step * (2 * rng.random() - 1)
        uy = u(y)
        if uy <= ux or rng.random() < math.exp(-beta * (uy - ux)):
            x, ux = y, uy
        if i >= burn:
            out.append(x)
    return out
