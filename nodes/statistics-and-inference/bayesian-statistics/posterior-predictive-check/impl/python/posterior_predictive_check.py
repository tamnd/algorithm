# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/posterior-predictive-check/. The authors are listed in prov/2TJBEH.jsonl.
"""Posterior predictive checks (Rubin 1984; Gelman, Meng and Stern 1996).

ppc draws one replicated data set for each posterior draw and returns the posterior
predictive p-value P(T(x_rep, theta) >= T(x, theta) | x), with the pairs of values for a
plot. The closed forms below give the exact p-value and its law under the model for the
normal mean with a normal prior, where the p-values pile up near 1/2.
"""

import math
import random
from statistics import NormalDist
from typing import Callable, Sequence

_N = NormalDist()


def ppc(
    x,
    draws: Sequence,
    simulate: Callable,
    T: Callable,
    rng: random.Random,
) -> tuple[float, list[tuple[float, float]]]:
    """The template: returns (p-value, [(T(x_rep, theta_s), T(x, theta_s)) for each s])."""
    count = 0  # @line L1
    pairs = []
    for theta in draws:  # @line L2
        x_rep = simulate(theta, rng)  # @line L3
        t_rep, t_obs = T(x_rep, theta), T(x, theta)
        if t_rep >= t_obs:  # @line L4
            count += 1
        pairs.append((t_rep, t_obs))
    return count / len(draws), pairs  # @line L5


# Normal mean: x_1..x_n ~ N(theta, sigma^2), sigma known, theta ~ N(0, tau^2).

def normal_posterior(xbar: float, n: int, sigma: float, tau: float) -> tuple[float, float]:
    v = 1.0 / (n / sigma**2 + 1.0 / tau**2)
    return v * n * xbar / sigma**2, v


def ppp_mean(xbar: float, n: int, sigma: float, tau: float) -> float:
    """Exact posterior predictive p-value of T = the sample mean: P(xbar_rep >= xbar | x)."""
    m, v = normal_posterior(xbar, n, sigma, tau)
    return 1.0 - _N.cdf((xbar - m) / math.sqrt(v + sigma**2 / n))


def pileup_factor(n: int, sigma: float, tau: float) -> float:
    """c with p = Phi(-c Z), Z standard normal, when the data come from the model."""
    s2 = sigma**2 / n
    return math.sqrt(s2 / (2 * tau**2 + s2))


def ppp_mean_tail(alpha: float, c: float) -> float:
    """P(p <= alpha) for p = Phi(-c Z): Phi(z_alpha / c)."""
    return _N.cdf(_N.inv_cdf(alpha) / c)


def ppp_mean_variance(c: float) -> float:
    """Var(p) for p = Phi(-c Z): arcsin(c^2 / (1 + c^2)) / (2 pi); 1/12 when c = 1."""
    return math.asin(c * c / (1 + c * c)) / (2 * math.pi)


def chi2_sf_even(x: float, k: int) -> float:
    """P(chi^2_k >= x) for even k."""
    h = x / 2
    term, total = 1.0, 1.0
    for j in range(1, k // 2):
        term *= h / j
        total += term
    return math.exp(-h) * total


def ppp_variance_known_sigma(xs: Sequence[float], sigma: float) -> float:
    """p-value of T = the sample variance when sigma is known. T is ancillary, so its
    posterior predictive law is its sampling law, (sigma^2 / (n - 1)) chi^2_{n-1}.
    Requires n - 1 even."""
    n = len(xs)
    if (n - 1) % 2:
        raise ValueError("n - 1 must be even for the closed form")
    m = sum(xs) / n
    s2 = sum((v - m) ** 2 for v in xs) / (n - 1)
    return chi2_sf_even((n - 1) * s2 / sigma**2, n - 1)


# Counts: x_i ~ Poisson(lambda), lambda ~ Gamma(a, rate b); posterior Gamma(a + sum x, b + n).

def poisson(lam: float, rng: random.Random) -> int:
    if lam > 30:
        # sum of independent Poisson parts keeps the product method stable
        k = int(lam // 30)
        return sum(poisson(lam / (k + 1), rng) for _ in range(k + 1))
    k, prod, lim = 0, rng.random(), math.exp(-lam)
    while prod > lim:
        k += 1
        prod *= rng.random()
    return k


def dispersion(xs: Sequence[int], _theta=None) -> float:
    """Sample variance over sample mean; about 1 for Poisson data."""
    n = len(xs)
    m = sum(xs) / n
    if m == 0:
        return 0.0
    return sum((v - m) ** 2 for v in xs) / (n - 1) / m


def poisson_gamma_check(xs: Sequence[int], a: float, b: float, n_draws: int, rng: random.Random, T=dispersion) -> float:
    n, s = len(xs), sum(xs)
    draws = [rng.gammavariate(a + s, 1.0 / (b + n)) for _ in range(n_draws)]
    p, _ = ppc(xs, draws, lambda lam, r: [poisson(lam, r) for _ in range(n)], T, rng)
    return p
