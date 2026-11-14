# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/empirical-bayes/. The authors are listed in prov/NGX20X.jsonl.
"""Empirical Bayes: estimate the prior from many parallel cases, then use the Bayes rule.

Three instances of the template on the page:

* robbins: Poisson counts, no model for the prior (f-modeling). The Bayes rule
  E[theta | x] = (x + 1) f(x + 1) / f(x) is estimated with the observed frequencies.
* gamma_poisson_fit and gamma_poisson_posterior_mean: Poisson counts with a gamma
  prior fitted by maximum marginal likelihood (g-modeling).
* normal_eb: normal means x_i ~ N(theta_i, s_i^2) with theta_i ~ N(mu, tau^2), where
  mu and tau^2 are fitted by maximum marginal likelihood (type II maximum likelihood).

tweedie_posterior_mean gives E[mu | z] = z + sigma^2 d/dz log f(z) for a normal mixture
f, and discrete_prior_posterior_mean computes the same posterior mean directly. Both are
used to check Tweedie's formula and Robbins's formula against the exact Bayes rule.
"""

import math
from typing import Sequence


def robbins(counts: Sequence[float]) -> list[float]:
    """Robbins's estimate of E[theta | x] for x = 0, ..., len(counts) - 2.

    counts[x] is the number (or frequency) of cases with value x. The estimate at x is
    (x + 1) counts[x + 1] / counts[x]; it is None where counts[x] is 0.
    """
    out = []
    for x in range(len(counts) - 1):
        out.append(None if counts[x] == 0 else (x + 1) * counts[x + 1] / counts[x])
    return out


def poisson_mixture_posterior_mean(x: int, atoms: Sequence, weights: Sequence):
    """Exact E[theta | x] when theta has the discrete prior P(theta = atoms[k]) = weights[k].

    Works with Fractions if the factor exp(-theta) is already folded into the weights:
    pass weights w_k = g_k exp(-theta_k), then the result is sum w theta^(x+1) / sum w theta^x.
    """
    num = sum(w * a ** (x + 1) for a, w in zip(atoms, weights))
    den = sum(w * a ** x for a, w in zip(atoms, weights))
    return num / den


def poisson_mixture_marginal(x: int, atoms: Sequence, weights: Sequence):
    """f(x) * x! for the same discrete prior: sum_k w_k theta_k^x (w_k includes exp(-theta_k))."""
    return sum(w * a ** x for a, w in zip(atoms, weights))


def _nb_loglik(counts: Sequence[float], nu: float, scale: float) -> float:
    """Log-likelihood of grouped counts under the negative binomial marginal of a
    Poisson law with a Gamma(shape nu, scale) prior."""
    p = scale / (1.0 + scale)
    total = 0.0
    for x, c in enumerate(counts):
        if c:
            total += c * (math.lgamma(x + nu) - math.lgamma(nu) - math.lgamma(x + 1)
                          + x * math.log(p) + nu * math.log1p(-p))
    return total


def _golden_max(f, lo: float, hi: float, tol: float = 1e-10) -> float:
    """Maximize a unimodal function on [lo, hi] by golden section search."""
    g = (math.sqrt(5.0) - 1.0) / 2.0
    a, b = lo, hi
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = f(c), f(d)
    while b - a > tol * (1.0 + abs(a) + abs(b)):
        if fc >= fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = f(d)
    return (a + b) / 2.0


def gamma_poisson_fit(counts: Sequence[float]) -> tuple[float, float]:
    """Maximum marginal likelihood (shape nu, scale) of a gamma prior for Poisson counts.

    For a fixed shape the likelihood is maximized at scale = mean / nu, because the
    maximum likelihood estimate of a negative binomial mean is the sample mean. The
    shape is then found by a one-dimensional search on log(nu).
    """
    n = sum(counts)
    mean = sum(x * c for x, c in enumerate(counts)) / n
    if mean <= 0:
        raise ValueError("all counts are zero")

    def prof(t: float) -> float:
        nu = math.exp(t)
        return _nb_loglik(counts, nu, mean / nu)

    t = _golden_max(prof, math.log(1e-4), math.log(1e4))
    nu = math.exp(t)
    return nu, mean / nu


