# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-bayesian-computation/. The authors are listed in prov/5HMWEW.jsonl.
"""Approximate Bayesian computation: the template with a rejection sampler and an
optional local linear regression adjustment (Beaumont, Zhang and Balding 2002), plus
the exact Bayes factors of the Poisson versus geometric example of model choice.

abc returns the kept parameters together with their simulated summaries.
Cost: n_sims prior draws and simulations, then O(k) for the k kept pairs.
"""

import math
import random
from fractions import Fraction
from typing import Callable, Sequence


def abc(
    x,
    prior_draw: Callable,
    simulate: Callable,
    summary: Callable,
    distance: Callable,
    eps: float,
    n_sims: int,
    rng: random.Random,
    adjust: bool = False,
) -> list:
    """The template with SAMPLER = rejection and ADJUST = regression (if adjust).

    Returns a list of (theta, s, weight). Without adjustment all weights are 1.
    Precondition: scalar theta and scalar summary when adjust is True.
    """
    s_obs = summary(x)  # @line L1

    def accept(s):  # @line L2
        return distance(s, s_obs) <= eps

    kept = []
    for _ in range(n_sims):  # @line L3
        th = prior_draw(rng)
        s = summary(simulate(th, rng))
        if accept(s):
            kept.append((th, s, 1.0))
    if adjust:
        kept = regression_adjust(kept, s_obs, eps)  # @line L4
    return kept  # @line L5


def regression_adjust(kept: Sequence, s_obs: float, eps: float) -> list:
    """Local linear regression adjustment with Epanechnikov weights.

    Fit theta = a + b (s - s_obs) by weighted least squares over the kept pairs,
    with weights 1 - (|s - s_obs| / eps)^2, and return (theta - b (s - s_obs), s, weight).
    If the summaries do not vary, nothing is changed.
    """
    ws = [max(0.0, 1.0 - ((s - s_obs) / eps) ** 2) if eps > 0 else 1.0 for _, s, _ in kept]
    tot = math.fsum(ws)
    if tot == 0:
        return list(kept)
    sm = math.fsum(w * (s - s_obs) for w, (_, s, _) in zip(ws, kept)) / tot
    tm = math.fsum(w * t for w, (t, _, _) in zip(ws, kept)) / tot
    sxx = math.fsum(w * (s - s_obs - sm) ** 2 for w, (_, s, _) in zip(ws, kept))
    if sxx == 0:
        return list(kept)
    sxy = math.fsum(w * (s - s_obs - sm) * (t - tm) for w, (t, s, _) in zip(ws, kept))
    b = sxy / sxx
    return [(t - b * (s - s_obs), s, w) for w, (t, s, _) in zip(ws, kept)]


def weighted_mean_var(kept: Sequence) -> tuple[float, float]:
    tot = math.fsum(w for _, _, w in kept)
    m = math.fsum(w * t for t, _, w in kept) / tot
    v = math.fsum(w * (t - m) ** 2 for t, _, w in kept) / tot
    return m, v


# Model choice: Poisson(lambda), lambda ~ Exp(1), against Geometric(p) on {0, 1, ...},
# P(x | p) = p (1 - p)^x, p ~ Uniform(0, 1). All values are exact Fractions.

def evidence_poisson(xs: Sequence[int]) -> Fraction:
    """m_P(x) = Gamma(S + 1) / ((n + 1)^(S + 1) prod x_i!)."""
    n, s = len(xs), sum(xs)
    return Fraction(math.factorial(s), (n + 1) ** (s + 1) * math.prod(math.factorial(v) for v in xs))


def evidence_geometric(xs: Sequence[int]) -> Fraction:
    """m_G(x) = B(n + 1, S + 1) = n! S! / (n + S + 1)!."""
    n, s = len(xs), sum(xs)
    return Fraction(math.factorial(n) * math.factorial(s), math.factorial(n + s + 1))


def evidence_poisson_sum(n: int, s: int) -> Fraction:
    """Marginal probability of S = s under the Poisson model: n^s / (n + 1)^(s + 1)."""
    return Fraction(n**s, (n + 1) ** (s + 1))


def evidence_geometric_sum(n: int, s: int) -> Fraction:
    """Marginal probability of S = s under the geometric model: C(n + s - 1, s) B(n + 1, s + 1)."""
    return math.comb(n + s - 1, s) * Fraction(math.factorial(n) * math.factorial(s), math.factorial(n + s + 1))


def abc_model_choice(xs: Sequence[int], summary: Callable, n_sims: int, rng: random.Random) -> tuple[int, int]:
    """ABC rejection over (model, parameter) with equal prior model probabilities and eps = 0.

    Returns (kept under Poisson, kept under geometric). Their ratio estimates the Bayes
    factor of the summary, which equals the true one only if the summary is sufficient
    for the model index as well.
    """
    n = len(xs)
    s_obs = summary(xs)
    counts = [0, 0]
    for _ in range(n_sims):
        m = rng.randrange(2)
        if m == 0:
            lam = rng.expovariate(1.0)
            y = [_poisson(lam, rng) for _ in range(n)]
        else:
            p = rng.random()
            y = [_geometric(p, rng) for _ in range(n)]
        if summary(y) == s_obs:
            counts[m] += 1
    return counts[0], counts[1]


def _poisson(lam: float, rng: random.Random) -> int:
    k, prod, lim = 0, rng.random(), math.exp(-lam)
    while prod > lim:
        k += 1
        prod *= rng.random()
    return k


def _geometric(p: float, rng: random.Random) -> int:
    """Number of failures before the first success."""
    if p >= 1.0:
        return 0
    u = 1.0 - rng.random()
    return int(math.log(u) / math.log1p(-p)) if p > 0 else 10**9
