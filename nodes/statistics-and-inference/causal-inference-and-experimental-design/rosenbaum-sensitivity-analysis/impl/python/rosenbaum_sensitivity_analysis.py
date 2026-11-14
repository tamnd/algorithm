# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rosenbaum-sensitivity-analysis/. The authors are listed in prov/4KS2ZT.jsonl.

"""Rosenbaum bounds for matched pairs.

In pair s the treated-minus-control difference is d[s]. Under the sharp null
of no effect and a hidden bias of at most gamma (the odds of treatment of the
two units in a pair differ by a factor of at most gamma), the chance that the
unit with the larger response is the treated one lies in
[1 / (1 + gamma), gamma / (1 + gamma)]. A statistic of the form sum q_s * 1[d_s > 0]
with q_s >= 0 is then bounded in law by the same sum with independent Bernoulli
signs at the two ends. Every bound is a one-sided p-value for the alternative
that treatment raises the response. With int or Fraction inputs the results are exact.
"""

import math
from collections.abc import Callable, Sequence
from fractions import Fraction


def doubled_midranks(values: Sequence) -> list[int]:
    """2 x (midrank of each value), in input order; doubling keeps tied midranks integral."""
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    r2 = [0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r2[order[k]] = i + j + 2
        i = j + 1
    return r2


def bernoulli_sum_law(q: Sequence[int], p) -> list:
    """law[v] = Pr[sum_s B_s q_s = v] for independent B_s ~ Bernoulli(p). Cost: Theta(len(q) * sum(q))."""
    total = sum(q)
    law = [0] * (total + 1)
    law[0] = 1
    top = 0
    for qs in q:
        top += qs
        for v in range(top, -1, -1):
            stay = law[v] * (1 - p)
            law[v] = stay + (law[v - qs] * p if v >= qs else 0)
    return law


def signed_rank_bounds(d: Sequence, gamma=1) -> tuple:
    """Bounds on the one-sided signed-rank p-value under hidden bias at most gamma.

    Returns (t, p_low, p_high), where t is the signed-rank statistic W+ (the sum of
    the ranks of |d_s| over the pairs with d_s > 0, midranks for ties, zero
    differences dropped). For every assignment law allowed by the model,
    p_low <= Pr[W+ >= t] <= p_high. gamma = 1 gives the exact Wilcoxon p-value twice.
    Cost: Theta(n^3) arithmetic operations for n nonzero pairs.
    """
    if gamma < 1:
        raise ValueError("gamma must be at least 1")
    kept = [v for v in d if v != 0]  # @line L1
    q2 = doubled_midranks([abs(v) for v in kept])  # @line L2
    t2 = sum(r for r, v in zip(q2, kept) if v > 0)  # @line L3
    p_hi = Fraction(gamma) / (1 + Fraction(gamma)) if not isinstance(gamma, float) else gamma / (1 + gamma)  # @line L4
    p_lo = 1 - p_hi
    up = bernoulli_sum_law(q2, p_hi)  # @line L5
    lo = bernoulli_sum_law(q2, p_lo)  # @line L6
    return Fraction(t2, 2), sum(lo[t2:]), sum(up[t2:])  # @line L7


def sign_test_bounds(k: int, n: int, gamma=1) -> tuple:
    """Bounds on Pr[K >= k] for binary outcomes (McNemar): n discordant pairs, k of them with the event in the treated unit.

    Returns (p_low, p_high) = upper tails of Binomial(n, 1/(1+gamma)) and Binomial(n, gamma/(1+gamma)).
    """
    if gamma < 1 or not 0 <= k <= n:
        raise ValueError("need gamma >= 1 and 0 <= k <= n")
    p = Fraction(gamma) / (1 + Fraction(gamma)) if not isinstance(gamma, float) else gamma / (1 + gamma)

    def tail(pr):
        return sum(math.comb(n, j) * pr**j * (1 - pr) ** (n - j) for j in range(k, n + 1))

    return tail(1 - p), tail(p)


def normal_upper_bound(d: Sequence, gamma: float = 1.0) -> float:
    """Normal approximation to p_high: the bounding sum has mean p sum q and variance p (1 - p) sum q^2."""
    kept = [v for v in d if v != 0]
    if not kept:
        return 1.0
    q = [r / 2 for r in doubled_midranks([abs(v) for v in kept])]
    t = sum(r for r, v in zip(q, kept) if v > 0)
    p = gamma / (1 + gamma)
    mean = p * sum(q)
    sd = math.sqrt(p * (1 - p) * sum(r * r for r in q))
    z = (t - mean) / sd
    return 0.5 * math.erfc(z / math.sqrt(2.0))


def sensitivity_value(upper: Callable[[float], float], alpha: float = 0.05, hi: float = 1000.0, tol: float = 1e-6) -> float:
    """The Gamma at which the upper p-value bound reaches alpha, found by bisection.

    upper(gamma) must be nondecreasing in gamma. Returns 1.0 if upper(1) > alpha
    (not significant even without bias) and hi if upper(hi) <= alpha.
    """
    if upper(1.0) > alpha:  # @line L8
        return 1.0
    if upper(hi) <= alpha:
        return hi
    a, b = 1.0, hi
    while b - a > tol * a:
        mid = (a + b) / 2
        if upper(mid) <= alpha:
            a = mid
        else:
            b = mid
    return (a + b) / 2
