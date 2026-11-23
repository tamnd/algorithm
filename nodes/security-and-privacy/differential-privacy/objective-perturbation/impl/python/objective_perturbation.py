# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/objective-perturbation/. The authors are listed in prov/HFPG7H.jsonl.
"""Objective perturbation for regularized logistic regression (Chaudhuri, Monteleoni and Sarwate, Algorithm 2).

The regularized empirical risk is

    J(f, D) = (1/n) sum_i ln(1 + exp(-y_i f.x_i)) + (Lambda/2) |f|^2,

with |x_i| <= 1 and y_i in {-1, +1}. The logistic loss l(z) = ln(1 + e^(-z))
has |l'| <= 1 and 0 < l'' <= c = 1/4. The algorithm draws a noise vector b
with density proportional to exp(-beta |b|) and returns the minimizer of

    J(f, D) + (1/n) b.f + (Delta/2) |f|^2,

which is epsilon-DP under replace neighbors.

The minimizer is found by gradient descent, so it is exact only up to the
tolerance. Floats and random.Random are used for the noise, so this code shows
the algorithm and is not a safe deployment.
"""

from __future__ import annotations

import math
import random
from typing import Sequence

Vector = list[float]
Example = tuple[Sequence[float], int]

C_LOGISTIC = 0.25  # the bound on the second derivative of the logistic loss


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


def perturbed_objective(f: Sequence[float], data: Sequence[Example], lam: float, b: Sequence[float], extra: float) -> float:
    """J(f, D) + (1/n) b.f + (extra/2) |f|^2, the objective of line L5."""
    return risk(f, data, lam) + dot(b, f) / len(data) + extra / 2 * dot(f, f)


def perturbed_gradient(f: Sequence[float], data: Sequence[Example], lam: float, b: Sequence[float], extra: float) -> Vector:
    """The gradient of the objective of line L5."""
    n = len(data)
    return [g + bi / n + extra * fi for g, bi, fi in zip(risk_gradient(f, data, lam), b, f)]


def minimize_perturbed(data: Sequence[Example], lam: float, b: Sequence[float], extra: float,
                       tol: float = 1e-11, max_steps: int = 200000) -> Vector:
    """The minimizer of the objective of line L5 by gradient descent with step 1/(1/4 + lam + extra).

    The objective is (lam + extra)-strongly convex and (1/4 + lam + extra)-smooth
    when |x_i| <= 1, so the iteration converges linearly. It stops when the
    gradient norm is at most tol. Cost: O(n d) per iteration.
    """
    f = [0.0] * len(b)
    step = 1 / (C_LOGISTIC + lam + extra)
    for _ in range(max_steps):
        g = perturbed_gradient(f, data, lam, b, extra)
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


def privacy_parameters(n: int, lam: float, epsilon: float, c: float = C_LOGISTIC) -> tuple[float, float]:
    """The pair (epsilon', Delta) of lines L1 to L3. Cost: O(1)."""
    eps_prime = epsilon - math.log(1 + 2 * c / (n * lam) + c * c / (n * n * lam * lam))  # @line L1
    if eps_prime > 0:
        extra = 0.0  # @line L2
    else:
        extra = c / (n * (math.exp(epsilon / 4) - 1)) - lam  # @line L3
        eps_prime = epsilon / 2
    return eps_prime, extra


def objective_perturbation(data: Sequence[Example], lam: float, epsilon: float, rng: random.Random) -> Vector:
    """An epsilon-DP model for regularized logistic regression (replace neighbors).

    Precondition: n >= 1, |x_i| <= 1, y_i in {-1, +1}, lam > 0, epsilon > 0.
    Cost: O(n d) per iteration of the minimizer plus O(d) for the noise.
    """
    if lam <= 0 or epsilon <= 0:
        raise ValueError("need lam > 0 and epsilon > 0")
    if not data or any(norm(x) > 1 + 1e-12 or y not in (-1, 1) for x, y in data):
        raise ValueError("need n >= 1, |x| <= 1 and y in {-1, +1}")
    n, d = len(data), len(data[0][0])
    eps_prime, extra = privacy_parameters(n, lam, epsilon)
    b = sample_noise(d, eps_prime / 2, rng)  # @line L4
    f_priv = minimize_perturbed(data, lam, b, extra)  # @line L5
    return f_priv  # @line L6


def noise_of(f: Sequence[float], data: Sequence[Example], lam: float, extra: float) -> Vector:
    """The unique b for which f minimizes the objective of line L5: b = -n (grad J(f) + extra f)."""
    n = len(data)
    return [-n * (g + extra * fi) for g, fi in zip(risk_gradient(f, data, lam), f)]


def jacobian_matrix(f: Sequence[float], data: Sequence[Example], lam: float, extra: float) -> list[Vector]:
    """A(f) = sum_i l''(y_i f.x_i) x_i x_i^T + n (lam + extra) I, minus the Jacobian of noise_of."""
    n, d = len(data), len(f)
    a = [[n * (lam + extra) if i == j else 0.0 for j in range(d)] for i in range(d)]
    for x, y in data:
        s = _sigmoid(y * dot(f, x))
        w = s * (1 - s)
        for i in range(d):
            for j in range(d):
                a[i][j] += w * x[i] * x[j]
    return a


def log_det(a: Sequence[Sequence[float]]) -> float:
    """ln det a for a symmetric positive definite matrix, by Gaussian elimination. Cost: O(d^3)."""
    m = [list(row) for row in a]
    d = len(m)
    total = 0.0
    for k in range(d):
        p = max(range(k, d), key=lambda i: abs(m[i][k]))
        m[k], m[p] = m[p], m[k]
        pivot = m[k][k]
        if pivot <= 0:
            raise ValueError("matrix is not positive definite")
        total += math.log(pivot)
        for i in range(k + 1, d):
            r = m[i][k] / pivot
            for j in range(k, d):
                m[i][j] -= r * m[k][j]
    return total


def output_log_density(f: Sequence[float], data: Sequence[Example], lam: float, epsilon: float) -> float:
    """The log density of the output of objective_perturbation at f, normalizer included.

    By the change of variables b = noise_of(f), the density is
    nu(noise_of(f)) det A(f), with nu(b) = exp(-beta |b|) / Z.
    """
    n, d = len(data), len(f)
    eps_prime, extra = privacy_parameters(n, lam, epsilon)
    beta = eps_prime / 2
    log_z = math.log(2) + d / 2 * math.log(math.pi) + math.lgamma(d) - math.lgamma(d / 2) - d * math.log(beta)
    b = noise_of(f, data, lam, extra)
    return -beta * norm(b) - log_z + log_det(jacobian_matrix(f, data, lam, extra))
