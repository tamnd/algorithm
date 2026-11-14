# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nested-sampling/. The authors are listed in prov/G4YCZZ.jsonl.
"""Nested sampling (Skilling 2006) for the marginal likelihood Z = integral of L(theta) pi(d theta).

The caller gives:
  log_lik(theta)                     the log-likelihood log L(theta);
  prior_draw(rng)                    one draw from the prior pi;
  constrained_draw(rng, log_l_star)  one draw from pi restricted to {log L > log_l_star}.

The prior mass above the i-th dead likelihood is estimated by X_i = exp(-i/N), because
log X_i is a sum of i independent terms log t with t ~ Beta(N, 1) and E log t = -1/N.

Cost: about N (H + log(1/eps)) iterations for N live points, information H (nats) and
stopping tolerance eps. Each iteration makes one constrained draw and one O(log N)
heap update; the stopping test costs O(N) once every N iterations.
"""

import heapq
import math
import random
from fractions import Fraction
from typing import Callable, Sequence


def _log_add(a: float, b: float) -> float:
    """log(e^a + e^b)."""
    if a == -math.inf:
        return b
    if b == -math.inf:
        return a
    if a < b:
        a, b = b, a
    return a + math.log1p(math.exp(b - a))


def _update_h(h_acc: float, log_z_old: float, log_z_new: float, log_term: float, log_l: float) -> float:
    """Running value of (1/Z) sum_i w_i L_i log L_i, rescaled each time Z grows."""
    if log_z_old == -math.inf:
        return log_l
    return math.exp(log_z_old - log_z_new) * h_acc + math.exp(log_term - log_z_new) * log_l


def nested_sampling(
    log_lik: Callable,
    prior_draw: Callable,
    constrained_draw: Callable,
    n_live: int,
    rng: random.Random,
    eps: float = 1e-8,
    max_iter: int = 10**7,
) -> dict:
    """Run nested sampling. Returns a dict with
      log_z       the estimate of log Z,
      h           the estimated information H = KL(posterior || prior) in nats,
      error       Skilling's error estimate sqrt(h / n_live) for log_z,
      iterations  the number of dead points before the live points are added,
      dead        a list of (theta, log L, log w) for posterior summaries.

    Precondition: n_live >= 1; the law of L(theta) under the prior has no atoms;
    constrained_draw returns exact, independent draws from the constrained prior.
    """
    live = []
    for k in range(n_live):  # @line L1
        th = prior_draw(rng)
        live.append((log_lik(th), k, th))
    heapq.heapify(live)  # live[0] is the live point with the lowest likelihood
    counter = n_live
    log_z, log_x_prev, i = -math.inf, 0.0, 0  # @line L2
    h_acc = 0.0
    dead = []
    while i < max_iter:  # @line L3
        i += 1
        log_l_star, _, th_star = live[0]  # @line L4
        log_x = -i / n_live  # @line L5
        log_w = log_x_prev + math.log(-math.expm1(log_x - log_x_prev))  # log(X_{i-1} - X_i)
        log_z_new = _log_add(log_z, log_l_star + log_w)  # @line L6
        h_acc = _update_h(h_acc, log_z, log_z_new, log_l_star + log_w, log_l_star)
        log_z = log_z_new
        dead.append((th_star, log_l_star, log_w))
        th_new = constrained_draw(rng, log_l_star)  # @line L7
        heapq.heapreplace(live, (log_lik(th_new), counter, th_new))
        counter += 1
        log_x_prev = log_x
        if i % n_live == 0:
            log_l_max = max(p[0] for p in live)
            if log_l_max + log_x < math.log(eps) + log_z:  # @line L8
                break
    log_w = log_x_prev - math.log(n_live)
    for log_l, _, th in live:
        log_z_new = _log_add(log_z, log_l + log_w)  # @line L9
        h_acc = _update_h(h_acc, log_z, log_z_new, log_l + log_w, log_l)
        log_z = log_z_new
        dead.append((th, log_l, log_w))
    h = h_acc - log_z
    return {  # @line L10
        "log_z": log_z,
        "h": h,
        "error": math.sqrt(max(h, 0.0) / n_live),
        "iterations": i,
        "dead": dead,
    }


def posterior_mean(result: dict, f: Callable) -> float:
    """Posterior mean of f(theta) from the dead points, with weights w_i L_i / Z."""
    log_z = result["log_z"]
    return math.fsum(math.exp(lw + ll - log_z) * f(th) for th, ll, lw in result["dead"])


def layer_cake(values: Sequence, probs: Sequence) -> Fraction:
    """Z = integral_0^1 L(X) dX for a discrete prior, as an exact sum over the levels of L.

    X(lam) = P(L > lam) is a step function; sorting the distinct values of L in
    decreasing order and adding L_k (X(L_k-) - X(L_k)) gives sum_k p_k L_k exactly.
    Inputs are Fractions (or ints); ties in L are allowed.
    """
    levels = sorted(set(values), reverse=True)
    total = Fraction(0)
    for lam in levels:
        above = sum((p for v, p in zip(values, probs) if v > lam), Fraction(0))  # X(lam)
        at_or_above = sum((p for v, p in zip(values, probs) if v >= lam), Fraction(0))
        total += Fraction(lam) * (at_or_above - above)
    return total
