# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conjugate-prior/. The authors are listed in prov/6PNECN.jsonl.

"""Closed-form posterior updates for the standard conjugate pairs.

Each function maps prior hyperparameters and data to posterior
hyperparameters. The arithmetic is exact when the inputs are Fractions.
"""

from fractions import Fraction
from typing import List, Sequence, Tuple


def beta_binomial(a, b, data: Sequence[int]) -> Tuple:
    """Bernoulli data, Beta(a, b) prior -> Beta(a + s, b + n - s)."""
    s = sum(data)
    return a + s, b + len(data) - s


def gamma_poisson(alpha, beta, data: Sequence[int]) -> Tuple:
    """Poisson data, Gamma(shape alpha, rate beta) prior -> Gamma(alpha + sum x, beta + n)."""
    return alpha + sum(data), beta + len(data)


def normal_known_variance(mu0, tau0_sq, sigma_sq, data: Sequence) -> Tuple:
    """N(theta, sigma_sq) data with sigma_sq known, N(mu0, tau0_sq) prior on theta.

    Returns (mu_n, tau_n_sq): precisions add, and the mean is the
    precision-weighted average of mu0 and the sample mean.
    """
    n = len(data)
    prec = 1 / tau0_sq + n / sigma_sq
    tau_n_sq = 1 / prec
    mu_n = tau_n_sq * (mu0 / tau0_sq + sum(data) / sigma_sq)
    return mu_n, tau_n_sq


def normal_inverse_gamma(mu0, kappa0, alpha0, beta0, data: Sequence) -> Tuple:
    """N(mu, s2) data, mu | s2 ~ N(mu0, s2 / kappa0), s2 ~ InvGamma(alpha0, beta0).

    Returns (mu_n, kappa_n, alpha_n, beta_n).
    """
    n = len(data)
    if n == 0:
        return mu0, kappa0, alpha0, beta0
    xbar = sum(data) / Fraction(n) if isinstance(data[0], (int, Fraction)) else sum(data) / n
    ss = sum((x - xbar) ** 2 for x in data)
    kappa_n = kappa0 + n
    mu_n = (kappa0 * mu0 + n * xbar) / kappa_n
    alpha_n = alpha0 + Fraction(n, 2) if isinstance(alpha0, (int, Fraction)) else alpha0 + n / 2
    beta_n = beta0 + ss / 2 + kappa0 * n * (xbar - mu0) ** 2 / (2 * kappa_n)
    return mu_n, kappa_n, alpha_n, beta_n


def dirichlet_multinomial(alpha: Sequence, counts: Sequence[int]) -> List:
    """Categorical data summarized by counts, Dirichlet(alpha) prior -> Dirichlet(alpha + counts)."""
    if len(alpha) != len(counts):
        raise ValueError("alpha and counts differ in length")
    return [a + c for a, c in zip(alpha, counts)]


def exponential_family_conjugate(chi: Sequence, nu, stats: Sequence[Sequence]) -> Tuple[List, object]:
    """Generic update for p(x|eta) = h(x) exp(eta.T(x) - A(eta)).

    The prior is proportional to exp(eta.chi - nu A(eta)). The data enter
    only through the sufficient statistics T(x_i), given in stats.
    Returns (chi + sum T(x_i), nu + n).
    """
    out = list(chi)
    for t in stats:
        for k, v in enumerate(t):
            out[k] = out[k] + v
    return out, nu + len(stats)
