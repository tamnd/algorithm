# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dp-sgd/. The authors are listed in prov/X5S7AN.jsonl.
"""Differentially private stochastic gradient descent (Abadi et al., CCS 2016).

Each step samples a batch by Poisson sampling with rate q, computes the
gradient of each example in the batch, clips each gradient to the L2 norm C,
sums the clipped gradients, adds Gaussian noise with standard deviation
sigma * C in each coordinate, and takes a step. The privacy cost of T steps is
computed with the Renyi divergence of the sampled Gaussian mechanism at
integer orders (Mironov, Talwar and Zhang 2019), converted to (epsilon, delta).

The model here is logistic regression with labels in {-1, +1}, so that the
code needs no library. Floats and random.Random are used for the sampling
and the noise, so this code shows the algorithm and is not a safe deployment:
a deployment needs a cryptographic source of randomness and an exact sampler.
The neighbor relation is add/remove of one example.
"""

from __future__ import annotations

import math
import random
from typing import Sequence

Vector = list[float]
Example = tuple[Sequence[float], int]


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(a: Sequence[float]) -> float:
    return math.sqrt(dot(a, a))


def logistic_loss(theta: Sequence[float], x: Sequence[float], y: int) -> float:
    """ln(1 + exp(-y theta.x)), computed without overflow."""
    z = -y * dot(theta, x)
    return z + math.log1p(math.exp(-z)) if z > 0 else math.log1p(math.exp(z))


def logistic_gradient(theta: Sequence[float], x: Sequence[float], y: int) -> Vector:
    """The gradient of the logistic loss in theta: -y x / (1 + exp(y theta.x))."""
    m = y * dot(theta, x)
    s = math.exp(-m) / (1 + math.exp(-m)) if m >= 0 else 1 / (1 + math.exp(m))
    return [-y * s * xi for xi in x]


def clip(g: Sequence[float], c: float) -> Vector:
    """g / max(1, |g| / c): the vector itself if its norm is at most c, else scaled to norm c."""
    scale = max(1.0, norm(g) / c)
    return [gi / scale for gi in g]


def dp_sgd(data: Sequence[Example], q: float, sigma: float, c: float, eta: float, steps: int, rng: random.Random) -> Vector:
    """Train logistic regression with DP-SGD and return the last parameter vector.

    Precondition: 0 < q <= 1, sigma > 0, c > 0, eta > 0 and all x of the same
    dimension d. The output is (epsilon, delta)-DP under add/remove with the
    epsilon of epsilon_for(q, sigma, steps, delta). Cost: O(T n d) time for
    T steps over n examples, and O(d) extra space.
    """
    if not (0 < q <= 1 and sigma > 0 and c > 0 and eta > 0):
        raise ValueError("need 0 < q <= 1 and positive sigma, c and eta")
    n = len(data)
    d = len(data[0][0])
    theta = [0.0] * d  # @line L1
    for _ in range(steps):  # @line L2
        total = [0.0] * d
        for x, y in data:
            if rng.random() < q:  # @line L3
                g = logistic_gradient(theta, x, y)  # @line L4
                gc = clip(g, c)  # @line L5
                total = [a + b for a, b in zip(total, gc)]
        noisy = [a + rng.gauss(0.0, sigma * c) for a in total]  # @line L6
        theta = [t - eta * gi / (q * n) for t, gi in zip(theta, noisy)]  # @line L7
    return theta  # @line L8


def _log_add(a: float, b: float) -> float:
    if a == -math.inf:
        return b
    if b == -math.inf:
        return a
    m = max(a, b)
    return m + math.log(math.exp(a - m) + math.exp(b - m))


def log_a(q: float, sigma: float, alpha: int) -> float:
    """ln A_alpha with A_alpha = sum_k C(alpha, k) (1 - q)^(alpha - k) q^k exp((k^2 - k) / (2 sigma^2)).

    A_alpha is E[(mu(z) / mu0(z))^alpha] for mu0 = N(0, sigma^2) and
    mu = (1 - q) mu0 + q N(1, sigma^2). Precondition: alpha >= 2 is an integer.
    """
    if alpha < 2 or int(alpha) != alpha:
        raise ValueError("alpha must be an integer at least 2")
    if q == 1:
        return alpha * (alpha - 1) / (2 * sigma ** 2)
    total = -math.inf
    for k in range(alpha + 1):
        term = math.lgamma(alpha + 1) - math.lgamma(k + 1) - math.lgamma(alpha - k + 1)
        term += k * math.log(q) + (alpha - k) * math.log1p(-q)
        term += (k * k - k) / (2 * sigma ** 2)
        total = _log_add(total, term)
    return total


def rdp_sampled_gaussian(q: float, sigma: float, alpha: int) -> float:
    """The Renyi DP of one step at order alpha: ln(A_alpha) / (alpha - 1).

    It is a bound for Poisson sampling with add/remove neighbors (Mironov,
    Talwar and Zhang, Theorem 5 shows that A_alpha is the larger of the two
    directions). Cost: O(alpha).
    """
    return log_a(q, sigma, alpha) / (alpha - 1)


def epsilon_for(q: float, sigma: float, steps: int, delta: float, orders: Sequence[int] = tuple(range(2, 257))) -> tuple[float, int]:
    """(epsilon, alpha): the smallest T rdp(alpha) + ln(1/delta) / (alpha - 1) over the orders.

    This converts Renyi DP to (epsilon, delta)-DP (Mironov 2017) after T steps
    of composition. Precondition: 0 < delta < 1. Cost: O(sum of the orders).
    """
    if not 0 < delta < 1:
        raise ValueError("need 0 < delta < 1")
    best = (math.inf, orders[0])
    for a in orders:
        eps = steps * rdp_sampled_gaussian(q, sigma, a) + math.log(1 / delta) / (a - 1)
        if eps < best[0]:
            best = (eps, a)
    return best
