# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bridge-sampling/. The authors are listed in prov/TC3WDX.jsonl.
"""Bridge sampling of a ratio of normalizing constants (Meng and Wong 1996).

Two densities p_k = q_k / c_k, k = 1, 2, are known only up to the constants c_k.
Given draws theta_1..theta_n1 from p1 and phi_1..phi_n2 from p2, the bridge
identity

    r = c1 / c2 = E_2[q1 alpha] / E_1[q2 alpha]

holds for every bridge function alpha with 0 < integral of alpha q1 q2 < infinity.
All functions here work with logarithms, because q1 and q2 often differ by
hundreds of orders of magnitude.

For a marginal likelihood, p1 is the posterior with q1 = f(x | theta) pi(theta), so
c1 = Z, and p2 is a normalized proposal density g with c2 = 1. Then r = Z.

The inputs are the log ratios log l = log q1 - log q2 at the two samples:
  log_l1[i] = log q1(theta_i) - log q2(theta_i),  theta_i ~ p1,
  log_l2[j] = log q1(phi_j) - log q2(phi_j),      phi_j ~ p2.

Cost: one pass over the n1 + n2 ratios per iteration, Theta((n1 + n2) T) for T
iterations. The iteration is a contraction in log r, so T = O(log(1/tol)).
"""

import math
from typing import Callable, Sequence


def log_sum_exp(xs: Sequence[float]) -> float:
    """log(sum(exp(x))) without overflow."""
    m = max(xs)
    if m == -math.inf:
        return -math.inf
    return m + math.log(math.fsum(math.exp(x - m) for x in xs))


def log_mean_exp(xs: Sequence[float]) -> float:
    return log_sum_exp(xs) - math.log(len(xs))


def _log_add(a: float, b: float) -> float:
    """log(e^a + e^b)."""
    if a < b:
        a, b = b, a
    return a + math.log1p(math.exp(b - a))


def optimal_bridge(
    log_l1: Sequence[float],
    log_l2: Sequence[float],
    tol: float = 1e-12,
    max_iter: int = 10000,
    log_r0: float | None = None,
) -> tuple[float, int]:
    """Meng-Wong iteration for the optimal bridge. Returns (log r_hat, iterations).

    Precondition: both samples are non-empty and all log ratios are finite.
    """
    n1, n2 = len(log_l1), len(log_l2)
    s1 = n1 / (n1 + n2)  # @line L1
    s2 = n2 / (n1 + n2)
    ls1, ls2 = math.log(s1), math.log(s2)
    # L2 and L3: the caller passes log l1 and log l2.
    log_r = log_mean_exp(log_l2) if log_r0 is None else log_r0  # @line L4
    for it in range(1, max_iter + 1):  # @line L5
        # log of (1/n2) sum_j l2j / (s1 l2j + s2 r)
        num = log_mean_exp([b - _log_add(ls1 + b, ls2 + log_r) for b in log_l2])  # @line L6
        # log of (1/n1) sum_i 1 / (s1 l1i + s2 r)
        den = log_mean_exp([-_log_add(ls1 + a, ls2 + log_r) for a in log_l1])  # @line L7
        new = num - den  # @line L8
        if abs(new - log_r) <= tol:  # @line L9
            return new, it
        log_r = new
    return log_r, max_iter  # @line L10


def bridge_from_densities(
    log_q1: Callable[[float], float],
    log_q2: Callable[[float], float],
    draws1: Sequence,
    draws2: Sequence,
    tol: float = 1e-12,
) -> float:
    """log r_hat from the two samples and the two log densities (lines L2 and L3, then L4 to L10).

    draws1 come from p1 = q1/c1 and draws2 from p2 = q2/c2. Cost: 2 (n1 + n2) density
    evaluations plus the iteration.
    """
    log_l1 = [log_q1(t) - log_q2(t) for t in draws1]  # @line L2
    log_l2 = [log_q1(t) - log_q2(t) for t in draws2]  # @line L3
    return optimal_bridge(log_l1, log_l2, tol)[0]


def estimating_function(log_r: float, log_l1: Sequence[float], log_l2: Sequence[float]) -> float:
    """(1/n1) sum r / (s1 l1i + s2 r) - (1/n2) sum l2j / (s1 l2j + s2 r).

    Strictly increasing in r, from -1/s1 at r = 0 to 1/s2 as r grows; its unique root
    is the fixed point of the iteration. Used by the tests and by bisection_bridge.
    """
    n1, n2 = len(log_l1), len(log_l2)
    s1, s2 = n1 / (n1 + n2), n2 / (n1 + n2)
    left = math.fsum(1.0 / (s1 * math.exp(a - log_r) + s2) for a in log_l1) / n1
    right = math.fsum(1.0 / (s1 + s2 * math.exp(log_r - b)) for b in log_l2) / n2
    return left - right


def bisection_bridge(log_l1: Sequence[float], log_l2: Sequence[float], tol: float = 1e-13) -> float:
    """The root of estimating_function by bisection in log r: an independent oracle."""
    lo = min(min(log_l1), min(log_l2)) - 1.0
    hi = max(max(log_l1), max(log_l2)) + 1.0
    while estimating_function(lo, log_l1, log_l2) > 0:
        lo -= 10.0
    while estimating_function(hi, log_l1, log_l2) < 0:
        hi += 10.0
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if estimating_function(mid, log_l1, log_l2) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def general_bridge(
    log_q1_at_1: Sequence[float],
    log_q2_at_1: Sequence[float],
    log_q1_at_2: Sequence[float],
    log_q2_at_2: Sequence[float],
    log_alpha: Callable[[float, float], float],
) -> float:
    """log of r_hat = mean_j q1(phi_j) alpha(phi_j) / mean_i q2(theta_i) alpha(theta_i).

    log_alpha(log_q1, log_q2) gives log alpha at a point from the two log densities there.
    alpha = 1/q2 gives importance sampling with proposal p2; alpha = 1/q1 gives reciprocal
    importance sampling (the harmonic mean when p2 is the prior); alpha = 1/sqrt(q1 q2)
    gives the geometric bridge.
    """
    num = log_mean_exp([a + log_alpha(a, b) for a, b in zip(log_q1_at_2, log_q2_at_2)])
    den = log_mean_exp([b + log_alpha(a, b) for a, b in zip(log_q1_at_1, log_q2_at_1)])
    return num - den


def importance_sampling(log_q1_at_2: Sequence[float], log_q2_at_2: Sequence[float]) -> float:
    """log of mean_j q1(phi_j) / q2(phi_j) with phi_j ~ p2: the bridge with alpha = 1/q2."""
    return log_mean_exp([a - b for a, b in zip(log_q1_at_2, log_q2_at_2)])


def harmonic_mean(log_lik_at_post: Sequence[float]) -> float:
    """Harmonic mean estimate of log Z from log f(x | theta_i), theta_i ~ posterior.

    It is the bridge with p2 = prior and alpha = 1/q1: 1/Z = E_post[1/f(x | theta)].
    Its variance is often infinite; see the page.
    """
    return -log_mean_exp([-v for v in log_lik_at_post])