def gamma_poisson_posterior_mean(x: int, nu: float, scale: float) -> float:
    """E[theta | x] = (x + nu) scale / (1 + scale) under a Gamma(nu, scale) prior."""
    return (x + nu) * scale / (1.0 + scale)


def _normal_marginal_loglik(x, s2, mu, tau2) -> float:
    """Log-likelihood of the marginal law x_i ~ N(mu, s2_i + tau2)."""
    terms = [math.log(2 * math.pi * (v + tau2)) + (a - mu) ** 2 / (v + tau2) for a, v in zip(x, s2)]  # @line L1
    return -0.5 * math.fsum(terms)


def _weighted_mean(x, s2, tau2) -> float:
    w = [1.0 / (v + tau2) for v in s2]
    return math.fsum(a * b for a, b in zip(w, x)) / math.fsum(w)


def normal_eb(x: Sequence[float], s2: Sequence[float]) -> dict:
    """Type II maximum likelihood for x_i ~ N(theta_i, s2_i), theta_i ~ N(mu, tau^2).

    The marginal law is x_i ~ N(mu, s2_i + tau^2) (line L1 of the template). For
    equal s2_i the maximum is tau^2 = max(0, mean((x - xbar)^2) - s2), mu = xbar. For
    unequal s2_i, mu is profiled out as the weighted mean and tau is found by a
    search on [0, upper]. Returns mu, tau2, the shrinkage factors B_i = s2_i/(s2_i +
    tau^2), the posterior means and the plug-in posterior variances.
    """
    p = len(x)
    if len(set(s2)) == 1:
        v = s2[0]
        xbar = math.fsum(x) / p
        tau2 = max(0.0, math.fsum((a - xbar) ** 2 for a in x) / p - v)  # @line L2
        mu = xbar
    else:
        spread = max(x) - min(x)
        upper = (spread + math.sqrt(max(s2))) ** 2

        def prof(tau: float) -> float:
            t2 = tau * tau
            return _normal_marginal_loglik(x, s2, _weighted_mean(x, s2, t2), t2)

        grid = [upper * j / 400.0 for j in range(401)]
        vals = [prof(t) for t in grid]
        j = max(range(len(grid)), key=lambda i: vals[i])
        lo = grid[max(j - 1, 0)]
        hi = grid[min(j + 1, len(grid) - 1)]
        tau = _golden_max(prof, lo, hi) if j > 0 else 0.0
        if j > 0 and prof(0.0) >= prof(tau):
            tau = 0.0
        tau2 = tau * tau
        mu = _weighted_mean(x, s2, tau2)
    shrink, mean, var = [], [], []
    for a, v in zip(x, s2):  # @line L3
        b = v / (v + tau2) if v + tau2 > 0 else 1.0
        shrink.append(b)
        mean.append(mu + (1.0 - b) * (a - mu))  # @line L4
        var.append((1.0 - b) * v)
    return {"mu": mu, "tau2": tau2, "shrink": shrink, "post_mean": mean, "post_var": var,  # @line L5
            "loglik": _normal_marginal_loglik(x, s2, mu, tau2)}


def tweedie_posterior_mean(z: float, atoms: Sequence[float], weights: Sequence[float],
                           sigma2: float = 1.0) -> float:
    """Tweedie's formula E[mu | z] = z + sigma2 * f'(z)/f(z) for the normal mixture
    f(z) = sum_k g_k N(z; mu_k, sigma2), with the derivative computed analytically."""
    dens = [g * math.exp(-(z - m) ** 2 / (2 * sigma2)) for m, g in zip(atoms, weights)]
    f = math.fsum(dens)
    fprime = math.fsum(d * (m - z) / sigma2 for d, m in zip(dens, atoms))
    return z + sigma2 * fprime / f


def discrete_prior_posterior_mean(z: float, atoms: Sequence[float], weights: Sequence[float],
                                  sigma2: float = 1.0) -> float:
    """E[mu | z] for z ~ N(mu, sigma2) and the discrete prior P(mu = atoms[k]) = weights[k]."""
    post = [g * math.exp(-(z - m) ** 2 / (2 * sigma2)) for m, g in zip(atoms, weights)]
    return math.fsum(p * m for p, m in zip(post, atoms)) / math.fsum(post)
