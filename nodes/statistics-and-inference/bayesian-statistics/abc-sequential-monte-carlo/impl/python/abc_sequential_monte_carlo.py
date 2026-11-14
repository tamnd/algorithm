# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/abc-sequential-monte-carlo/. The authors are listed in prov/HY1FY8.jsonl.
"""ABC sequential Monte Carlo, in the population Monte Carlo form of Beaumont, Cornuet,
Marin and Robert (2009), for a scalar parameter.

Generation 1 is ABC rejection at tolerance eps_1. Generation t >= 2 proposes
theta* = theta_j + N(0, s^2) with j drawn from the previous weights, keeps theta* when its
simulated summary is within eps_t, and gives it the importance weight

    w = pi(theta*) / sum_j W_j K(theta* | theta_j).

The weighted population targets the eps_t-posterior pi(theta) P_theta(rho <= eps_t), for
any previous population, because the acceptance probability appears in both the target
and the proposal and cancels.

Cost per generation: N / A simulations for acceptance rate A, plus N^2 kernel
evaluations for the weights.
"""

import math
import random
from typing import Callable, Sequence


def normal_pdf(z: float, s: float) -> float:
    return math.exp(-0.5 * (z / s) ** 2) / (s * math.sqrt(2 * math.pi))


def weighted_variance(xs: Sequence[float], ws: Sequence[float]) -> float:
    m = math.fsum(w * x for x, w in zip(xs, ws))
    return math.fsum(w * (x - m) ** 2 for x, w in zip(xs, ws))


def smc_weight(theta, prior_pdf: Callable, prev: Sequence, prev_w: Sequence, kernel_pdf: Callable):
    """The importance weight pi(theta) / sum_j W_j K(theta | theta_j) (line L9).

    Works with floats or with Fractions (for the exact tests).
    """
    g = sum(w * kernel_pdf(theta, p) for p, w in zip(prev, prev_w))
    return prior_pdf(theta) / g


def abc_smc(
    prior_draw: Callable,
    prior_pdf: Callable,
    simulate: Callable,
    summary: Callable,
    s_obs,
    distance: Callable,
    eps_schedule: Sequence[float],
    n: int,
    rng: random.Random,
    equal_weights: bool = False,
) -> dict:
    """Run ABC-SMC. Returns the final particles, normalized weights, the kernel scales,
    the number of simulations per generation, and the effective sample sizes.

    Precondition: eps_schedule is non-increasing; prior_pdf(theta) > 0 exactly where the
    prior has mass. equal_weights=True drops the importance weights (a wrong variant,
    kept for the tests and the page).
    """
    sims = []
    parts = []
    count = 0
    while len(parts) < n:  # @line L1
        count += 1
        th = prior_draw(rng)
        if distance(summary(simulate(th, rng)), s_obs) <= eps_schedule[0]:
            parts.append(th)
    sims.append(count)
    weights = [1.0 / n] * n
    scales = []
    for eps in eps_schedule[1:]:  # @line L3
        s = math.sqrt(2 * weighted_variance(parts, weights))  # @line L2
        s = max(s, 1e-12)
        scales.append(s)
        cum = []
        acc = 0.0
        for w in weights:
            acc += w
            cum.append(acc)
        new_parts, new_w = [], []
        count = 0
        for _ in range(n):  # @line L4
            while True:  # @line L5
                j = min(_bisect(cum, rng.random() * acc), n - 1)  # @line L6
                th = parts[j] + rng.gauss(0.0, s)
                if prior_pdf(th) <= 0:  # @line L8
                    continue
                count += 1  # count simulations only
                y = simulate(th, rng)  # @line L7
                if distance(summary(y), s_obs) <= eps:
                    break
            new_parts.append(th)
            if equal_weights:
                new_w.append(1.0)
            else:
                new_w.append(smc_weight(th, prior_pdf, parts, weights, lambda a, b: normal_pdf(a - b, s)))  # @line L9
        tot = math.fsum(new_w)
        parts, weights = new_parts, [w / tot for w in new_w]  # @line L10
        sims.append(count)
    return {  # @line L11
        "particles": parts,
        "weights": weights,
        "scales": scales,
        "sims": sims,
        "ess": 1.0 / math.fsum(w * w for w in weights),
    }


def _bisect(cum: Sequence[float], u: float) -> int:
    lo, hi = 0, len(cum)
    while lo < hi:
        mid = (lo + hi) // 2
        if cum[mid] <= u:
            lo = mid + 1
        else:
            hi = mid
    return lo
