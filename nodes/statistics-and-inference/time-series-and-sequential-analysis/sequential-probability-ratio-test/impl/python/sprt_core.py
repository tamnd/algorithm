# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-probability-ratio-test/. The authors are listed in prov/9JY1HF.jsonl.
"""Wald's sequential probability ratio test (SPRT).

The test reads i.i.d. observations one at a time and keeps the log likelihood
ratio Lambda_n = sum log f1(x_i) - log f0(x_i). It stops as soon as Lambda_n
leaves the open interval (a, b) with Wald's thresholds
a = log(beta / (1 - alpha)) and b = log((1 - beta) / alpha).

Cost: O(1) time and O(1) memory per observation. The number of observations N
is random; under either hypothesis E[N] is finite when f0 and f1 differ.
"""

import math
from collections.abc import Callable, Iterable
from fractions import Fraction


def wald_thresholds(alpha: float, beta: float) -> tuple[float, float]:
    """Wald's thresholds (a, b) for target error rates alpha, beta with alpha + beta < 1."""
    if not (0.0 < alpha < 1.0 and 0.0 < beta < 1.0 and alpha + beta < 1.0):
        raise ValueError("need 0 < alpha, beta and alpha + beta < 1")
    return math.log(beta / (1.0 - alpha)), math.log((1.0 - beta) / alpha)


def sprt(stream: Iterable[float], log_f0: Callable[[float], float], log_f1: Callable[[float], float],
         alpha: float, beta: float) -> tuple[str, int, float]:
    """Run the SPRT of H0: density f0 against H1: density f1 on the stream.

    Returns (decision, n, Lambda_n) where decision is "reject H0", "accept H0",
    or "no decision" if the stream ends first. Precondition: f0 and f1 are
    positive on the same set, so every log ratio is finite. Cost O(1) per item.
    """
    a, b = wald_thresholds(alpha, beta)  # @line L1
    lam = 0.0  # @line L2
    n = 0  # @line L2
    for x in stream:  # @line L3
        n += 1  # @line L4
        lam += log_f1(x) - log_f0(x)  # @line L5
        if lam >= b:  # @line L6
            return "reject H0", n, lam  # @line L6
        if lam <= a:  # @line L7
            return "accept H0", n, lam  # @line L7
    return "no decision", n, lam


def bernoulli_sprt_exact(p0: float, p1: float, p: float, alpha: float, beta: float,
                         n_max: int) -> tuple[float, float, float, float]:
    """Exact operating characteristics of the Bernoulli SPRT, truncated at n_max.

    The state after n draws is the number of heads h, since Lambda_n =
    h log(p1/p0) + (n - h) log((1 - p1)/(1 - p0)). A forward dynamic program
    over (n, h) gives, under the true head probability p,
    (P(reject H0, N <= n_max), P(accept H0, N <= n_max), E[min(N, n_max)], P(N > n_max)).
    Cost O(n_max^2).
    """
    a, b = wald_thresholds(alpha, beta)
    up, down = math.log(p1 / p0), math.log((1.0 - p1) / (1.0 - p0))
    alive = {0: 1.0}
    rej = acc = 0.0
    e_n = 0.0
    for n in range(1, n_max + 1):
        e_n += sum(alive.values())
        nxt: dict[int, float] = {}
        for h, m in alive.items():
            for dh, q in ((1, p), (0, 1.0 - p)):
                h2 = h + dh
                lam = h2 * up + (n - h2) * down
                if lam >= b:
                    rej += m * q
                elif lam <= a:
                    acc += m * q
                else:
                    nxt[h2] = nxt.get(h2, 0.0) + m * q
        alive = nxt
    return rej, acc, e_n, sum(alive.values())


def bernoulli_sprt_moments_exact(p0: float, p1: float, p: Fraction, alpha: float, beta: float,
                                 n_max: int) -> tuple[Fraction, Fraction]:
    """E[H_T] and E[T] in exact rational arithmetic, T = min(N, n_max), H_T = heads seen.

    The stopping rule uses floating log ratios; the probabilities are exact
    Fractions in p. Wald's equation says E[H_T] = p E[T] for the bounded
    stopping time T.
    """
    a, b = wald_thresholds(alpha, beta)
    up, down = math.log(p1 / p0), math.log((1.0 - p1) / (1.0 - p0))
    alive = {0: Fraction(1)}
    e_h = Fraction(0)
    e_t = Fraction(0)
    for n in range(1, n_max + 1):
        nxt: dict[int, Fraction] = {}
        for h, m in alive.items():
            for dh, q in ((1, p), (0, 1 - p)):
                h2 = h + dh
                lam = h2 * up + (n - h2) * down
                if lam >= b or lam <= a or n == n_max:
                    e_h += m * q * h2
                    e_t += m * q * n
                else:
                    nxt[h2] = nxt.get(h2, Fraction(0)) + m * q
        alive = nxt
    return e_h, e_t


def wald_asn(mean_step: float, p_upper: float, a: float, b: float) -> float:
    """Wald's ASN approximation E[N] = (p_upper b + (1 - p_upper) a) / E[Z], overshoot ignored."""
    return (p_upper * b + (1.0 - p_upper) * a) / mean_step
