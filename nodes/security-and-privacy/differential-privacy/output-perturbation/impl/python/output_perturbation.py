# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/output-perturbation/. The authors are listed in prov/DE6SYB.jsonl.
"""Output perturbation for regularized logistic regression (Chaudhuri, Monteleoni and Sarwate, Algorithm 1).

The regularized empirical risk is

    J(f, D) = (1/n) sum_i ln(1 + exp(-y_i f.x_i)) + (Lambda/2) |f|^2,

with |x_i| <= 1 and y_i in {-1, +1}. Its minimizer moves by at most 2/(n Lambda)
in L2 norm when one example is replaced. The algorithm releases the minimizer
plus a noise vector b with density proportional to exp(-beta |b|), with
beta = n Lambda epsilon / 2, which is epsilon-DP under replace neighbors.

The minimizer is found by gradient descent with the step 1/(1/4 + Lambda), so
it is exact only up to the tolerance. Floats and random.Random are used for
the noise, so this code shows the algorithm and is not a safe deployment.
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


def _sigmoid(z: float) -> float:
    if z >= 0:
        return 1 / (1 + math.exp(-z))
    e = math.exp(z)
    return e / (1 + e)


def risk(f: Sequence[float], data: Sequence[Example], lam: float) -> float:
    """J(f, D): the mean logistic loss plus (lam/2) |f|^2."""
    total = 0.0
    for x, y in data:
        z = -y * dot(f, x)
        total += z + math.log1p(math.exp(-z)) if z > 0 else math.log1p(math.exp(z))
    return total / len(data) + lam / 2 * dot(f, f)


def risk_gradient(f: Sequence[float], data: Sequence[Example], lam: float) -> Vector:
    """The gradient of J: (1/n) sum_i -y_i x_i sigmoid(-y_i f.x_i) + lam f."""
    n = len(data)
    g = [lam * fi for fi in f]
    for x, y in data:
        s = _sigmoid(-y * dot(f, x))
        for j, xj in enumerate(x):
            g[j] -= y * xj * s / n
    return g


def minimize_risk(data: Sequence[Example], lam: float, tol: float = 1e-11, max_steps: int = 100000) -> Vector:
    """The minimizer of J by gradient descent with step 1/(1/4 + lam).

    J is lam-strongly convex and (1/4 + lam)-smooth when |x_i| <= 1, so the
    iteration converges linearly. It stops when |grad J| <= tol, which puts the
    iterate within tol/lam of the minimizer. Cost: O(n d) per iteration.
    """
    d = len(data[0][0])
    f = [0.0] * d
    step = 1 / (0.25 + lam)
    for _ in range(max_steps):
        g = risk_gradient(f, data, lam)
        if norm(g) <= tol:
            return f
        f = [fi - step * gi for fi, gi in zip(f, g)]
    return f


def sample_noise(d: int, beta: float, rng: random.Random) -> Vector:
    """A vector b in R^d with density proportional to exp(-beta |b|).

    The norm |b| has the Gamma(d, 1/beta) law, the sum of d Exp(beta) draws,
    and the direction is uniform on the sphere. Cost: O(d) draws.
    """
    r = sum(rng.expovariate(beta) for _ in range(d))
    while True:
        u = [rng.gauss(0.0, 1.0) for _ in range(d)]
        s = norm(u)
        if s > 0:
            return [r * ui / s for ui in u]


def output_perturbation(data: Sequence[Example], lam: float, epsilon: float, rng: random.Random) -> Vector:
    """An epsilon-DP model for regularized logistic regression (replace neighbors).

    Precondition: n >= 1, |x_i| <= 1, y_i in {-1, +1}, lam > 0, epsilon > 0.
    Cost: O(n d) per iteration of the minimizer plus O(d) for the noise.
    """
    if lam <= 0 or epsilon <= 0:
        raise ValueError("need lam > 0 and epsilon > 0")
    if any(norm(x) > 1 + 1e-12 or y not in (-1, 1) for x, y in data):
        raise ValueError("need |x| <= 1 and y in {-1, +1}")
    n = len(data)
    f_star = minimize_risk(data, lam)  # @line L1
    beta = n * lam * epsilon / 2  # @line L2
    b = sample_noise(len(f_star), beta, rng)  # @line L3
    return [fi + bi for fi, bi in zip(f_star, b)]  # @line L4


def sensitivity_bound(n: int, lam: float) -> float:
    """2 / (n lam), the L2 sensitivity of the minimizer under replace (CMS Corollary 8)."""
    return 2 / (n * lam)


def output_log_density(z: Sequence[float], center: Sequence[float], beta: float) -> float:
    """The log density of the output at z, given the minimizer center; the normalizer is included."""
    d = len(z)
    # The normalizer of exp(-beta |b|) in R^d is 2 pi^(d/2) Gamma(d) / (Gamma(d/2) beta^d).
    log_norm = math.log(2) + d / 2 * math.log(math.pi) + math.lgamma(d) - math.lgamma(d / 2) - d * math.log(beta)
    return -beta * norm([a - b for a, b in zip(z, center)]) - log_norm
