# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-estimation/. The authors are listed in prov/8RHNEA.jsonl.

"""Maximum likelihood estimation.

Closed forms for the Bernoulli, Poisson and Gaussian models, a Newton
solver for a one-parameter exponential family (the MLE solves
A'(eta) = mean of T(x), so it matches moments), the Neyman-Scott
estimator, and the log-likelihood of a Gaussian mixture, whose supremum
is infinite.
"""

import math
from fractions import Fraction
from itertools import product
from typing import Callable, Dict, List, Sequence, Tuple


def bernoulli_mle(xs: Sequence[int]) -> Fraction:
    return Fraction(sum(xs), len(xs))


def poisson_mle(xs: Sequence[int]) -> Fraction:
    return Fraction(sum(xs), len(xs))


def gaussian_mle(xs: Sequence) -> Tuple[object, object]:
    """(mean, variance) that maximize the Gaussian likelihood; the variance divides by n."""
    n = len(xs)
    mu = sum(xs) / Fraction(n) if isinstance(xs[0], (int, Fraction)) else sum(xs) / n
    var = sum((x - mu) ** 2 for x in xs) / n
    return mu, var


def gaussian_loglik(xs: Sequence[float], mu: float, var: float) -> float:
    return sum(-0.5 * math.log(2 * math.pi * var) - (x - mu) ** 2 / (2 * var) for x in xs)


def exp_family_mle_1d(t_mean: float, dA: Callable[[float], float], d2A: Callable[[float], float], eta0: float = 0.0, iters: int = 100) -> float:
    """Natural parameter MLE of a one-parameter exponential family.

    The log-likelihood is n (eta * t_mean - A(eta)) + const, which is
    concave; its stationary point solves A'(eta) = t_mean. Newton's
    method on the score.
    """
    eta = eta0
    for _ in range(iters):
        step = (dA(eta) - t_mean) / d2A(eta)
        eta -= step
        if abs(step) < 1e-14:
            break
    return eta


def neyman_scott_mle(groups: Sequence[Sequence]) -> Tuple[List, object]:
    """MLE in x_ij ~ N(mu_i, s2), i = 1..k strata, j = 1..m.

    mu_i hat is the stratum mean and s2 hat = (1/(k m)) sum_ij (x_ij - mu_i hat)^2.
    """
    mus = [sum(g) / Fraction(len(g)) if isinstance(g[0], (int, Fraction)) else sum(g) / len(g) for g in groups]
    total = sum(len(g) for g in groups)
    s2 = sum((x - mu) ** 2 for g, mu in zip(groups, mus) for x in g) / total
    return mus, s2


def neyman_scott_expected_s2(noise: Dict[Fraction, Fraction], means: Sequence[Fraction], m: int) -> Fraction:
    """E[s2 hat] by full enumeration of the noise, x_ij = means[i] + e_ij.

    noise maps each noise value to its probability; the e_ij are i.i.d.
    """
    vals = list(noise.items())
    k = len(means)
    expect = Fraction(0)
    for combo in product(vals, repeat=k * m):
        p = Fraction(1)
        for _, q in combo:
            p *= q
        groups = [[means[i] + combo[i * m + j][0] for j in range(m)] for i in range(k)]
        expect += p * neyman_scott_mle(groups)[1]
    return expect


def mixture_loglik(xs: Sequence[float], weights: Sequence[float], mus: Sequence[float], sds: Sequence[float]) -> float:
    total = 0.0
    for x in xs:
        dens = sum(w * math.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi)) for w, m, s in zip(weights, mus, sds))
        total += math.log(dens)
    return total
