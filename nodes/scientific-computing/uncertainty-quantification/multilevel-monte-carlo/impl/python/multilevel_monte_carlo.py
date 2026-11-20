# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multilevel-monte-carlo/. The authors are listed in prov/SAT4ZW.jsonl.
"""Multilevel Monte Carlo with the adaptive level and sample choice of Giles (2008, 2015).

The caller gives a function sample(l, n, rng) that draws n independent samples
of the correction Y_l = P_l - P_(l-1) (with P_(-1) = 0). The fine and the coarse
value in one sample must use the same random input, or the variance of Y_l does
not decay. The function returns the sum of the samples, the sum of their
squares and the total cost of the n samples.

The rates alpha (weak error), beta (variance of Y_l) and gamma (cost of Y_l)
are given by the caller, as in Giles 2008. The estimator stops when the
estimated variance is at most eps^2 / 2 and the estimated bias is at most
eps / sqrt(2), so that the mean squared error is at most eps^2 if the
estimates are right.
"""

import math
import random
from typing import Callable

Sampler = Callable[[int, int, random.Random], tuple[float, float, float]]


def optimal_counts(v: list[float], c: list[float], eps: float) -> list[int]:
    """N_l = ceil(2 eps^-2 sqrt(V_l / C_l) sum_k sqrt(V_k C_k)), so that sum V_l / N_l <= eps^2 / 2."""
    total = sum(math.sqrt(vk * ck) for vk, ck in zip(v, c))
    return [math.ceil(2.0 / eps**2 * math.sqrt(vl / cl) * total) for vl, cl in zip(v, c)]


def mlmc(
    sample: Sampler,
    eps: float,
    alpha: float,
    beta: float,
    gamma: float,
    rng: random.Random,
    l0: int = 2,
    n0: int = 200,
    max_level: int = 20,
) -> dict:
    """Estimate E[P] to a root mean square error of about eps.

    Returns a dict with the estimate, the finest level L, the sample counts,
    the mean and variance of each correction, and the total cost.
    """
    big_l = l0  # @line L1
    n = [0] * (big_l + 1)
    dn = [n0] * (big_l + 1)
    s1 = [0.0] * (big_l + 1)
    s2 = [0.0] * (big_l + 1)
    cost = [0.0] * (big_l + 1)
    while any(x > 0 for x in dn):  # @line L2
        for l in range(big_l + 1):  # @line L3
            if dn[l] > 0:
                a, b, w = sample(l, dn[l], rng)
                s1[l] += a
                s2[l] += b
                cost[l] += w
                n[l] += dn[l]
        v, c = _moments(n, s1, s2, cost, beta, gamma)  # @line L4
        dn = [max(0, nl - ml) for nl, ml in zip(optimal_counts(v, c, eps), n)]  # @line L5
        if all(x == 0 for x in dn):  # @line L6
            m = [s1[l] / n[l] for l in range(big_l + 1)]
            bias = max(abs(m[big_l]), abs(m[big_l - 1]) / 2**alpha) / (2**alpha - 1)  # @line L7
            if bias > eps / math.sqrt(2.0):  # @line L8
                if big_l == max_level:
                    raise RuntimeError("the bias test failed at the largest level")
                big_l += 1
                n.append(0)
                s1.append(0.0)
                s2.append(0.0)
                cost.append(0.0)
                v, c = _moments(n, s1, s2, cost, beta, gamma)
                dn = [max(0, nl - ml) for nl, ml in zip(optimal_counts(v, c, eps), n)]
    means = [s1[l] / n[l] for l in range(big_l + 1)]
    v, _ = _moments(n, s1, s2, cost, beta, gamma)
    return {
        "estimate": sum(means),  # @line L9
        "L": big_l,
        "N": n,
        "means": means,
        "variances": v,
        "cost": sum(cost),
    }


def _moments(n, s1, s2, cost, beta, gamma):
    """Sample variance and mean cost per level. A new level with no samples gets V and C from the rates."""
    v, c = [], []
    for l in range(len(n)):
        if n[l] > 0:
            mean = s1[l] / n[l]
            v.append(max(s2[l] / n[l] - mean * mean, 1e-300))
            c.append(cost[l] / n[l])
        else:
            v.append(v[l - 1] / 2**beta)
            c.append(c[l - 1] * 2**gamma)
    return v, c


def gbm_euler_sampler(s0: float, r: float, sigma: float, t: float) -> Sampler:
    """Coupled Euler-Maruyama samples of P_l - P_(l-1) for P = S_T of geometric Brownian motion.

    Level l uses 2^l steps of size h_l = T / 2^l. The coarse path of a sample sums
    pairs of the fine Brownian increments, so both paths see the same noise.
    The cost of one sample is the number of fine plus coarse steps.
    """

    def sample(l: int, nsamp: int, rng: random.Random) -> tuple[float, float, float]:
        nf = 2**l
        hf = t / nf
        sq = math.sqrt(hf)
        sum1 = sum2 = 0.0
        for _ in range(nsamp):
            xf = s0
            xc = s0
            dwc = 0.0
            for k in range(nf):
                dw = sq * rng.gauss(0.0, 1.0)
                xf += r * xf * hf + sigma * xf * dw
                dwc += dw
                if l > 0 and k % 2 == 1:
                    xc += r * xc * (2 * hf) + sigma * xc * dwc
                    dwc = 0.0
            y = xf - xc if l > 0 else xf
            sum1 += y
            sum2 += y * y
        steps = nf + (nf // 2 if l > 0 else 0)
        return sum1, sum2, float(steps * nsamp)

    return sample


def euler_gbm_mean(s0: float, r: float, t: float, l: int) -> float:
    """The exact mean E[P_l] = S_0 (1 + r h_l)^(2^l) of the Euler value of S_T, with h_l = T / 2^l."""
    return s0 * (1.0 + r * t / 2**l) ** (2**l)
