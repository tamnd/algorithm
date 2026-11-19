# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/map-speaker-adaptation/. The authors are listed in prov/TAZK46.jsonl.

"""MAP adaptation of the means of a Gaussian mixture (Gauvain and Lee 1994).

The prior model is a mixture of M Gaussians with diagonal covariances: weights
c[m], means mu0[m] and variances var[m]. The prior on the mean of Gaussian m is
N(mu0[m], var[m] / tau), independent over m, and the weights and variances are
fixed. One EM step of MAP estimation is

    mu_m = (tau mu0_m + sum_t gamma_m(t) o_t) / (tau + sum_t gamma_m(t)),

where gamma_m(t) is the posterior of Gaussian m at frame t under the current
means. map_adapt iterates this step; one step is the usual practice.

reynolds_adapt is the one-step form of Reynolds, Quatieri and Dunn 2000, which
also adapts the weights and the variances with the coefficient
alpha_m = n_m / (n_m + r) for a relevance factor r. For the means it gives the
same value as one step of map_adapt with tau = r.

Every log is the natural log. Posteriors are computed in log space.
"""

import math
from typing import List, Sequence, Tuple

from nlslog import log_sum

Vector = List[float]
Matrix = List[List[float]]

LOG_2PI = math.log(2.0 * math.pi)


def log_gauss_diag(x: Sequence[float], mu: Sequence[float], var: Sequence[float]) -> float:
    """Return log N(x; mu, diag(var))."""
    s = 0.0
    for xi, mi, vi in zip(x, mu, var):
        s += LOG_2PI + math.log(vi) + (xi - mi) * (xi - mi) / vi
    return -0.5 * s


def posteriors(frame: Sequence[float], weights: Sequence[float], means: Sequence[Sequence[float]],
               variances: Sequence[Sequence[float]]) -> Tuple[Vector, float]:
    """Return (gamma, log p(frame)) for a diagonal Gaussian mixture."""
    lp = [math.log(w) + log_gauss_diag(frame, m, v) if w > 0 else float("-inf")
          for w, m, v in zip(weights, means, variances)]
    z = log_sum(lp)
    return [math.exp(x - z) for x in lp], z


def statistics(frames: Sequence[Sequence[float]], weights: Sequence[float], means: Sequence[Sequence[float]],
               variances: Sequence[Sequence[float]]) -> Tuple[Vector, Matrix, Matrix, float]:
    """Return (n, s, q, log likelihood): n_m = sum gamma, s_m = sum gamma o, q_m = sum gamma o^2 per dimension."""
    M, d = len(means), len(means[0])
    n = [0.0] * M
    s = [[0.0] * d for _ in range(M)]
    q = [[0.0] * d for _ in range(M)]
    ll = 0.0
    for o in frames:
        g, z = posteriors(o, weights, means, variances)  # @line L3
        ll += z
        for m in range(M):
            gm = g[m]
            if gm > 0.0:
                n[m] += gm  # @line L4
                for i in range(d):
                    s[m][i] += gm * o[i]
                    q[m][i] += gm * o[i] * o[i]
    return n, s, q, ll


def map_means(mu0: Sequence[Sequence[float]], n: Sequence[float], s: Sequence[Sequence[float]], tau: float) -> Matrix:
    """Return mu_m = (tau mu0_m + s_m) / (tau + n_m). Needs tau > 0 or n_m > 0."""
    out = []
    for m in range(len(mu0)):
        den = tau + n[m]
        if den <= 0.0:
            raise ValueError("tau + n_m must be positive")
        out.append([(tau * a + b) / den for a, b in zip(mu0[m], s[m])])  # @line L5
    return out


def log_prior(means: Sequence[Sequence[float]], mu0: Sequence[Sequence[float]],
              variances: Sequence[Sequence[float]], tau: float) -> float:
    """Return sum_m log N(mu_m; mu0_m, diag(var_m) / tau)."""
    return math.fsum(log_gauss_diag(mu, m0, [v / tau for v in var]) for mu, m0, var in zip(means, mu0, variances))


def map_adapt(frames: Sequence[Sequence[float]], weights: Sequence[float], mu0: Sequence[Sequence[float]],
              variances: Sequence[Sequence[float]], tau: float, iterations: int = 1) -> Tuple[Matrix, List[float]]:
    """Run MAP-EM on the means. Return (means, objective values).

    The objective is log p(frames | means) + log prior(means), given before
    each iteration and after the last one (tau > 0 for the prior term).
    """
    means = [list(map(float, m)) for m in mu0]  # @line L1
    history = []
    for _ in range(iterations):  # @line L2
        n, s, _, ll = statistics(frames, weights, means, variances)
        history.append(ll + log_prior(means, mu0, variances, tau))
        means = map_means(mu0, n, s, tau)
    ll = statistics(frames, weights, means, variances)[3]
    history.append(ll + log_prior(means, mu0, variances, tau))
    return means, history  # @line L6


def reynolds_adapt(frames: Sequence[Sequence[float]], weights: Sequence[float], means: Sequence[Sequence[float]],
                   variances: Sequence[Sequence[float]], r: float = 16.0, adapt: str = "wmv",
                   var_floor: float = 1e-6) -> Tuple[Vector, Matrix, Matrix]:
    """One-step adaptation of weights (w), means (m) and variances (v) with alpha_m = n_m / (n_m + r).

    Return (weights, means, variances); the parts not named in adapt stay.
    """
    T = len(frames)
    M, d = len(means), len(means[0])
    n, s, q, _ = statistics(frames, weights, means, variances)
    alpha = [n[m] / (n[m] + r) if n[m] + r > 0 else 0.0 for m in range(M)]
    new_w = list(weights)
    if "w" in adapt:
        raw = [alpha[m] * n[m] / T + (1.0 - alpha[m]) * weights[m] for m in range(M)]
        z = math.fsum(raw)
        new_w = [x / z for x in raw]
    new_mu = [list(mu) for mu in means]
    new_var = [list(v) for v in variances]
    for m in range(M):
        if n[m] <= 0.0:
            continue
        E = [x / n[m] for x in s[m]]
        E2 = [x / n[m] for x in q[m]]
        mu_hat = [alpha[m] * E[i] + (1.0 - alpha[m]) * means[m][i] for i in range(d)]
        if "m" in adapt:
            new_mu[m] = mu_hat
        if "v" in adapt:
            # Reynolds et al. 2000: the second moment is interpolated, then the square of the adapted mean is removed.
            new_var[m] = [max(var_floor, alpha[m] * E2[i] + (1.0 - alpha[m]) * (variances[m][i] + means[m][i] ** 2)
                              - mu_hat[i] ** 2) for i in range(d)]
    return new_w, new_mu, new_var
