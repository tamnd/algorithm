# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cori-rt-estimation/. The authors are listed in prov/FC6CRV.jsonl.
"""The Cori method: a gamma posterior for R_t over sliding windows.

Model: I_t given the past is Poisson(R Lambda_t), with the total
infectiousness Lambda_t = sum over s >= 1 of w[s] I_(t-s), and R constant
over each window of tau days. With a gamma prior of shape a and scale b on R,
the posterior over the window that ends on day t is a gamma law with

    shape A = a + (sum of I_s over the window),
    rate  B = 1 / b + (sum of Lambda_s over the window).

Days are numbered 1 to T; incidence[0] is day 1. w[0] must be 0, and w[s] is
the weight of an infector infected s days earlier.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Sequence, Tuple

from biostoch import chi2_sf, poisson


@dataclass
class WindowEstimate:
    t_start: int  # first day of the window (1-based)
    t_end: int  # last day of the window
    shape: float  # A
    rate: float  # B
    mean: float
    sd: float
    cv: float
    quantiles: Tuple[float, ...]


def total_infectiousness(incidence: Sequence[float], w: Sequence[float]) -> List[float]:
    """Lambda_t for t = 1 .. T, with the cases before day 1 taken as 0."""
    if w and w[0] != 0:
        raise ValueError("w[0] must be 0: no infection on the day of one's own infection")
    T = len(incidence)
    lam = [0.0] * T
    for t in range(T):
        acc = 0.0
        for s in range(1, min(t, len(w) - 1) + 1):
            acc += w[s] * incidence[t - s]
        lam[t] = acc
    return lam


def gamma_cdf(x: float, shape: float, rate: float) -> float:
    """P(X <= x) for X ~ Gamma(shape, rate), as 1 - chi2_sf(2 rate x, 2 shape)."""
    if x <= 0:
        return 0.0
    return 1.0 - chi2_sf(2.0 * rate * x, 2.0 * shape)


def gamma_quantile(p: float, shape: float, rate: float, tol: float = 1e-12) -> float:
    """The p-quantile of Gamma(shape, rate) by bisection on gamma_cdf."""
    if not 0.0 < p < 1.0:
        raise ValueError("need 0 < p < 1")
    lo, hi = 0.0, (shape + 10.0 * math.sqrt(shape) + 10.0) / rate
    while gamma_cdf(hi, shape, rate) < p:
        hi *= 2.0
    while hi - lo > tol * max(1.0, hi):
        mid = 0.5 * (lo + hi)
        if gamma_cdf(mid, shape, rate) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def estimate(incidence: Sequence[float], w: Sequence[float], tau: int = 7,
             a: float = 1.0, b: float = 5.0,
             probs: Sequence[float] = (0.025, 0.5, 0.975),
             first_day: int = 2) -> List[WindowEstimate]:
    """Posterior summaries of R for every window of tau days inside first_day .. T.

    Windows start on first_day or later, so that Lambda uses at least one
    past day. a and b are the shape and the scale of the gamma prior.
    """
    if tau < 1 or a <= 0 or b <= 0:
        raise ValueError("need tau >= 1, a > 0 and b > 0")
    T = len(incidence)
    lam = total_infectiousness(incidence, w)  # @line L1
    ci = [0.0] * (T + 1)  # prefix sums of I and Lambda
    cl = [0.0] * (T + 1)
    for t in range(T):
        ci[t + 1] = ci[t] + incidence[t]
        cl[t + 1] = cl[t] + lam[t]
    out = []
    for t in range(first_day + tau - 1, T + 1):  # @line L2
        s = t - tau + 1
        A = a + ci[t] - ci[s - 1]  # @line L3
        B = 1.0 / b + cl[t] - cl[s - 1]  # @line L4
        mean, sd = A / B, math.sqrt(A) / B  # @line L5
        qs = tuple(gamma_quantile(p, A, B) for p in probs)  # @line L6
        out.append(WindowEstimate(s, t, A, B, mean, sd, 1.0 / math.sqrt(A), qs))  # @line L7
    return out


def simulate(rng, seed: Sequence[int], r_path: Sequence[float], w: Sequence[float]) -> List[int]:
    """Incidence from the Poisson renewal model.

    seed gives the first days. Day len(seed) + k + 1 gets
    Poisson(r_path[k] Lambda), one biostoch.poisson draw per day, in order.
    """
    inc = list(seed)
    for r in r_path:
        t = len(inc)
        lam = sum(w[s] * inc[t - s] for s in range(1, min(t, len(w) - 1) + 1))
        inc.append(poisson(rng, r * lam))
    return inc
